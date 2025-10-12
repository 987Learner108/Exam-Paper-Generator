from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from typing import List


class MailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USER,
            MAIL_PASSWORD=settings.EMAIL_PASS,
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fm = FastMail(self.conf)
    
    async def send_welcome_email(self, email: str, full_name: str, password: str):
        """Send welcome email with login credentials"""
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0066cc;">Welcome to Intelligent Exam Paper Generator</h2>
                <p>Dear {full_name},</p>
                <p>Your account has been created successfully. Here are your login credentials:</p>
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Password:</strong> {password}</p>
                </div>
                <p>Please login at: <a href="{settings.FRONTEND_URL}">{settings.FRONTEND_URL}</a></p>
                <p>For security reasons, please change your password after first login.</p>
                <br>
                <p>Best regards,<br>Exam Generator Team</p>
            </body>
        </html>
        """
        
        message = MessageSchema(
            subject="Welcome to Exam Paper Generator",
            recipients=[email],
            body=html,
            subtype="html"
        )
        
        await self.fm.send_message(message)
    
    async def send_password_reset(self, email: str, full_name: str, new_password: str):
        """Send password reset email"""
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0066cc;">Password Reset</h2>
                <p>Dear {full_name},</p>
                <p>Your password has been reset. Here is your new password:</p>
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>New Password:</strong> {new_password}</p>
                </div>
                <p>Please login at: <a href="{settings.FRONTEND_URL}">{settings.FRONTEND_URL}</a></p>
                <p>For security reasons, please change your password after login.</p>
                <br>
                <p>Best regards,<br>Exam Generator Team</p>
            </body>
        </html>
        """
        
        message = MessageSchema(
            subject="Password Reset - Exam Paper Generator",
            recipients=[email],
            body=html,
            subtype="html"
        )
        
        await self.fm.send_message(message)
    
    async def send_paper_generated_notification(self, email: str, full_name: str, subject: str, paper_id: str):
        """Send notification when paper is generated"""
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0066cc;">Exam Paper Generated Successfully</h2>
                <p>Dear {full_name},</p>
                <p>Your exam paper for <strong>{subject}</strong> has been generated successfully.</p>
                <p>Paper ID: <strong>{paper_id}</strong></p>
                <p>Please login to review and approve the paper.</p>
                <p><a href="{settings.FRONTEND_URL}/verify-paper/{paper_id}" style="background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px;">Review Paper</a></p>
                <br>
                <p>Best regards,<br>Exam Generator Team</p>
            </body>
        </html>
        """
        
        message = MessageSchema(
            subject=f"Exam Paper Generated - {subject}",
            recipients=[email],
            body=html,
            subtype="html"
        )
        
        await self.fm.send_message(message)
    
    async def send_password_reset_link(self, email: str, full_name: str, reset_token: str):
        """Send password reset link"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #0066cc;">Password Reset Request</h2>
                <p>Dear {full_name},</p>
                <p>We received a request to reset your password. Click the button below to reset it:</p>
                <p><a href="{reset_url}" style="background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0;">Reset Password</a></p>
                <p>This link will expire in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
                <br>
                <p>Best regards,<br>Exam Generator Team</p>
            </body>
        </html>
        """
        
        message = MessageSchema(
            subject="Password Reset Request - Exam Paper Generator",
            recipients=[email],
            body=html,
            subtype="html"
        )
        
        await self.fm.send_message(message)


mail_service = MailService()
