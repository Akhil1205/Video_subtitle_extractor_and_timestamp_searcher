from django.conf import settings
from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .tasks import process_video , get_data_from_db
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class VideoUploadView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'video_subtitle/upload.html')
    
    def post(self, request , *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not Token.objects.filter(key=token).exists():
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        video = request.FILES.get('video')
        VIDEO_NAME = video.name
        video_path = os.path.join(settings.MEDIA_ROOT, VIDEO_NAME)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # Save the video file
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)
        import pdb; pdb.set_trace()
        for token_video_mapping in TokenVideoMapping.query(token):
            if token_video_mapping.video_name == VIDEO_NAME:
                return Response({'error': 'Video already uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Update the video_name
                token_video_mapping.update(actions=[
                    TokenVideoMapping.video_name.set(VIDEO_NAME)
                ])
        process_video(video_path, token)
        
        return Response({'message': 'Video uploaded successfully'}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class SearchSubtitlesView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'video_subtitle/search.html')
    
    def put(self, request , *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not Token.objects.filter(key=token).exists():
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        keyword = request.data.get('keyword')
        results_list = get_data_from_db(keyword, token)
        
        return Response({'result': results_list}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render (request, 'video_subtitle/login.html')
    
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        user = User.objects.filter(username=username, password=password).first()
        
        if user is not None:
            # Check if the user already has a token, create one if not
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
