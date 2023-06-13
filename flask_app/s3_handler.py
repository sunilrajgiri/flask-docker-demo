from werkzeug.utils import secure_filename
import boto3, botocore
from aws_creds import S3_CREDS


class S3Handler:

    def build_s3_connection(self):
        s3 = boto3.client(
                "s3",
                aws_access_key_id=S3_CREDS['AWS_S3_ACCESS_KEY_ID'],
                aws_secret_access_key=S3_CREDS['AWS_S3_SECRET_ACCESS_KEY']
            )
        return s3

    def upload_file_to_s3(self, file_, acl="public-read"):
        filename = secure_filename(file_.filename)
        s3 = self.build_s3_connection()
        try:
            s3.upload_fileobj(
                file,
                S3_CREDS["AWS_BUCKET_NAME"],
                filename,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file_.content_type
                }
            )

        except Exception as e:
            # This is a catch all exception, edit this part to fit your needs.
            print("Something Happened: ", e)
            return e
    
        # after upload file to s3 bucket, return filename of the uploaded file
        return filename

