# Medical Imaging Backend

A professional Node.js/Express backend for medical imaging management with DICOM support.

## Features

- **Patient Management**: Complete CRUD operations with medical history
- **Doctor Management**: Staff management with specialties and schedules
- **Study Management**: Medical studies with DICOM metadata
- **Image Management**: Upload, view, and annotate medical images
- **Authentication**: JWT-based auth with role-based access control
- **File Upload**: Secure DICOM file upload with thumbnail generation
- **Search**: Full-text search for patients and doctors
- **Reports**: Study reporting system

## Database Relationships

```
Patient (1) -----> (N) Study
Doctor (1) -----> (N) Study
Study (1) -----> (N) Image
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Patients
- `POST /api/patients` - Create patient
- `GET /api/patients` - Get all patients (with search)
- `GET /api/patients/:patientId` - Get patient with studies
- `PUT /api/patients/:patientId` - Update patient
- `DELETE /api/patients/:patientId` - Delete patient
- `GET /api/patients/search?q=query` - Search patients

### Doctors
- `POST /api/doctors` - Create doctor
- `GET /api/doctors` - Get all doctors (with search)
- `GET /api/doctors/:doctorId` - Get doctor with studies
- `PUT /api/doctors/:doctorId` - Update doctor
- `DELETE /api/doctors/:doctorId` - Delete doctor
- `GET /api/doctors/search?q=query` - Search doctors

### Studies
- `POST /api/studies` - Create study
- `GET /api/studies` - Get all studies (with filters)
- `GET /api/studies/:studyId` - Get study details
- `GET /api/studies/:studyId/full` - Get full study with images
- `PUT /api/studies/:studyId` - Update study
- `DELETE /api/studies/:studyId` - Delete study
- `POST /api/studies/:studyId/report` - Add study report
- `GET /api/studies/:studyId/report` - Get study report

### Images
- `POST /api/images/studies/:studyId/images` - Upload images
- `GET /api/images/studies/:studyId/images` - Get study images
- `GET /api/images/:imageId` - Get image details
- `GET /api/images/files/:fileId` - Get image file
- `GET /api/images/:imageId/thumbnail` - Get thumbnail
- `DELETE /api/images/:imageId` - Delete image
- `POST /api/images/:imageId/annotations` - Add annotation

## Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start MongoDB (required)

4. Run the application:
```bash
# Development
npm run dev

# Production
npm start
```

## Environment Variables

- `MONGODB_URI` - MongoDB connection string
- `JWT_SECRET` - JWT secret key
- `PORT` - Server port (default: 5000)
- `NODE_ENV` - Environment (development/production)
- `FRONTEND_URL` - Frontend URL for CORS

## File Structure

```
backend/
├── controllers/
│   ├── patients.controller.js
│   ├── doctors.controller.js
│   ├── studies.controller.js
│   ├── images.controller.js
│   └── auth.controller.js
├── routes/
│   ├── patients.routes.js
│   ├── doctors.routes.js
│   ├── studies.routes.js
│   ├── images.routes.js
│   └── auth.routes.js
├── models/
│   ├── patient.model.js
│   ├── doctor.model.js
│   ├── study.model.js
│   ├── image.model.js
│   └── user.model.js
├── middleware/
│   ├── auth.js
│   └── upload.js
├── uploads/           # File uploads
├── app.js            # Main application file
├── package.json      # Dependencies
└── .env.example      # Environment template
```

## Security Features

- JWT authentication with expiration
- Password hashing with bcrypt
- Rate limiting
- CORS protection
- File type validation
- Request size limits
- Helmet.js security headers

## Example Response

```json
{
  "id": "study_001",
  "patient": {
    "id": "pat_001",
    "firstName": "Emma",
    "lastName": "Dubois"
  },
  "doctor": {
    "id": "doc_001",
    "firstName": "Jean",
    "lastName": "Martin",
    "specialty": "Radiology"
  },
  "modality": "MRI",
  "bodyPart": "Brain",
  "status": "completed",
  "images": [
    {
      "id": "img_001",
      "sequenceType": "T1",
      "fileUrl": "https://api.example.com/files/mri/img_001.dcm"
    }
  ]
}
```
