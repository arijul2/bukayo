from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import os
import aiofiles
from pathlib import Path
import uuid
from document_processor import DocumentProcessor
from job_matcher import JobMatcher
from s3_service import S3Service
from typing import Optional

app = FastAPI(title="JobMatch AI API", version="1.0.0")

# Add CORS middleware for React frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],        
)

# Initialize processors
doc_processor = DocumentProcessor()

# Initialize S3 service
s3_service = S3Service()

# Initialize job matcher (you'll need to set your OpenAI API key)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
if not OPENAI_API_KEY:
    # You can either set this as environment variable or hardcode it temporarily
    # For production, always use environment variables!
    OPENAI_API_KEY = "your-openai-api-key-here"  # REPLACE WITH YOUR ACTUAL KEY

job_matcher = JobMatcher(OPENAI_API_KEY)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a resume file to S3"""
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
    
    # Generate S3 key with UUID but store original filename in metadata
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_key = f"resumes/{unique_filename}"
    
    try:
        result = s3_service.upload_file(
            file_content=content,
            s3_key=s3_key,
            original_filename=file.filename,
            file_type="resume"
        )

        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {result['error']}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Resume uploaded successfully",
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_size": len(content),
                "s3_key": s3_key,
                "file_type": "resume"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

@app.post("/upload-job-description/")
async def upload_job_description(file: UploadFile = File(...)):
    """Upload a job description file to S3"""
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
    
    # Generate S3 key with UUID but store original filename in metadata
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_key = f"job_descriptions/{unique_filename}"
    
    try:
        result = s3_service.upload_file(
            file_content=content,
            s3_key=s3_key,
            original_filename=file.filename,
            file_type="job_description"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {result['error']}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Job description uploaded successfully",
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_size": len(content),
                "s3_key": s3_key,
                "file_type": "job_description"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

@app.post("/analyze-job-match/")
async def analyze_job_match(
    resume_filename: str = Form(...),
    job_filename: str = Form(...)
):
    """
    Analyze how well a resume matches a job description using AI
    
    Args:
        resume_filename: Filename of uploaded resume
        job_filename: Filename of uploaded job description
    """

    try:
        # Download files from S3
        resume_s3_key = resume_filename
        job_s3_key = job_filename
        
        resume_content = s3_service.download_file(resume_s3_key)
        job_content = s3_service.download_file(job_s3_key)
        
        # Save temporarily to process with document processor
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_filename).suffix) as temp_resume:
            temp_resume.write(resume_content)
            temp_resume_path = temp_resume.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(job_filename).suffix) as temp_job:
            temp_job.write(job_content)
            temp_job_path = temp_job.name
        
        try:
            # Extract text from both documents
            resume_data = doc_processor.process_resume(temp_resume_path)
            job_data = doc_processor.process_job_description(temp_job_path)
            
            resume_text = resume_data["raw_text"]
            job_text = job_data["raw_text"]
            
            # Perform AI analysis
            analysis_result = job_matcher.analyze_job_match(resume_text, job_text)
            
            # Add file metadata to response
            analysis_result.update({
                "resume_filename": resume_filename,
                "job_filename": job_filename,
                "resume_metadata": resume_data["metadata"],
                "job_metadata": job_data["metadata"]
            })
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Job match analysis completed successfully",
                    "analysis": analysis_result
                }
            )
            
        finally:
            # Clean up temporary files
            os.unlink(temp_resume_path)
            os.unlink(temp_job_path)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/generate-cover-letter/")
async def generate_cover_letter(
    resume_filename: str = Form(...),
    job_filename: str = Form(...)
):
    """
    Generate a personalized cover letter based on resume, job description, and analysis
    
    Args:
        resume_filename: Filename of uploaded resume
        job_filename: Filename of uploaded job description
        
    Returns:
        Generated cover letter with metadata
    """
    try:
        # Download files from S3
        resume_s3_key = resume_filename
        job_s3_key = job_filename
        
        resume_content = s3_service.download_file(resume_s3_key)
        job_content = s3_service.download_file(job_s3_key)
        
        # Save temporarily to process with document processor
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_filename).suffix) as temp_resume:
            temp_resume.write(resume_content)
            temp_resume_path = temp_resume.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(job_filename).suffix) as temp_job:
            temp_job.write(job_content)
            temp_job_path = temp_job.name
        
        try:
            # Extract text from both documents
            resume_data = doc_processor.process_resume(temp_resume_path)
            job_data = doc_processor.process_job_description(temp_job_path)
            
            resume_text = resume_data["raw_text"]
            job_text = job_data["raw_text"]
            
            # First perform analysis to get insights
            analysis_result = job_matcher.analyze_job_match(resume_text, job_text)
            
            # Generate cover letter using the analysis
            cover_letter_result = job_matcher.generate_cover_letter(resume_text, job_text, analysis_result)
            
            # Add file metadata to response
            cover_letter_result.update({
                "resume_filename": resume_filename,
                "job_filename": job_filename,
                "resume_metadata": resume_data["metadata"],
                "job_metadata": job_data["metadata"],
                "analysis_result": analysis_result
            })
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Cover letter generation completed successfully",
                    "result": cover_letter_result
                }
            )
            
        finally:
            # Clean up temporary files
            os.unlink(temp_resume_path)
            os.unlink(temp_job_path)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Cover letter generation failed: {str(e)}"
        )

@app.post("/process-document/{filename}")
async def process_document(filename: str, doc_type: str):
    """Test endpoint to process a document and extract text"""
    if doc_type == "resume":
        s3_key = f"resumes/{filename}"
        try:
            file_content = s3_service.download_file(s3_key)
            
            # Save temporarily to process with document processor
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                result = doc_processor.process_resume(temp_file_path)
                return JSONResponse(content={
                    "message": "Resume processed successfully",
                    "filename": filename,
                    "processing_result": result
                })
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Resume file not found: {str(e)}")
    
    elif doc_type == "job_description":
        s3_key = f"job_descriptions/{filename}"
        try:
            file_content = s3_service.download_file(s3_key)
            
            # Save temporarily to process with document processor
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                result = doc_processor.process_job_description(temp_file_path)
                return JSONResponse(content={
                    "message": "Job description processed successfully",
                    "filename": filename,
                    "processing_result": result
                })
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Job description file not found: {str(e)}")
    
    else:
        raise HTTPException(status_code=400, detail="doc_type must be 'resume' or 'job_description'")

@app.get("/")
async def root():
    return {
        "message": "JobMatch AI - Resume and Job Description Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "upload_resume": "/upload-resume/",
            "upload_job": "/upload-job-description/",
            "analyze_match": "/analyze-job-match/",
            "generate_cover_letter": "/generate-cover-letter/",
            "docs": "/docs"
        }
    }

@app.get("/resumes/")
async def list_resumes():
    """List all uploaded resume files from S3"""
    try:
        files = s3_service.list_files("resumes/")
        return {"resumes": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@app.get("/job-descriptions/")
async def list_job_descriptions():
    """List all uploaded job description files from S3"""
    try:
        files = s3_service.list_files("job_descriptions/")
        return {"job_descriptions": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

@app.get("/download-resume/{filename}")
async def download_resume(filename: str):
    """Download a specific resume file from S3"""
    s3_key = f"resumes/{filename}"
    try:
        file_content = s3_service.download_file(s3_key)
        return Response(
            content=file_content,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")

@app.get("/download-job-description/{filename}")
async def download_job_description(filename: str):
    """Download a specific job description file from S3"""
    s3_key = f"job_descriptions/{filename}"
    try:
        file_content = s3_service.download_file(s3_key)
        return Response(
            content=file_content,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)