import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL ||
  (import.meta.env.MODE === 'production'
    ? 'https://exam-generator-backend.onrender.com'
    : 'http://localhost:8000')

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  getCurrentUser: () => api.get('/auth/me'),
}

// Admin API
export const adminAPI = {
  createUser: (data) => api.post('/admin/users', data),
  listUsers: () => api.get('/admin/users'),
  updateUser: (userId, data) => api.patch(`/admin/users/${userId}`, data),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
  resetPassword: (email) => api.post('/admin/users/reset-password', { email }),
  getAnalytics: () => api.get('/admin/analytics'),
}

// Teacher API
export const teacherAPI = {
  uploadResource: (formData) => api.post('/teacher/upload-resource', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  listResources: () => api.get('/teacher/resources'),
  deleteResource: (resourceId) => api.delete(`/teacher/resources/${resourceId}`),
  getSubjectsAndDepartments: () => api.get('/teacher/subjects-departments'),
  generatePaper: (data) => api.post('/teacher/generate-paper', data),
  listPapers: () => api.get('/teacher/papers'),
  getPaper: (paperId) => api.get(`/teacher/papers/${paperId}`),
  approvePaper: (paperId) => api.post('/teacher/approve-paper', { paper_id: paperId }),
  regeneratePaper: (paperId, feedbackPrompt) => api.post('/teacher/regenerate-paper', { 
    paper_id: paperId, 
    feedback_prompt: feedbackPrompt 
  }),
  downloadPDF: (fileId) => api.get(`/teacher/download-pdf/${fileId}`, {
    responseType: 'blob',
  }),
  getHistory: () => api.get('/teacher/history'),
  deleteHistoryItem: (historyId) => api.delete(`/teacher/history/${historyId}`),
  clearAllHistory: () => api.delete('/teacher/history'),
  updatePaperMetadata: (paperId, data) => api.patch(`/teacher/papers/${paperId}/metadata`, data),
  
  // Approved Papers Management
  searchApprovedPapers: (subject, department) => {
    const params = new URLSearchParams()
    if (subject) params.append('subject', subject)
    if (department) params.append('department', department)
    return api.get(`/teacher/approved-papers?${params.toString()}`)
  },
  getApprovedPaperDetails: (paperId) => api.get(`/teacher/approved-papers/${paperId}`),
  deleteApprovedPaper: (paperId) => api.delete(`/teacher/approved-papers/${paperId}`),
  createPaperCopyForEdit: (paperId) => api.post(`/teacher/approved-papers/${paperId}/copy-for-edit`),
}

export default api
