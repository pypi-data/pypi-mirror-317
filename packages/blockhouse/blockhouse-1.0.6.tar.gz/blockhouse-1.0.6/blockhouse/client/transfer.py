from blockhouse.client.s3_connector import S3Connector
class Transfer:
    def __init__(self):
        self.s3_connector = S3Connector()

    def send_file(self, local_file_path, bucket_name):
        # Upload a file to an S3 bucket
        return self.s3_connector.upload_file(local_file_path, bucket_name)