# video_subtitle/models.py
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from django.conf import settings
import boto3

session = boto3.Session(aws_access_key_id = settings.AWS_ACCESS_KEY_ID,aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY, region_name = settings.AWS_S3_REGION_NAME)
class BaseModel(Model):
    class Meta:
        table_name = 'subtitles'
        region = settings.AWS_S3_REGION_NAME
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        aws_session_token = session.get_credentials().token
        write_capacity_units = 5
        # Specifies the read capacity
        read_capacity_units = 5

class SubtitlesTimeRange(BaseModel):
    keyword = UnicodeAttribute(hash_key=True)
    duration = UnicodeAttribute(range_key=True)  

    # @staticmethod
    # def create_table_if_not_exists():
    #     print("about to create============================")
    #     if not SubtitlesTimeRange.exists():

    #         SubtitlesTimeRange.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    #         print("table created==================================")