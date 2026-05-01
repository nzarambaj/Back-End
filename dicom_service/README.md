# DICOM Service

Clean DICOM processing service without authentication requirements.

## Features

- DICOM file upload and processing
- Metadata extraction
- Image rendering and thumbnails
- Image enhancement (contrast, brightness, sharpness)
- File management and statistics
- No authentication required

## API Endpoints

### Health Check
```
GET /api/dicom/health
```

### File Operations
```
POST /api/dicom/upload          # Upload DICOM file
GET  /api/dicom/files           # List all files
DELETE /api/dicom/delete/:id   # Delete file
```

### Image Operations
```
GET  /api/dicom/image/:id       # Get processed image
GET  /api/dicom/thumbnail/:id   # Get thumbnail
POST /api/dicom/enhance/:id     # Enhance image
```

### Data Operations
```
GET  /api/dicom/metadata/:id    # Get metadata
GET  /api/dicom/statistics/:id  # Get statistics
```

## Installation

```bash
cd dicom_service
npm install
npm start
```

## Usage

1. Upload DICOM files via POST to `/api/dicom/upload`
2. View metadata via GET to `/api/dicom/metadata/:filename`
3. Get processed images via GET to `/api/dicom/image/:filename`
4. Enhance images via POST to `/api/dicom/enhance/:filename`

## Supported Formats

- .dcm
- .dicom
- .dic
- .ima
