from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import aiofiles
from pathlib import Path
import uuid

app = FastAPI()

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directories if they don't exist
RESUME_UPLOAD_DIR = Path("uploads/resumes")
JOB_UPLOAD_DIR = Path("uploads/job_descriptions")
RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
JOB_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a resume file (PDF, DOC, DOCX, or TXT)"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = RESUME_UPLOAD_DIR / unique_filename
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Resume uploaded successfully",
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_size": len(content),
                "file_path": str(file_path),
                "file_type": "resume"
            }
        )
    
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

@app.post("/upload-job-description/")
async def upload_job_description(file: UploadFile = File(...)):
    """Upload a job description file (PDF, DOC, DOCX, or TXT)"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = JOB_UPLOAD_DIR / unique_filename
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Job description uploaded successfully",
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_size": len(content),
                "file_path": str(file_path),
                "file_type": "job_description"
            }
        )
    
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

@app.get("/")
async def root():
    return {"message": "JobMatch AI - Resume and Job Description Upload API"}

@app.get("/resumes/")
async def list_resumes():
    """List all uploaded resume files"""
    try:
        files = []
        for file_path in RESUME_UPLOAD_DIR.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "created": file_path.stat().st_ctime,
                    "type": "resume"
                })
        return {"resumes": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@app.get("/job-descriptions/")
async def list_job_descriptions():
    """List all uploaded job description files"""
    try:
        files = []
        for file_path in JOB_UPLOAD_DIR.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "created": file_path.stat().st_ctime,
                    "type": "job_description"
                })
        return {"job_descriptions": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@app.get("/download-resume/{filename}")
async def download_resume(filename: str):
    """Download a specific resume file"""
    file_path = RESUME_UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/download-job-description/{filename}")
async def download_job_description(filename: str):
    """Download a specific job description file"""
    file_path = JOB_UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)