# customwysiwyg/views.py

import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_protect
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # Validate file size (e.g., max 5MB)
        if image.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'Image file too large ( > 5MB )'}, status=400)

        # Validate file type
        valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if image.content_type not in valid_mime_types:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        # Generate a unique filename
        ext = os.path.splitext(image.name)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(f'{request.user.username}/wysiwyg_uploads/', filename)

        # Save the image using default storage
        saved_path = default_storage.save(file_path, ContentFile(image.read()))

        # Get the URL to the saved image
        image_url = default_storage.url(saved_path)

        return JsonResponse({'url': image_url})

    return JsonResponse({'error': 'Invalid request'}, status=400)
