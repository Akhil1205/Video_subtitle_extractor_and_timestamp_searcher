# Video Subtitle Fetcher

## Overview

Video Subtitle Fetcher is a web application that allows users to upload videos, extract subtitles using CCExtractor, and search for specific subtitles within those videos. The backend is built using Django, and the application is hosted on an AWS EC2 instance.

## Backend

The backend is implemented using Django and provides two token-authenticated APIs:

### /video/upload/
- **Functionality**: Processes the uploaded video, extracts subtitles using CCExtractor, and stores the video name, subtitles, duration, and user token in the database. The processed video is then uploaded to an AWS S3 bucket.

### /video/search
- **Functionality**: Searches for the subtitle duration based on a keyword provided by the user. The user's token is authorized, and the latest video uploaded by the user is identified. The application returns the subtitle durations matching the keyword for the latest video uploaded by the user.

### Database
- **PynamoDB** is used to configure AWS DynamoDB as the primary database.
- **Tables**:
  - `SubtitleTimeRange`
  - `TokenVideoMapping`

## Front-End

The front-end is built with basic HTML and JavaScript. JavaScript is used to update the status from the backend and query the backend for responses to display.

## Hosting

The application is hosted on an AWS EC2 instance with the following configurations:

- **Instance Type**: `t3a.small` for its competitive pricing and higher number of cores, beneficial for uploading large video files (above 50 MB).
- **Elastic IP**: Used to maintain a constant public IP address despite instance restarts or reboots.
- **IAM Role**: Utilized for querying DynamoDB and uploading files to the S3 bucket. The IAM role is granted `AmazonS3FullAccess` and `AmazonDynamoDBFullAccess` policies for seamless connectivity.

### Security

IAM role-based access is used for enhanced security, avoiding hard-coding access keys and security keys in the code or retrieving them from environment variables.

### Deployment

The deployment involves configuring the application with NGINX, setting up Gunicorn, and ensuring security groups allow appropriate traffic. The `client_max_body_size` in NGINX is set to 100MB to avoid over-utilization of resources.

## Project Links

- **GitHub Repository**: [Video Subtitle Extractor and Timestamp Searcher](https://github.com/Akhil1205/Video_subtitle_extractor_and_timestamp_search)
- **Hosted Website**: [Video Subtitle Fetcher](http://65.0.223.7/video/login/)

  - **Login Credentials**:
    - **Username**: not_disclosed
    - **Password**: not_disclosed
    - **Note**: Use an `.mp4` type file for upload and wait for 30 to 40 seconds for the upload to complete from the front-end to the back-end.

## Usage

1. **Upload a Video**:
   - Navigate to `/video/upload/` and upload your video file.
   - Wait for the video to be processed and uploaded to the S3 bucket.
2. **Search for Subtitles**:
   - Navigate to `/video/search/` and enter a keyword to search within the subtitles of the latest uploaded video.


