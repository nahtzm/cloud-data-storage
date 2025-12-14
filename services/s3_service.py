import os
import uuid

import boto3


def create_s3_client():
    return boto3.client(
        "s3",
        region_name="us-east-1",
    )


s3 = create_s3_client()


def upload_file_to_s3(file, user_id, bucket):
    ext = os.path.splitext(file.filename)[1]
    s3_key = f"user_{user_id}/{uuid.uuid4()}{ext}"

    s3.upload_fileobj(file, bucket, s3_key)

    return s3_key


def generate_presigned_download(file, bucket, s3_key, expire=60):
    return s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': s3_key,
            'ResponseContentDisposition':
                f'attachment; filename="{file.filename}"'
        },
        ExpiresIn=expire
    )


def delete_s3_object(bucket, s3_key):
    s3.delete_object(
        Bucket=bucket,
        Key=s3_key
    )
