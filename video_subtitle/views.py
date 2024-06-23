from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render
import os

from .forms import VideoUploadForm, SearchForm
from .tasks import process_video , get_data_from_db # Assuming you have a process_video function in your utils module

# video_name = "default"
class VideoUploadView(FormView):
    form_class = VideoUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        video = self.request.FILES['video']
        settings.VIDEO_NAME = video.name[:6]
        video_path = os.path.join(settings.MEDIA_ROOT, settings.VIDEO_NAME)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Save the video file
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
        
        # Process the video after saving
        process_video(video_path)
        
        return super().form_valid(form)

class SearchView(FormView):
    form_class = SearchForm
    template_name = 'success.html'

    def form_valid(self, form):
        keyword = form.cleaned_data['keyword']
        print(keyword)
        import pdb; pdb.set_trace()
        results_list = get_data_from_db(keyword)
        # results_list =[1,2,3]
        return render(self.request, self.template_name, {'form': form, 'results_list': results_list})