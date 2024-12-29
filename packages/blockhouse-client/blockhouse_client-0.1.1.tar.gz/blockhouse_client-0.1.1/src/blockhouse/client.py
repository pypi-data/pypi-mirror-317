from blockhouse.s3_connector import S3Connector
class BlockhouseClient:
    def __init__(self):
        self.s3_connector = S3Connector()

    def transfer_file(self, local_file_path, bucket_name):
        # Upload a file to an S3 bucket
        return self.s3_connector.upload_file(local_file_path, bucket_name)