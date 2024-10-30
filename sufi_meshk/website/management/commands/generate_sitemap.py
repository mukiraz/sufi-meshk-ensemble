import os
import boto3
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from website.sitemaps import sitemaps

class Command(BaseCommand):
    help = "Generate sitemap.xml and upload it to the S3 bucket."

    def handle(self, *args, **options):
        # Generate sitemap content
        sitemap_content = render_to_string('sitemap_template.xml', {
            'sitemaps': sitemaps
        })

        
        # Save to local static directory
        sitemap_path = os.path.join(settings.BASE_DIR, 'static', 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        # Upload to S3
        self.upload_to_s3(sitemap_content)

        self.stdout.write(self.style.SUCCESS('Sitemap.xml created and uploaded to S3 successfully!'))

    def upload_to_s3(self, content):
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Define bucket name and key (file name in S3)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3_key = 'static/sitemap.xml'  # S3'te 'static/' klasörüne kaydediyoruz

        # Upload the content as a file
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=content,
            ContentType='application/xml',
            CacheControl=settings.AWS_S3_OBJECT_PARAMETERS['CacheControl']
        )