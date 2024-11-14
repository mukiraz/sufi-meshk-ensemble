import os
import boto3
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Upload all files in static/css to the S3 bucket, maintaining the 'static/css' folder structure."

    def handle(self, *args, **options):
        # Path to the local static/css directory
        css_directory = os.path.join(settings.BASE_DIR, 'static', 'css')
        
        # Check if the directory exists
        if not os.path.isdir(css_directory):
            self.stdout.write(self.style.ERROR("Directory static/css not found."))
            return
        
        # Upload each file in the directory
        for root, dirs, files in os.walk(css_directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.upload_to_s3(file_path, css_directory)

        self.stdout.write(self.style.SUCCESS("All CSS files uploaded to S3 successfully!"))

    def upload_to_s3(self, file_path, base_directory):
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Define bucket name and S3 key, preserving 'static/css' structure
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        relative_path = os.path.relpath(file_path, base_directory)
        s3_key = f'static/css/{relative_path.replace(os.sep, "/")}'

        # Upload the file, overwrite if exists
        s3_client.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=s3_key,
            ExtraArgs={
                'ContentType': 'text/css' if file_path.endswith('.css') else 'application/json',
                'CacheControl': 'max-age=0, no-cache, no-store, must-revalidate'
            }
        )
