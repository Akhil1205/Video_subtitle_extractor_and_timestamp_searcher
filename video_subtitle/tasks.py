import os,boto3,subprocess
from celery import shared_task
from django.conf import settings
from video_subtitle.models import SubtitlesTimeRange, TokenVideoMapping
from django.conf import settings
from pynamodb.exceptions import PutError

@shared_task
def process_video(video_path, token):
    try:
        import pdb; pdb.set_trace()
        s3_client = boto3.client('s3',region_name=settings.AWS_S3_REGION_NAME)        
        s3_client.upload_file(video_path, settings.AWS_STORAGE_BUCKET_NAME, os.path.basename(video_path))
        subprocess.run([settings.CCEXTRACTOR_PATH,video_path, '-o', 'output1.srt'])
        with open("output1.srt", 'r') as file:
            lines = file.readlines()
        i = 0
        duration = ""
        prev = ''
        subtitles_bulk_update_list=[]
        video_name  = ""
        for user_video in TokenVideoMapping.query(token):
            video_name = user_video.video_name
        while i < len(lines):
            if prev == '':
                prev = 'time'
                i+=1
            elif '-->' in lines[i]:
                duration = lines[i]
                i+=1
            else:
                # Capture entire block as keyword and add to subtitles list
                keyword_lines = ""
                while i < len(lines) and lines[i]!= '\n':
                    keyword_lines += lines[i].rstrip('\n')
                    keyword_lines = keyword_lines.strip()
                    i+=1
                prev = ''
                
                if keyword_lines:
                    subtitle = SubtitlesTimeRange(user_token = token, video_name = video_name, subtitle=keyword_lines,  duration= duration)
                    subtitles_bulk_update_list.append(subtitle)
                i+=1
        # Perform the bulk write operation
        with SubtitlesTimeRange.batch_write() as batch:
            for subtitle in subtitles_bulk_update_list:
                try:
                    batch.save(subtitle)
                except PutError as e:
                    print(f"Error writing item {subtitle.video_name}, {subtitle.subtitle}: {e}")
                    
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

def get_data_from_db(keyword, token):
    try:
        results = []
        video_name =""
        for token_video_mapping in TokenVideoMapping.query(token):
            video_name = token_video_mapping.video_name
        for i in SubtitlesTimeRange.query(video_name, filter_condition= SubtitlesTimeRange.subtitle.contains(keyword)):
            if i.user_token != token:
                continue
            start_time, end_time = i.duration.split(' --> ')
            results.append({'start_time': start_time.strip(), 'end_time': end_time.strip()})
        return results
    except Exception as e:
        print(f"Error fetching data from db: {e}")
        return []
    