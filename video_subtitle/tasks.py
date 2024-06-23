import os,boto3,subprocess
from celery import shared_task
from django.conf import settings
from video_subtitle.models import SubtitlesTimeRange
from django.conf import settings
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
        duration = ""
        prev = ''
        while i < 14:
            print(lines[i])
            if prev == '':
                prev = 'time'
                i+=1
            elif '-->' in lines[i]:
                duration = lines[i]
                i+=1
            else:
                # Capture entire block as keyword and add to subtitles list
                keyword_lines = ""
                while i < 14 and lines[i]!= '\n':
                    keyword_lines += lines[i].rstrip('\n')
                    keyword_lines = keyword_lines.strip()
                    i+=1
                prev = ''
                    
                if keyword_lines:
                    import pdb; pdb.set_trace()
                    print(f"Keyword: {keyword_lines}, Duration: {duration} -----------------------------")
                    subtitle = SubtitlesTimeRange(video_name = settings.VIDEO_NAME, subtitle=keyword_lines,  duration= duration)
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

def get_data_from_db(keyword):
    try:
        results = []
        print(keyword)
        for i in SubtitlesTimeRange.query(settings.VIDEO_NAME ,filter_condition= SubtitlesTimeRange.subtitle.contains(keyword), limit=5):
            # Split the duration into start and end times
            start_time, end_time = i.duration.split(' --> ')
            # Append the result as a dictionary
            results.append({'start_time': start_time.strip(), 'end_time': end_time.strip()})
        
        return results
    except Exception as e:
        print(f"Error fetching data from db: {e}")
        return []

