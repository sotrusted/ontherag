import os
from django.conf import settings

def load_images(request):
    logo_path = os.path.join(settings.MEDIA_URL, 'CE_OTRLogo_RealMadrid_alpha-Black.png')
    media_path = os.path.join(settings.MEDIA_ROOT, 'images')
    image_files = [fn for fn in os.listdir(media_path) if fn[0] != '.']
    image_urls = [os.path.join(settings.MEDIA_URL, 'images', image) for image in image_files]
    return {
        'logo_path': logo_path,
        'image_urls': image_urls
    }
