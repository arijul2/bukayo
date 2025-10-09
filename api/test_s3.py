import os
from s3_service import S3Service

def test_s3_connection():
    """Test S3 connection and basic operations"""
    print("🧪 Testing S3 Connection...")
    
    try:
        # Initialize S3 service
        s3_service = S3Service()
        print("✅ S3 service initialized successfully")
        
        # Test listing files in resumes folder
        print("\n📁 Testing resumes folder...")
        resume_files = s3_service.list_files("resumes/")
        print(f"✅ Found {len(resume_files)} files in resumes/")
        for file in resume_files[:3]:  # Show first 3 files
            print(f"   - {file['original_filename']} ({file['size']} bytes)")
        
        # Test listing files in job_descriptions folder
        print("\n📁 Testing job_descriptions folder...")
        job_files = s3_service.list_files("job_descriptions/")
        print(f"✅ Found {len(job_files)} files in job_descriptions/")
        for file in job_files[:3]:  # Show first 3 files
            print(f"   - {file['original_filename']} ({file['size']} bytes)")
        
        # Test uploading a small test file
        print("\n📤 Testing file upload...")
        test_content = b"This is a test file for S3 integration"
        test_result = s3_service.upload_file(
            file_content=test_content,
            s3_key="test/test_file.txt",
            original_filename="test_file.txt",
            file_type="test"
        )
        
        if test_result["success"]:
            print("✅ Test file uploaded successfully")
            
            # Test downloading the file back
            print("📥 Testing file download...")
            downloaded_content = s3_service.download_file("test/test_file.txt")
            if downloaded_content == test_content:
                print("✅ Test file downloaded successfully")
            else:
                print("❌ Downloaded content doesn't match original")
            
            # Clean up test file
            print("🧹 Cleaning up test file...")
            s3_service.delete_file("test/test_file.txt")
            print("✅ Test file deleted successfully")
        else:
            print(f"❌ Test file upload failed: {test_result['error']}")
        
        print("\n🎉 All S3 tests passed! Your S3 integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ S3 connection failed: {e}")
        print("\n💡 Make sure you have set these environment variables:")
        print("   - AWS_ACCESS_KEY_ID")
        print("   - AWS_SECRET_ACCESS_KEY") 
        print("   - AWS_REGION")
        print("   - S3_BUCKET_NAME")
        return False

if __name__ == "__main__":
    test_s3_connection()
