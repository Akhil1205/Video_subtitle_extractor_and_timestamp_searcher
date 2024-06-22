import os,boto3,subprocess
from celery import shared_task
from django.conf import settings
from video_subtitle.models import SubtitlesTimeRange
# @shared_task
def process_video(video_path):
    try:
        print("------------------in celery---------------------------------")
        s3_client = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_S3_REGION_NAME)        
        s3_client.upload_file(video_path, settings.AWS_STORAGE_BUCKET_NAME, os.path.basename(video_path))
        subprocess.run([settings.CCEXTRACTOR_PATH,video_path, '-o', 'output1.srt'])
        with open("output1.srt", 'r') as file:
            lines = file.readlines()
        i = 0
        start_time = ""
        end_time = ""
        prev = ''
        while i < len(lines):
            if prev == '':
                prev = 'time'
                i+=1

            elif '-->' in lines[i]:
                # Capture start and end time
                start_end = lines[i].split(' --> ')
                start_time = start_end[0].strip()
                end_time = start_end[1].strip()
                i+=1
            else:
                # Capture entire block as keyword and add to subtitles list
                keyword_lines = ""
                while i < len(lines) and lines[i]!= '\n':
                    keyword_lines += lines[i].rstrip('\n')
                    keyword_lines = keyword_lines.strip() + ' '
                    i+=1
                prev = ''
                i+=1
                    
                if keyword_lines:
                    subtitle = SubtitlesTimeRange(keyword=keyword_lines,  duration= start_time + '-->' + end_time)
                    subtitle.save()
                i+=1

    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle extraction: {e}")
    except Exception as e:
        print(f"Error processing video: {e}")
    finally:
        # Cleanup: Delete the video and output files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists("output1.srt"):
            os.remove("output1.srt")