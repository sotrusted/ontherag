import os
from django.conf import settings

def load_images(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'images')
    image_files = [fn for fn in os.listdir(media_path) if fn[0] != '.']
    image_urls = [os.path.join(settings.MEDIA_URL, 'images', image) for image in image_files]
    return {
        'image_urls': image_urls
    }