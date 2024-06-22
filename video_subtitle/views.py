from rest_framework.views import APIView
# from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render,redirect
from .forms import VideoUploadForm
from video_subtitle.tasks import process_video
import os

class ProcessVideoSubtitle(APIView):
    def post(self, request):
        # Process the video subtitle
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']
            print(video)
            # subprocess.run([settings.CCEXTRACTOR_PATH,video.path, '-o', 'output.srt'])
            form.save()
        context = {
            "form": form
        }
        return render(request,"video_subtitle/upload.html",context )
    
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = request.FILES['video']
            video_name = video.name
            video_path = os.path.join(settings.MEDIA_ROOT, video_name)
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            with open(video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)
            process_video(video_path)
            return redirect('success')
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

def success(request):
    return render(request, 'success.html')