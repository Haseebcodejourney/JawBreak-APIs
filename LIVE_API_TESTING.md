# 🧪 **LIVE API TESTING GUIDE**

## 🚀 **First: Deploy Your APIs**

Follow the **FASTEST_DEPLOY.md** guide to get your APIs live in 3 minutes:
1. Go to [https://railway.app](https://railway.app)
2. Deploy your GitHub repository
3. Set environment variables
4. Get your live URL

---

## 🔗 **Your Live API Base URL**

Once deployed, your APIs will be available at:
```
https://your-app-name.railway.app
```

*Replace `your-app-name` with your actual Railway app name*

---

## 🧪 **Test Your Live APIs**

### **Method 1: Browser Testing (Easiest)**

Open these URLs in your browser:

#### **1. Health Check**
```
https://your-app-name.railway.app/health/
```
*Should return: Server status and database connection*

#### **2. API Documentation**
```
https://your-app-name.railway.app/
```
*Should show: API documentation and available endpoints*

#### **3. Authentication Endpoints**
```
https://your-app-name.railway.app/api/v1/auth/
```
*Should show: Login, register, and authentication options*

---

### **Method 2: Postman Testing (Recommended)**

Download Postman: [https://www.postman.com/downloads/](https://www.postman.com/downloads/)

#### **Test Collection:**

**1. Health Check**
```
GET https://your-app-name.railway.app/health/
```

**2. User Registration**
```
POST https://your-app-name.railway.app/api/v1/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "first_name": "Test",
  "last_name": "User"
}
```

**3. User Login**
```
POST https://your-app-name.railway.app/api/v1/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpass123"
}
```

**4. Get Patients (Protected)**
```
GET https://your-app-name.railway.app/api/v1/patients/
Authorization: Bearer YOUR_TOKEN_HERE
```

---

### **Method 3: Command Line Testing**

**1. Health Check**
```bash
curl https://your-app-name.railway.app/health/
```

**2. Register User**
```bash
curl -X POST https://your-app-name.railway.app/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**3. Login User**
```bash
curl -X POST https://your-app-name.railway.app/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

---

## 📍 **All Your Live API Endpoints**

Replace `your-app-name` with your actual app name:

### **Authentication**
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login user
- `POST /api/v1/auth/logout/` - Logout user
- `GET /api/v1/auth/profile/` - Get user profile

### **Patients**
- `GET /api/v1/patients/` - List all patients
- `POST /api/v1/patients/` - Create new patient
- `GET /api/v1/patients/{id}/` - Get specific patient
- `PUT /api/v1/patients/{id}/` - Update patient
- `DELETE /api/v1/patients/{id}/` - Delete patient

### **Visits**
- `GET /api/v1/visits/` - List all visits
- `POST /api/v1/visits/` - Create new visit
- `GET /api/v1/visits/{id}/` - Get specific visit
- `PUT /api/v1/visits/{id}/` - Update visit
- `DELETE /api/v1/visits/{id}/` - Delete visit

### **File Management**
- `POST /api/v1/files/upload/` - Upload file
- `GET /api/v1/files/` - List files
- `GET /api/v1/files/{id}/` - Get specific file
- `DELETE /api/v1/files/{id}/` - Delete file

### **OASIS**
- `GET /api/v1/oasis/` - List OASIS assessments
- `POST /api/v1/oasis/` - Create OASIS assessment
- `GET /api/v1/oasis/{id}/` - Get specific assessment
- `PUT /api/v1/oasis/{id}/` - Update assessment

### **Communication**
- `GET /api/v1/communication/` - List communications
- `POST /api/v1/communication/` - Create communication
- `GET /api/v1/communication/{id}/` - Get specific communication

---

## ✅ **Testing Checklist**

After deployment, test these in order:

- [ ] **Health Check** - Verify server is running
- [ ] **API Documentation** - Check if docs are accessible
- [ ] **User Registration** - Create test user
- [ ] **User Login** - Get authentication token
- [ ] **Protected Endpoints** - Test with auth token
- [ ] **CRUD Operations** - Create, Read, Update, Delete
- [ ] **File Upload** - Test file functionality
- [ ] **Database Operations** - Verify data persistence

---

## 🔍 **Expected Responses**

### **Successful Health Check**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-07-12T10:30:00Z"
}
```

### **Successful Login**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

---

## 🎉 **Your APIs Are Live and Ready!**

Once you see successful responses, your Healthcare Management APIs are serving patients worldwide! 🌍

**Share your live API URL with your team and start building amazing healthcare applications!**
