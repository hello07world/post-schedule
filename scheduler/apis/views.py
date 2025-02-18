import os
import time
import uuid
import openai
import requests

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Post
from ..serializers import PostSerializer

# Ensure your OpenAI API key is set in your environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, updating, and deleting posts.
    Uses the 'X-User' header to differentiate users.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.headers.get('X-User', 'anonymous')
        return Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.headers.get('X-User', 'anonymous')
        serializer.save(user=user)


# 1. Caption Generator API using OpenAI's GPT-3
class GenerateCaptionAPIView(APIView):
    def get(self, request, format=None):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="Generate a creative and trend-relevant social media caption:",
                max_tokens=50,
                temperature=0.7,
            )
            caption = response.choices[0].text.strip()
            return Response({"caption": caption}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 2. Image Generator API using OpenAI's DALL·E (Image API)
class GenerateImageAPIView(APIView):
    def post(self, request, format=None):
        caption = request.data.get('caption', '')
        if not caption:
            return Response({"error": "Caption is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = openai.Image.create(
                prompt=caption,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            return Response({"image_url": image_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 3. Text-to-Video API using an external AI tool (e.g., D-ID Creative Reality API)
class GenerateTextVideoAPIView(APIView):
    """
    This API view receives text input and uses an external AI tool (e.g., D-ID Creative Reality API)
    to generate a video based solely on that text.
    """

    def post(self, request, format=None):
        video_text = request.data.get('text', '')
        if not video_text:
            return Response({"error": "Text input is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # D-ID API configuration
        api_key = os.environ.get("DID_API_KEY", "your-did-api-key")
        api_endpoint = "https://api.d-id.com/talks"  # Adjust endpoint as per documentation
        
        payload = {
            "script": {
                "type": "text",
                "input": video_text,
                "provider": {"type": "microsoft", "voice_id": "en-US-AriaNeural"}
            },
            "config": {"fluent": True}
        }
        
        headers = {
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            creation_response = requests.post(api_endpoint, json=payload, headers=headers)
            if creation_response.status_code != 201:
                return Response({
                    "error": "Video generation request failed.",
                    "details": creation_response.json()
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            data = creation_response.json()
            video_id = data.get("id")
            if not video_id:
                return Response({"error": "Video ID not returned."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Poll the API for video completion (adjust polling interval and timeout as needed)
            poll_endpoint = f"{api_endpoint}/{video_id}"
            max_attempts = 30
            for attempt in range(max_attempts):
                poll_response = requests.get(poll_endpoint, headers=headers)
                if poll_response.status_code != 200:
                    return Response({"error": "Failed to poll video status."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                poll_data = poll_response.json()
                if poll_data.get("status") == "completed":
                    video_url = poll_data.get("result_url")
                    if video_url:
                        return Response({"video_url": video_url}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error": "Video URL not available."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                time.sleep(2)
            
            return Response({"error": "Video generation timed out."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 4. Create Post API view (if separate from PostViewSet)
class CreatePostAPIView(APIView):
    """
    An alternative API to create a post.
    This endpoint allows setting status (created, draft, scheduled, published, deleted),
    as well as optional scheduled_time.
    """
    def post(self, request, format=None):
        # You can adjust the fields as needed
        data = request.data.copy()
        data['user'] = request.headers.get('X-User', 'anonymous')
        
        # Validate required fields if necessary
        required_fields = ['post_type']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response({field: "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        from ..serializers import PostSerializer  # Import here to avoid circular import issues
        
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
