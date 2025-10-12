from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from app.core.auth import require_teacher
from app.core.database import get_database, get_gridfs
from app.services.file_parser import FileParser
from app.services.langgraph_flow import paper_generator
from app.services.pdf_generator import PDFGenerator
from app.services.mail_service import mail_service
from app.services.embedding_service import embedding_service
from app.services.cloudinary_service import cloudinary_service
from app.schemas.paper import GeneratePaperRequest, ApprovePaperRequest, RegeneratePaperRequest, EditApprovedPaperRequest, UpdatePaperMetadataRequest
from bson import ObjectId
from datetime import datetime
import os
import aiofiles
from app.core.config import settings

router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.post("/upload-resource")
async def upload_resource(
    file: UploadFile = File(...),
    subject: str = Form(None),
    department: str = Form(None),
    year: int = Form(None),
    section: str = Form(None),
    current_user: dict = Depends(require_teacher)
):
    """Upload a resource file to Cloudinary (PDF, DOCX, PPTX, Image)"""
    db = get_database()
    
    print(f"\n📤 Upload request from teacher {current_user['user_id']}")
    print(f"   File: {file.filename} ({file.content_type})")
    
    # Validate file type
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: PDF, DOCX, PPTX, Images"
        )
    
    allowed_extensions = ['.pdf', '.docx', '.pptx', '.jpg', '.jpeg', '.png', '.webp']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file extension")
    
    # Read file content once
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds {settings.MAX_FILE_SIZE / 1024 / 1024}MB limit"
        )
    
    # Quick PDF validation (non-blocking)
    if file_ext == '.pdf':
        import fitz
        try:
            pdf_doc = fitz.open(stream=content, filetype="pdf")
            page_count = pdf_doc.page_count
            if page_count > 100:
                pdf_doc.close()
                raise HTTPException(status_code=400, detail="PDF exceeds 100 pages limit")
            pdf_doc.close()
            print(f"   ✅ PDF validated: {page_count} pages")
        except HTTPException:
            raise
        except Exception as e:
            print(f"   ⚠️ PDF validation warning: {e}")
    
    # Upload to Cloudinary FIRST (parallel with parsing)
    import time
    upload_start = time.time()
    
    print(f"   ☁️ Uploading to Cloudinary...")
    print(f"   📦 File size: {file_size / 1024 / 1024:.2f} MB")
    
    # Reset file pointer for Cloudinary upload
    await file.seek(0)
    
    try:
        # Upload happens in background while we parse
        cloudinary_result = await cloudinary_service.upload_file(
            file=file,
            folder=f"exam_resources/{current_user['user_id']}"
        )
        
        upload_time = time.time() - upload_start
        print(f"   ✅ Cloudinary upload successful: {cloudinary_result['public_id']}")
        print(f"   ⏱️  Upload took: {upload_time:.2f} seconds")
        
        # Warn if upload is slow
        if upload_time > 30:
            print(f"   ⚠️  Slow upload detected! Consider compressing files to under 2MB")
        
    except Exception as e:
        upload_time = time.time() - upload_start
        print(f"   ❌ Upload failed after {upload_time:.2f} seconds")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to upload to Cloudinary: {str(e)}"
        )
    
    # Parse file to extract text and topics (can be done async after upload)
    parser = FileParser()
    try:
        print(f"   📄 Parsing file for content extraction...")
        if file_ext == '.pdf':
            extracted_text, topics = await parser.parse_pdf(content)
        elif file_ext == '.docx':
            extracted_text, topics = await parser.parse_docx(content)
        elif file_ext == '.pptx':
            extracted_text, topics = await parser.parse_pptx(content)
        else:  # Image
            extracted_text, topics = await parser.parse_image(content)
        
        print(f"   ✅ Extracted {len(extracted_text)} characters, {len(topics)} topics")
        
    except Exception as e:
        # Don't fail upload if parsing fails - store with empty content
        print(f"   ⚠️ Parsing warning: {str(e)}")
        extracted_text = ""
        topics = []
    
    # Get teacher info
    teacher = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
    
    # Store metadata in MongoDB Atlas
    resource_data = {
        "teacher_id": current_user["user_id"],
        "filename": file.filename,
        "file_type": file_ext[1:],
        "file_size": file_size,
        "content_type": file.content_type,
        
        # Cloudinary data
        "cloudinary_url": cloudinary_result["url"],
        "cloudinary_public_id": cloudinary_result["public_id"],
        "cloudinary_resource_type": cloudinary_result["resource_type"],
        
        # Extracted content
        "extracted_text": extracted_text,
        "topics": topics,
        
        # Metadata
        "subject": subject,
        "department": department,
        "year": year,
        "section": section,
        "uploaded_by": teacher.get("full_name") if teacher else None,
        "uploaded_at": datetime.utcnow(),
        "processed": True
    }
    
    result = await db.resources.insert_one(resource_data)
    
    print(f"   ✅ Resource saved to MongoDB: {result.inserted_id}")
    
    return {
        "id": str(result.inserted_id),
        "filename": file.filename,
        "cloudinary_url": cloudinary_result["url"],
        "topics": topics,
        "file_size": file_size,
        "message": "Resource uploaded successfully to Cloudinary"
    }


@router.get("/resources")
async def list_resources(
    current_user: dict = Depends(require_teacher)
):
    """List all uploaded resources from MongoDB Atlas"""
    db = get_database()
    
    resources = await db.resources.find({
        "teacher_id": current_user["user_id"]
    }).sort("uploaded_at", -1).to_list(length=1000)
    
    return [
        {
            "id": str(r["_id"]),
            "filename": r["filename"],
            "file_type": r["file_type"],
            "file_size": r["file_size"],
            "cloudinary_url": r.get("cloudinary_url"),  # Cloudinary URL
            "topics": r.get("topics", []),
            "subject": r.get("subject"),
            "department": r.get("department"),
            "uploaded_by": r.get("uploaded_by"),
            "uploaded_at": r["uploaded_at"]
        }
        for r in resources
    ]


@router.get("/subjects-departments")
async def get_subjects_and_departments(
    current_user: dict = Depends(require_teacher)
):
    """Get unique subjects and departments from uploaded resources (case-insensitive)"""
    db = get_database()
    
    # Get all resources for this teacher
    resources = await db.resources.find({
        "teacher_id": current_user["user_id"],
        "processed": True
    }).to_list(length=10000)
    
    # Extract unique subjects and departments (case-insensitive)
    subjects_map = {}  # lowercase -> proper case
    departments_map = {}  # lowercase -> proper case
    subject_department_map = {}  # subject -> [departments]
    department_subject_map = {}  # department -> [subjects]
    
    for r in resources:
        subject = r.get("subject", "").strip()
        department = r.get("department", "").strip()
        
        # Add subject
        if subject:
            subject_lower = subject.lower()
            if subject_lower not in subjects_map:
                subjects_map[subject_lower] = subject
            
            # Map subject to departments
            if subject_lower not in subject_department_map:
                subject_department_map[subject_lower] = set()
            if department:
                subject_department_map[subject_lower].add(department.lower())
        
        # Add department
        if department:
            department_lower = department.lower()
            if department_lower not in departments_map:
                departments_map[department_lower] = department
            
            # Map department to subjects
            if department_lower not in department_subject_map:
                department_subject_map[department_lower] = set()
            if subject:
                department_subject_map[department_lower].add(subject.lower())
    
    # Convert to lists
    subjects = sorted(subjects_map.values(), key=str.lower)
    departments = sorted(departments_map.values(), key=str.lower)
    
    # Build mapping with proper case
    subject_to_departments = {}
    for subject_lower, dept_set in subject_department_map.items():
        proper_subject = subjects_map[subject_lower]
        subject_to_departments[proper_subject] = sorted([
            departments_map[d] for d in dept_set if d in departments_map
        ], key=str.lower)
    
    department_to_subjects = {}
    for dept_lower, subj_set in department_subject_map.items():
        proper_dept = departments_map[dept_lower]
        department_to_subjects[proper_dept] = sorted([
            subjects_map[s] for s in subj_set if s in subjects_map
        ], key=str.lower)
    
    return {
        "subjects": subjects,
        "departments": departments,
        "subject_to_departments": subject_to_departments,
        "department_to_subjects": department_to_subjects
    }


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Delete a resource from Cloudinary and MongoDB Atlas, and remove from RAG"""
    db = get_database()
    
    # Get the resource
    resource = await db.resources.find_one({
        "_id": ObjectId(resource_id),
        "teacher_id": current_user["user_id"]
    })
    
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    print(f"\n🗑️  Deleting resource: {resource['filename']}")
    
    # Delete file from Cloudinary
    if resource.get("cloudinary_public_id"):
        try:
            resource_type = resource.get("cloudinary_resource_type", "raw")
            await cloudinary_service.delete_file(
                resource["cloudinary_public_id"],
                resource_type=resource_type
            )
            print(f"   ✅ Deleted file from Cloudinary")
        except Exception as e:
            print(f"   ⚠️  Error deleting from Cloudinary: {e}")
    
    # Legacy: Delete from GridFS if exists
    if resource.get("gridfs_id"):
        try:
            fs = get_gridfs()
            await fs.delete(ObjectId(resource["gridfs_id"]))
            print(f"   ✅ Deleted legacy file from GridFS")
        except Exception as e:
            print(f"   ⚠️  Error deleting from GridFS: {e}")
    
    # Delete embeddings from vector store (RAG)
    try:
        # Delete embeddings associated with this resource
        deleted_count = await embedding_service.delete_embeddings_by_resource(resource_id)
        print(f"   ✅ Deleted {deleted_count} embeddings from RAG")
    except Exception as e:
        print(f"   ⚠️  Error deleting embeddings: {e}")
    
    # Delete resource metadata from database
    await db.resources.delete_one({"_id": ObjectId(resource_id)})
    print(f"   ✅ Deleted resource metadata")
    
    return {
        "message": "Resource deleted successfully",
        "filename": resource["filename"]
    }


@router.post("/generate-paper")
async def generate_paper_endpoint(
    request: GeneratePaperRequest,
    current_user: dict = Depends(require_teacher)
):
    """Generate exam paper using LangGraph with advanced features"""
    db = get_database()
    
    # Calculate total marks
    total_marks = (
        (request.mcq_count * request.mcq_marks) +
        (request.short_count * request.short_marks) +
        (request.medium_count * request.medium_marks) +
        (request.long_count * request.long_marks)
    )
    
    # Build detailed prompt with all requirements
    detailed_prompt = f"""
Generate a {request.exam_type} exam paper with the following specifications:

QUESTION DISTRIBUTION:
- MCQ: {request.mcq_count} questions × {request.mcq_marks} marks = {request.mcq_count * request.mcq_marks} marks
- Short Answer: {request.short_count} questions × {request.short_marks} marks = {request.short_count * request.short_marks} marks
- Medium Answer: {request.medium_count} questions × {request.medium_marks} marks = {request.medium_count * request.medium_marks} marks
- Long Answer: {request.long_count} questions × {request.long_marks} marks = {request.long_count * request.long_marks} marks

QUESTION SOURCE REQUIREMENTS:
- {request.previous_percent}% from Previous Year papers (use similar questions from past papers)
- {request.creative_percent}% Creative/Modified (modify existing questions creatively)
- {request.new_percent}% New/AI-Generated (create completely new questions)

BLOOM'S TAXONOMY DISTRIBUTION:
- MCQ questions: Remember, Understand levels
- Short Answer: Understand, Apply levels
- Medium Answer: Apply, Analyze levels
- Long Answer: Analyze, Evaluate, Create levels

{f"TOPIC FOCUS: {request.prompt}" if request.prompt else "Cover all major topics from the syllabus"}

IMPORTANT: 
- For MCQ questions, format as: "Question?\nA) option1\nB) option2\nC) option3\nD) option4"
- Ensure all questions are relevant to the subject
- Maintain academic standards
- No duplicate questions
"""
    
    # Create prompt history entry
    history_data = {
        "teacher_id": current_user["user_id"],
        "prompt": detailed_prompt,
        "parameters": {
            "subject": request.subject,
            "department": request.department,
            "exam_type": request.exam_type,
            "total_marks": total_marks,
            "mcq_count": request.mcq_count,
            "short_count": request.short_count,
            "medium_count": request.medium_count,
            "long_count": request.long_count,
            "source_distribution": {
                "previous": request.previous_percent,
                "creative": request.creative_percent,
                "new": request.new_percent
            }
        },
        "status": "in_progress",
        "created_at": datetime.utcnow()
    }
    
    history_result = await db.prompts_history.insert_one(history_data)
    
    try:
        # Use LangGraph paper generator
        result = await paper_generator.generate_paper(
            teacher_id=current_user["user_id"],
            subject=request.subject,
            department=request.department,
            total_marks=total_marks,
            prompt=detailed_prompt,
            blooms_distribution=None,  # Auto-distribute based on question types
            unit_requirements=None
        )
        
        if result["current_step"] == "error":
            raise Exception("; ".join(result["errors"]))
        
        # Extract questions and add metadata
        questions = result["final_paper"]["questions"]
        
        # Add source type and format questions properly
        for i, q in enumerate(questions):
            # Determine source type based on position (distribute according to percentages)
            total_questions = len(questions)
            previous_count = int(total_questions * request.previous_percent / 100)
            creative_count = int(total_questions * request.creative_percent / 100)
            
            if i < previous_count:
                q["source"] = "previous"
            elif i < previous_count + creative_count:
                q["source"] = "creative"
            else:
                q["source"] = "new"
            
            # Add explanation field if not present
            if "explanation" not in q:
                q["explanation"] = q.get("answer_key", "")
        
        # Calculate detailed Bloom's distribution with source types
        blooms_with_sources = {}
        blooms_distribution = {}
        
        for q in questions:
            blooms_level = q.get("blooms_level", "Unknown")
            source = q.get("source", "new")
            
            # Initialize if not exists
            if blooms_level not in blooms_with_sources:
                blooms_with_sources[blooms_level] = {
                    "total": 0,
                    "previous": 0,
                    "creative": 0,
                    "new": 0
                }
            
            # Count total for this Bloom's level
            blooms_with_sources[blooms_level]["total"] += 1
            blooms_with_sources[blooms_level][source] += 1
            
            # Simple count for backward compatibility
            blooms_distribution[blooms_level] = blooms_with_sources[blooms_level]["total"]
        
        # Calculate summary
        summary = {
            "total_questions": len(questions),
            "total_marks": total_marks,
            "question_distribution": {
                "MCQ": sum(1 for q in questions if q.get("question_type") == "MCQ"),
                "Short": sum(1 for q in questions if "Short" in q.get("question_type", "")),
                "Medium": sum(1 for q in questions if "Medium" in q.get("question_type", "") or q.get("marks", 0) >= 5),
                "Long": sum(1 for q in questions if "Long" in q.get("question_type", "") or q.get("marks", 0) >= 10)
            },
            "source_distribution": {
                "Previous": sum(1 for q in questions if q.get("source") == "previous"),
                "Creative": sum(1 for q in questions if q.get("source") == "creative"),
                "New": sum(1 for q in questions if q.get("source") == "new")
            },
            "blooms_distribution": blooms_distribution,
            "blooms_with_sources": blooms_with_sources
        }
        
        # Store paper in database
        paper_data = {
            "teacher_id": current_user["user_id"],
            "subject": request.subject,
            "department": request.department,
            "section": request.section,
            "year": request.year,
            "exam_date": request.exam_date,
            "exam_type": request.exam_type,
            "total_marks": total_marks,
            "generation_prompt": detailed_prompt,
            "questions": questions,
            "summary": summary,
            "blooms_distribution": result["final_paper"].get("blooms_distribution", {}),
            "status": "draft",
            "created_at": datetime.utcnow()
        }
        
        paper_result = await db.papers.insert_one(paper_data)
        paper_id = str(paper_result.inserted_id)
        
        # Update history
        await db.prompts_history.update_one(
            {"_id": history_result.inserted_id},
            {
                "$set": {
                    "paper_id": paper_id,
                    "status": "success",
                    "completed_at": datetime.utcnow()
                }
            }
        )
        
        # Get user info for email
        user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
        
        # Send notification email
        try:
            await mail_service.send_paper_generated_notification(
                user["email"],
                user["full_name"],
                request.subject,
                paper_id
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        return {
            "paper_id": paper_id,
            "questions": questions,
            "summary": summary,
            "blooms_distribution": result["final_paper"].get("blooms_distribution", {}),
            "total_marks": total_marks,
            "message": "Paper generated successfully"
        }
    
    except Exception as e:
        # Update history with error
        await db.prompts_history.update_one(
            {"_id": history_result.inserted_id},
            {
                "$set": {
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": datetime.utcnow()
                }
            }
        )
        
        raise HTTPException(status_code=500, detail=f"Failed to generate paper: {str(e)}")


@router.get("/papers")
async def list_papers(
    current_user: dict = Depends(require_teacher)
):
    """List all generated papers"""
    db = get_database()
    
    papers = await db.papers.find({
        "teacher_id": current_user["user_id"]
    }).sort("created_at", -1).to_list(length=1000)
    
    return [
        {
            "id": str(p["_id"]),
            "subject": p["subject"],
            "department": p["department"],
            "total_marks": p["total_marks"],
            "status": p["status"],
            "blooms_distribution": p.get("blooms_distribution", {}),
            "created_at": p["created_at"],
            "approved_at": p.get("approved_at")
        }
        for p in papers
    ]


@router.get("/papers/{paper_id}")
async def get_paper(
    paper_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Get paper details"""
    db = get_database()
    
    paper = await db.papers.find_one({
        "_id": ObjectId(paper_id),
        "teacher_id": current_user["user_id"]
    })
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return {
        "_id": str(paper["_id"]),
        "id": str(paper["_id"]),
        "subject": paper["subject"],
        "department": paper["department"],
        "section": paper.get("section"),
        "year": paper.get("year"),
        "exam_date": paper.get("exam_date"),
        "total_marks": paper["total_marks"],
        "questions": paper.get("questions", []),
        "blooms_distribution": paper.get("blooms_distribution", {}),
        "status": paper["status"],
        "regeneration_count": paper.get("regeneration_count", 0),
        "question_paper_pdf": paper.get("question_paper_pdf"),
        "answer_key_pdf": paper.get("answer_key_pdf"),
        "created_at": paper["created_at"]
    }


@router.post("/approve-paper")
async def approve_paper(
    request: ApprovePaperRequest,
    current_user: dict = Depends(require_teacher)
):
    """Approve paper and generate PDFs"""
    db = get_database()
    fs = get_gridfs()
    
    # Get paper
    paper = await db.papers.find_one({
        "_id": ObjectId(request.paper_id),
        "teacher_id": current_user["user_id"]
    })
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Generate PDFs
    pdf_gen = PDFGenerator()
    
    question_paper_pdf = pdf_gen.generate_question_paper(
        subject=paper["subject"],
        department=paper["department"],
        section=paper.get("section", ""),
        year=paper.get("year", 2024),
        exam_date=paper.get("exam_date", datetime.utcnow()),
        total_marks=paper["total_marks"],
        questions=paper["questions"]
    )
    
    answer_key_pdf = pdf_gen.generate_answer_key(
        subject=paper["subject"],
        department=paper["department"],
        questions=paper["questions"]
    )
    
    # Store PDFs in GridFS
    question_paper_id = await fs.upload_from_stream(
        f"question_paper_{request.paper_id}.pdf",
        question_paper_pdf
    )
    
    answer_key_id = await fs.upload_from_stream(
        f"answer_key_{request.paper_id}.pdf",
        answer_key_pdf
    )
    
    # Update paper
    await db.papers.update_one(
        {"_id": ObjectId(request.paper_id)},
        {
            "$set": {
                "status": "approved",
                "approved_at": datetime.utcnow(),
                "question_paper_pdf": str(question_paper_id),
                "answer_key_pdf": str(answer_key_id)
            }
        }
    )
    
    # Add questions to FAISS index for future duplicate detection
    try:
        questions_to_add = [
            (q["question_text"], f"{request.paper_id}_{i}")
            for i, q in enumerate(paper["questions"])
        ]
        embedding_service.add_questions_batch(questions_to_add)
        print(f"✅ Added {len(questions_to_add)} questions to FAISS index")
    except Exception as e:
        print(f"⚠️  Failed to add questions to FAISS: {e}")
    
    return {
        "message": "Paper approved successfully",
        "question_paper_id": str(question_paper_id),
        "answer_key_id": str(answer_key_id)
    }


@router.post("/regenerate-paper")
async def regenerate_paper(
    request: RegeneratePaperRequest,
    current_user: dict = Depends(require_teacher)
):
    """Regenerate paper with optional feedback"""
    db = get_database()
    
    # Get original paper
    paper = await db.papers.find_one({
        "_id": ObjectId(request.paper_id),
        "teacher_id": current_user["user_id"]
    })
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Build enhanced prompt with STRICT preservation of original requirements
    original_prompt = paper.get("generation_prompt", "")
    previous_questions = paper.get("questions", [])
    total_marks = paper["total_marks"]
    
    # Extract question count from original prompt
    import re
    question_count_match = re.search(r'(\d+)\s*(?:questions?|mcqs?|problems?)', original_prompt.lower())
    question_count = int(question_count_match.group(1)) if question_count_match else len(previous_questions)
    
    # Create STRICT context-aware prompt that preserves requirements
    enhanced_prompt = f"""CRITICAL REQUIREMENTS (MUST BE FOLLOWED EXACTLY):
- Total Marks: {total_marks} (EXACT)
- Number of Questions: {question_count} (EXACT)
- Subject: {paper["subject"]}
- Department: {paper["department"]}

ORIGINAL TEACHER'S INSTRUCTIONS (FOLLOW STRICTLY):
{original_prompt}

PREVIOUS GENERATION SUMMARY:
- Generated {len(previous_questions)} questions with {sum(q.get('marks', 0) for q in previous_questions)} marks
- Question types used: {', '.join(set(q.get('question_type', '') for q in previous_questions))}
- Bloom's levels: {', '.join(set(q.get('blooms_level', '') for q in previous_questions))}
"""
    
    if request.feedback_prompt:
        enhanced_prompt += f"""
REGENERATION FEEDBACK (Apply while maintaining above requirements):
{request.feedback_prompt}

IMPORTANT: Apply the feedback BUT still generate EXACTLY {question_count} questions with EXACTLY {total_marks} marks total.
"""
    else:
        enhanced_prompt += f"""
REGENERATION GOAL: Generate a fresh set of {question_count} questions with {total_marks} marks, maintaining quality and variety.
"""
    
    # Create regeneration history entry
    history_data = {
        "teacher_id": current_user["user_id"],
        "prompt": enhanced_prompt,
        "original_paper_id": request.paper_id,
        "feedback": request.feedback_prompt,
        "parameters": {
            "subject": paper["subject"],
            "department": paper["department"],
            "total_marks": paper["total_marks"],
            "blooms_distribution": paper.get("blooms_distribution", {})
        },
        "status": "in_progress",
        "created_at": datetime.utcnow()
    }
    
    history_result = await db.prompts_history.insert_one(history_data)
    
    try:
        print(f"\n🔄 REGENERATION MODE: Maintaining strict requirements from original prompt")
        print(f"   Original: {paper['subject']} - {len(previous_questions)} questions, {total_marks} marks")
        print(f"   Feedback: {request.feedback_prompt or 'None - fresh generation'}")
        
        # Generate new paper with enhanced prompt
        result = await paper_generator.generate_paper(
            teacher_id=current_user["user_id"],
            subject=paper["subject"],
            department=paper["department"],
            total_marks=paper["total_marks"],
            prompt=enhanced_prompt,
            blooms_distribution=paper.get("blooms_distribution") or {},
            unit_requirements=paper.get("unit_requirements") or {}
        )
        
        if result["current_step"] == "error":
            raise Exception("; ".join(result["errors"]))
        
        # Store new paper version
        new_paper_data = {
            "teacher_id": current_user["user_id"],
            "subject": paper["subject"],
            "department": paper["department"],
            "section": paper.get("section"),
            "year": paper.get("year"),
            "exam_date": paper.get("exam_date"),
            "total_marks": result["final_paper"]["total_marks"],
            "generation_prompt": enhanced_prompt,
            "original_paper_id": request.paper_id,
            "regeneration_count": paper.get("regeneration_count", 0) + 1,
            "questions": result["final_paper"]["questions"],
            "blooms_distribution": result["final_paper"]["blooms_distribution"],
            "status": "pending",  # Changed from "draft" to "pending"
            "created_at": datetime.utcnow()
        }
        
        print(f"✅ Regeneration successful: {len(result['final_paper']['questions'])} questions, {result['final_paper']['total_marks']} marks")
        
        new_paper_result = await db.papers.insert_one(new_paper_data)
        new_paper_id = str(new_paper_result.inserted_id)
        
        # Mark old paper as superseded
        await db.papers.update_one(
            {"_id": ObjectId(request.paper_id)},
            {
                "$set": {
                    "status": "superseded",
                    "superseded_by": new_paper_id,
                    "superseded_at": datetime.utcnow()
                }
            }
        )
        
        # Update history
        await db.prompts_history.update_one(
            {"_id": history_result.inserted_id},
            {
                "$set": {
                    "paper_id": new_paper_id,
                    "status": "success",
                    "completed_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "paper_id": new_paper_id,
            "questions": result["final_paper"]["questions"],
            "blooms_distribution": result["final_paper"]["blooms_distribution"],
            "total_marks": result["final_paper"]["total_marks"],
            "regeneration_count": new_paper_data["regeneration_count"],
            "message": "Paper regenerated successfully"
        }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n❌ REGENERATION ERROR:")
        print(error_details)
        
        # Update history with error
        await db.prompts_history.update_one(
            {"_id": history_result.inserted_id},
            {
                "$set": {
                    "status": "failed",
                    "error_message": str(e),
                    "completed_at": datetime.utcnow()
                }
            }
        )
        
        raise HTTPException(status_code=500, detail=f"Failed to regenerate paper: {str(e)}")


@router.get("/download-pdf/{file_id}")
async def download_pdf(
    file_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Download PDF file"""
    from fastapi.responses import StreamingResponse
    
    fs = get_gridfs()
    
    try:
        # Get file from GridFS
        grid_out = await fs.open_download_stream(ObjectId(file_id))
        content = await grid_out.read()
        
        return StreamingResponse(
            iter([content]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={grid_out.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/history")
async def get_generation_history(
    current_user: dict = Depends(require_teacher)
):
    """Get paper generation history"""
    db = get_database()
    
    history = await db.prompts_history.find({
        "teacher_id": current_user["user_id"]
    }).sort("created_at", -1).to_list(length=100)
    
    return [
        {
            "id": str(h["_id"]),
            "prompt": h["prompt"],
            "parameters": h.get("parameters", {}),
            "status": h["status"],
            "paper_id": h.get("paper_id"),
            "error_message": h.get("error_message"),
            "created_at": h["created_at"],
            "completed_at": h.get("completed_at")
        }
        for h in history
    ]


@router.delete("/history/{history_id}")
async def delete_history_item(
    history_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Delete a single history item (and associated draft/pending paper if exists)"""
    db = get_database()
    fs = get_gridfs()
    
    # Get history item first
    history_item = await db.prompts_history.find_one({
        "_id": ObjectId(history_id),
        "teacher_id": current_user["user_id"]
    })
    
    if not history_item:
        raise HTTPException(status_code=404, detail="History item not found")
    
    # Check if there's an associated paper
    paper_id = history_item.get("paper_id")
    deleted_paper = False
    
    if paper_id:
        # Get the paper
        paper = await db.papers.find_one({"_id": ObjectId(paper_id)})
        
        if paper:
            # Only delete paper if it's pending or draft (not approved)
            if paper.get("status") in ["pending", "draft", "superseded"]:
                print(f"🗑️  Deleting associated paper {paper_id} (status: {paper.get('status')})")
                
                # Delete PDFs if they exist
                try:
                    if paper.get("question_paper_pdf"):
                        await fs.delete(ObjectId(paper["question_paper_pdf"]))
                    if paper.get("answer_key_pdf"):
                        await fs.delete(ObjectId(paper["answer_key_pdf"]))
                except Exception as e:
                    print(f"Error deleting PDFs: {e}")
                
                # Delete paper
                await db.papers.delete_one({"_id": ObjectId(paper_id)})
                deleted_paper = True
            else:
                print(f"ℹ️  Keeping approved paper {paper_id}")
    
    # Delete history record
    await db.prompts_history.delete_one({"_id": ObjectId(history_id)})
    
    message = "History item deleted successfully"
    if deleted_paper:
        message += " (associated draft paper also deleted)"
    
    return {"message": message, "deleted_paper": deleted_paper}


@router.delete("/history")
async def clear_all_history(
    current_user: dict = Depends(require_teacher)
):
    """Clear all history for the current user (and associated draft/pending papers)"""
    db = get_database()
    fs = get_gridfs()
    
    # Get all history items for this user
    history_items = await db.prompts_history.find({
        "teacher_id": current_user["user_id"]
    }).to_list(length=1000)
    
    deleted_papers_count = 0
    
    # Delete associated draft/pending papers
    for item in history_items:
        paper_id = item.get("paper_id")
        if paper_id:
            paper = await db.papers.find_one({"_id": ObjectId(paper_id)})
            if paper and paper.get("status") in ["pending", "draft", "superseded"]:
                print(f"🗑️  Deleting paper {paper_id} (status: {paper.get('status')})")
                
                # Delete PDFs
                try:
                    if paper.get("question_paper_pdf"):
                        await fs.delete(ObjectId(paper["question_paper_pdf"]))
                    if paper.get("answer_key_pdf"):
                        await fs.delete(ObjectId(paper["answer_key_pdf"]))
                except Exception as e:
                    print(f"Error deleting PDFs: {e}")
                
                # Delete paper
                await db.papers.delete_one({"_id": ObjectId(paper_id)})
                deleted_papers_count += 1
    
    # Delete all history records
    result = await db.prompts_history.delete_many({
        "teacher_id": current_user["user_id"]
    })
    
    message = f"Deleted {result.deleted_count} history items"
    if deleted_papers_count > 0:
        message += f" and {deleted_papers_count} draft papers"
    
    return {
        "message": message,
        "deleted_count": result.deleted_count,
        "deleted_papers": deleted_papers_count
    }


# ============================================
# APPROVED PAPERS MANAGEMENT
# ============================================

@router.get("/approved-papers")
async def search_approved_papers(
    subject: str = None,
    department: str = None,
    current_user: dict = Depends(require_teacher)
):
    """Search approved papers by subject and department (only user's own papers)"""
    db = get_database()
    
    # Build query - FILTER BY CURRENT USER
    query = {
        "status": "approved",
        "teacher_id": current_user["user_id"]  # Only show user's own papers
    }
    
    # Add subject filter if provided
    if subject:
        query["subject"] = {"$regex": subject, "$options": "i"}
    
    # Add department filter if provided
    if department:
        query["department"] = {"$regex": department, "$options": "i"}
    
    print(f"🔍 Searching approved papers for teacher {current_user['user_id']}")
    
    # Fetch approved papers
    papers = await db.papers.find(query).sort("created_at", -1).to_list(length=100)
    
    print(f"   ✅ Found {len(papers)} approved papers")
    
    return [
        {
            "id": str(paper["_id"]),
            "subject": paper["subject"],
            "department": paper["department"],
            "section": paper.get("section"),
            "year": paper.get("year"),
            "exam_date": paper.get("exam_date"),
            "total_marks": paper["total_marks"],
            "question_count": len(paper.get("questions", [])),
            "status": paper["status"],
            "created_at": paper["created_at"],
            "teacher_id": paper["teacher_id"],
            "question_paper_pdf": paper.get("question_paper_pdf"),
            "answer_key_pdf": paper.get("answer_key_pdf")
        }
        for paper in papers
    ]


@router.get("/approved-papers/{paper_id}")
async def get_approved_paper_details(
    paper_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Get detailed information about an approved paper (only user's own)"""
    db = get_database()
    
    paper = await db.papers.find_one({
        "_id": ObjectId(paper_id),
        "status": "approved",
        "teacher_id": current_user["user_id"]  # Only user's own papers
    })
    
    if not paper:
        raise HTTPException(status_code=404, detail="Approved paper not found or access denied")
    
    return {
        "_id": str(paper["_id"]),
        "id": str(paper["_id"]),
        "subject": paper["subject"],
        "department": paper["department"],
        "section": paper.get("section"),
        "year": paper.get("year"),
        "exam_date": paper.get("exam_date"),
        "total_marks": paper["total_marks"],
        "questions": paper.get("questions", []),
        "blooms_distribution": paper.get("blooms_distribution", {}),
        "status": paper["status"],
        "created_at": paper["created_at"],
        "question_paper_pdf": paper.get("question_paper_pdf"),
        "answer_key_pdf": paper.get("answer_key_pdf")
    }


@router.delete("/approved-papers/{paper_id}")
async def delete_approved_paper(
    paper_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Delete an approved paper (only user's own)"""
    db = get_database()
    fs = get_gridfs()
    
    # Get paper - verify ownership
    paper = await db.papers.find_one({
        "_id": ObjectId(paper_id),
        "status": "approved",
        "teacher_id": current_user["user_id"]  # Only user's own papers
    })
    
    if not paper:
        raise HTTPException(status_code=404, detail="Approved paper not found or access denied")
    
    print(f"🗑️  Deleting approved paper: {paper['subject']} (by teacher {current_user['user_id']})")
    
    # Delete PDFs from GridFS
    try:
        if paper.get("question_paper_pdf"):
            await fs.delete(ObjectId(paper["question_paper_pdf"]))
        if paper.get("answer_key_pdf"):
            await fs.delete(ObjectId(paper["answer_key_pdf"]))
    except Exception as e:
        print(f"Error deleting PDFs: {e}")
    
    # Delete paper from database
    await db.papers.delete_one({"_id": ObjectId(paper_id)})
    
    return {"message": "Approved paper deleted successfully"}


@router.patch("/papers/{paper_id}/metadata")
async def update_paper_metadata(
    paper_id: str,
    request: UpdatePaperMetadataRequest,
    current_user: dict = Depends(require_teacher)
):
    """Update paper metadata (subject, department, section, year, total_marks)"""
    db = get_database()
    
    # Build update dict from request
    update_data = {}
    if request.subject is not None:
        update_data["subject"] = request.subject
    if request.department is not None:
        update_data["department"] = request.department
    if request.section is not None:
        update_data["section"] = request.section
    if request.year is not None:
        update_data["year"] = request.year
    if request.total_marks is not None:
        update_data["total_marks"] = request.total_marks
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Update paper
    result = await db.papers.update_one(
        {"_id": ObjectId(paper_id), "teacher_id": current_user["user_id"]},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return {"message": "Paper metadata updated successfully"}


@router.post("/approved-papers/{paper_id}/copy-for-edit")
async def create_paper_copy_for_edit(
    paper_id: str,
    current_user: dict = Depends(require_teacher)
):
    """Create a copy of an approved paper for editing (only user's own papers)"""
    db = get_database()
    
    # Get the approved paper - verify ownership
    approved_paper = await db.papers.find_one({
        "_id": ObjectId(paper_id),
        "status": "approved",
        "teacher_id": current_user["user_id"]  # Only user's own papers
    })
    
    if not approved_paper:
        raise HTTPException(status_code=404, detail="Approved paper not found or access denied")
    
    print(f"\n📋 Creating copy of approved paper: {paper_id}")
    print(f"   Subject: {approved_paper['subject']}")
    print(f"   Questions: {len(approved_paper.get('questions', []))}")
    print(f"   Total Marks: {approved_paper['total_marks']}")
    
    # Create a copy of the paper with status "pending" for editing
    paper_copy = {
        "teacher_id": current_user["user_id"],
        "subject": approved_paper["subject"],
        "department": approved_paper["department"],
        "section": approved_paper.get("section"),
        "year": approved_paper.get("year"),
        "exam_date": approved_paper.get("exam_date"),
        "total_marks": approved_paper["total_marks"],
        "questions": approved_paper.get("questions", []),
        "blooms_distribution": approved_paper.get("blooms_distribution", {}),
        "status": "pending",  # Copy starts as pending for editing
        "generation_prompt": approved_paper.get("generation_prompt", ""),
        "original_approved_paper_id": paper_id,  # Reference to original approved paper
        "is_edit_copy": True,  # Flag to indicate this is a copy for editing
        "regeneration_count": 0,
        "created_at": datetime.utcnow()
    }
    
    # Insert the copy
    result = await db.papers.insert_one(paper_copy)
    copy_paper_id = str(result.inserted_id)
    
    print(f"✅ Created paper copy: {copy_paper_id} (Original {paper_id} preserved)")
    
    return {
        "paper_id": copy_paper_id,
        "original_paper_id": paper_id,
        "message": "Paper copy created for editing. Original paper preserved."
    }
