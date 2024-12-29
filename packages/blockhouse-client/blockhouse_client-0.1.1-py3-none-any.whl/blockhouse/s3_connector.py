from blockhouse.exceptions import BlockhouseError, S3UploadError
class S3Connector:
    def __init__(self):
        import boto3
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id='AKIAWJU4ZXZQATBAB26A',
            aws_secret_access_key='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',
            region_name='us-east-1'
        )

    def upload_file(self, file_name, bucket_name, object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            response = self.s3_client.upload_file(file_name, bucket_name, object_name)
            return response
        except Exception as e:
            raise S3UploadError(f"Failed to upload {file_name} to {bucket_name}: {str(e)}")

    def list_files(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            return [obj['Key'] for obj in response.get('Contents', [])]
        except Exception as e:
            raise BlockhouseError(f"Failed to list files in {bucket_name}: {str(e)}")