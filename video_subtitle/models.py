# video_subtitle/models.py
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from django.conf import settings
import boto3

# session = boto3.Session(aws_access_key_id = settings.AWS_ACCESS_KEY_ID,aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY, region_name = settings.AWS_S3_REGION_NAME)
class BaseModel(Model):
    class Meta:
        table_name = 'SubtitlesTimeRange'
        region = settings.AWS_S3_REGION_NAME
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        # aws_session_token = session.get_credentials().token
        write_capacity_units = 10
        # Specifies the read capacity
        read_capacity_units = 10
class BaseModeUser(Model):
    class Meta:
        table_name = 'TokenVideoMapping'
        region = settings.AWS_S3_REGION_NAME
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        # aws_session_token = session.get_credentials().token
        write_capacity_units = 5
        # Specifies the read capacity
        read_capacity_units = 5

class SubtitlesTimeRange(BaseModel):
    video_name = UnicodeAttribute(hash_key=True)
    duration = UnicodeAttribute(range_key=True) 
    subtitle = UnicodeAttribute()
    user_token = UnicodeAttribute()

class TokenVideoMapping(BaseModeUser):
    user_token = UnicodeAttribute(hash_key=True)
    video_name = UnicodeAttribute(range_key=True)
    
