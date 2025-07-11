# 🔗 **JawBreak APIs - Complete Endpoint Documentation**

## 🌐 **Base URL**
```
https://your-app-name.railway.app
```

---

## 🏠 **Home & Documentation**

### **GET /**
- **Description**: API Documentation Homepage
- **Response**: HTML page with all available endpoints
- **Access**: Public

### **GET /health/**
- **Description**: Health check endpoint
- **Response**: JSON with service status
- **Access**: Public
- **Example Response**:
```json
{
  "status": "healthy",
  "version": "1.0",
  "services": {
    "authentication": "active",
    "patients": "active",
    "visits": "active",
    "oasis": "active",
    "files": "active",
    "communication": "active"
  }
}
```

---

## 🔐 **Authentication Endpoints**
*Base: `/api/v1/auth/`*

### **POST /api/v1/auth/login/**
- **Description**: User login
- **Body**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
- **Response**: JWT tokens + user info

### **POST /api/v1/auth/register/**
- **Description**: User registration
- **Body**:
```json
{
  "username": "new_user",
  "email": "user@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

### **POST /api/v1/auth/logout/**
- **Description**: User logout
- **Auth**: Required

### **POST /api/v1/auth/token/refresh/**
- **Description**: Refresh JWT token
- **Body**:
```json
{
  "refresh": "your_refresh_token"
}
```

### **GET /api/v1/auth/profile/**
- **Description**: Get user profile
- **Auth**: Required

### **PUT /api/v1/auth/profile/update/**
- **Description**: Update user profile
- **Auth**: Required

### **POST /api/v1/auth/change-password/**
- **Description**: Change user password
- **Auth**: Required

### **GET /api/v1/auth/roles/**
- **Description**: List user roles
- **Auth**: Required

### **GET /api/v1/auth/permissions/**
- **Description**: List user permissions
- **Auth**: Required

### **POST /api/v1/auth/users/{user_id}/assign-role/**
- **Description**: Assign role to user
- **Auth**: Admin required

---

## 👥 **Patient Management**
*Base: `/api/v1/patients/`*

### **Core Patient Operations**
- **GET /api/v1/patients/** - List all patients
- **POST /api/v1/patients/** - Create new patient
- **GET /api/v1/patients/{id}/** - Get specific patient
- **PUT /api/v1/patients/{id}/** - Update patient
- **DELETE /api/v1/patients/{id}/** - Delete patient

### **Patient Search**
- **GET /api/v1/patients/search/** - General search
- **GET /api/v1/patients/search/by-name/** - Search by name
- **GET /api/v1/patients/search/by-dob/** - Search by date of birth
- **GET /api/v1/patients/search/by-mrn/** - Search by medical record number
- **GET /api/v1/patients/search/advanced/** - Advanced search

### **Patient-Specific Data**
- **GET /api/v1/patients/{id}/history/** - Patient history
- **GET /api/v1/patients/{id}/visits/** - Patient visits
- **GET /api/v1/patients/{id}/assessments/** - Patient assessments
- **GET /api/v1/patients/{id}/medications/** - Patient medications
- **GET /api/v1/patients/{id}/allergies/** - Patient allergies
- **GET /api/v1/patients/{id}/vitals/** - Patient vitals
- **GET /api/v1/patients/{id}/care-plan/** - Patient care plan
- **GET /api/v1/patients/{id}/demographics/** - Patient demographics

---

## 🏥 **Visit Management**
*Base: `/api/v1/visits/`*

### **Core Visit Operations**
- **GET /api/v1/visits/** - List all visits
- **POST /api/v1/visits/** - Create new visit
- **GET /api/v1/visits/{id}/** - Get specific visit
- **PUT /api/v1/visits/{id}/** - Update visit
- **DELETE /api/v1/visits/{id}/** - Delete visit

### **Visit Notes & Documentation**
- **GET/POST /api/v1/visits/{visit_id}/notes/** - Visit notes
- **GET/PUT/DELETE /api/v1/visits/{visit_id}/notes/{note_id}/** - Specific note
- **GET/POST /api/v1/visits/{visit_id}/structured-notes/** - Structured notes
- **GET/POST /api/v1/visits/{visit_id}/unstructured-notes/** - Unstructured notes

### **AI-Powered Features**
- **GET /api/v1/visits/{visit_id}/summary/** - AI visit summary
- **POST /api/v1/visits/{visit_id}/ai-documentation/** - AI documentation
- **POST /api/v1/visits/{visit_id}/transcript-to-note/** - Convert transcript to note
- **POST /api/v1/visits/{visit_id}/voice-to-text/** - Voice to text conversion

### **Templates**
- **GET /api/v1/visits/{visit_id}/template/** - Visit template
- **GET /api/v1/visits/templates/{discipline}/** - Discipline template
- **GET /api/v1/visits/templates/{discipline}/{visit_type}/** - Specific template

---

## 📁 **File Management & OCR**
*Base: `/api/v1/files/`*

### **File Upload**
- **POST /api/v1/files/upload/** - Upload single file
- **POST /api/v1/files/upload/multiple/** - Upload multiple files
- **POST /api/v1/files/upload/patient/{patient_id}/** - Upload patient file
- **POST /api/v1/files/upload/visit/{visit_id}/** - Upload visit file

### **OCR Processing**
- **POST /api/v1/files/ocr/** - OCR processing
- **POST /api/v1/files/ocr/batch/** - Batch OCR processing
- **POST /api/v1/files/documents/{document_id}/ocr/** - Document OCR
- **POST /api/v1/files/ocr/lab-results/** - Lab results OCR
- **POST /api/v1/files/ocr/forms/** - Forms OCR

### **AI Data Extraction**
- **POST /api/v1/files/extract-data/** - Extract data from files
- **POST /api/v1/files/documents/{document_id}/extract/** - Extract from specific document
- **POST /api/v1/files/extract/structured-data/** - Extract structured data
- **POST /api/v1/files/auto-insert-ehr/** - Auto-insert into EHR

### **Document Management**
- **GET /api/v1/files/documents/{document_id}/** - Get document details
- **GET /api/v1/files/documents/{document_id}/download/** - Download document

---

## 📋 **OASIS & Forms**
*Base: `/api/v1/oasis/`*

### **OASIS Operations**
- **GET /api/v1/oasis/** - List OASIS assessments
- **POST /api/v1/oasis/** - Create OASIS assessment
- **GET /api/v1/oasis/{id}/** - Get specific assessment
- **PUT /api/v1/oasis/{id}/** - Update assessment
- **DELETE /api/v1/oasis/{id}/** - Delete assessment

### **OASIS Specific**
- **POST /api/v1/oasis/submit/** - Submit OASIS form
- **GET /api/v1/oasis/template/{discipline}/** - Get discipline template

---

## 💬 **Communication**
*Base: `/api/v1/communication/`*

### **Communication Operations**
- **GET /api/v1/communication/** - List communications
- **POST /api/v1/communication/** - Create communication
- **GET /api/v1/communication/{id}/** - Get specific communication
- **PUT /api/v1/communication/{id}/** - Update communication
- **DELETE /api/v1/communication/{id}/** - Delete communication

### **Communication Specific**
- **POST /api/v1/communication/send-note/** - Send message/note
- **GET /api/v1/communication/threads/{patient_id}/** - Patient communication threads

---

## 🔧 **Admin Panel**
- **GET /admin/** - Django admin interface
- **Auth**: Admin credentials required

---

## 📝 **Request Examples**

### **Create Patient**
```bash
curl -X POST https://your-app-name.railway.app/api/v1/patients/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-01-01",
    "email": "john.doe@example.com"
  }'
```

### **Upload File**
```bash
curl -X POST https://your-app-name.railway.app/api/v1/files/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "patient_id=1"
```

### **OCR Processing**
```bash
curl -X POST https://your-app-name.railway.app/api/v1/files/ocr/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": 1,
    "extract_type": "lab_results"
  }'
```

---

## 🎯 **Testing Checklist**

### **Authentication Flow**
- [ ] Register user
- [ ] Login user
- [ ] Get profile
- [ ] Refresh token
- [ ] Change password

### **Patient Management**
- [ ] Create patient
- [ ] List patients
- [ ] Search patients
- [ ] Get patient details
- [ ] Update patient
- [ ] Get patient history

### **Visit Management**
- [ ] Create visit
- [ ] Add visit notes
- [ ] Generate AI summary
- [ ] Get visit templates

### **File Management**
- [ ] Upload file
- [ ] Process OCR
- [ ] Extract data
- [ ] Download file

### **Communication**
- [ ] Send message
- [ ] Get communication threads
- [ ] List communications

---

## 🚀 **Quick Start Testing**

1. **Deploy your APIs** using Railway
2. **Register a test user**:
   ```
   POST /api/v1/auth/register/
   ```
3. **Login to get token**:
   ```
   POST /api/v1/auth/login/
   ```
4. **Test protected endpoints** with the token
5. **Create test data** (patients, visits, etc.)

**🎉 Your Healthcare Management APIs are now ready to serve patients worldwide!**
