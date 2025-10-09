import boto3
import os
from typing import Dict, List, Optional
from botocore.exceptions import ClientError
import time

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.environ.get('S3_BUCKET_NAME')
        
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required")

    def upload_file(self, file_content: bytes, s3_key: str, 
                   original_filename: str, file_type: str) -> Dict:
        """Upload file to S3 with metadata"""
        try:
            # Upload file with metadata
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                Metadata={
                    'original_filename': original_filename,
                    'file_type': file_type,
                    'upload_time': str(int(time.time()))
                }
            )
            
            return {
                "success": True,
                "s3_key": s3_key,
                "original_filename": original_filename,
                "file_type": file_type
            }
        except ClientError as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_files(self, prefix: str) -> List[Dict]:
        """List files in S3 with metadata"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            for obj in response.get('Contents', []):
                # Get object metadata
                try:
                    metadata_response = self.s3_client.head_object(
                        Bucket=self.bucket_name,
                        Key=obj['Key']
                    )
                    metadata = metadata_response.get('Metadata', {})
                    
                    files.append({
                        "filename": obj['Key'],
                        "original_filename": metadata.get('original_filename', obj['Key']),
                        "size": obj['Size'],
                        "created": obj['LastModified'].timestamp(),
                        "type": metadata.get('file_type', 'unknown')
                    })
                except ClientError:
                    # Fallback if metadata can't be retrieved
                    files.append({
                        "filename": obj['Key'],
                        "original_filename": obj['Key'],
                        "size": obj['Size'],
                        "created": obj['LastModified'].timestamp(),
                        "type": 'unknown'
                    })
            
            return files
        except ClientError as e:
            raise Exception(f"Failed to list files: {str(e)}")

    def download_file(self, s3_key: str) -> bytes:
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Failed to download file: {str(e)}")

    def delete_file(self, s3_key: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete file: {str(e)}")
