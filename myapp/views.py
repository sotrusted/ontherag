from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
import os
from blog.models import Personal

# Create your views here.

def home(request):
    media_path = os.path.join(settings.MEDIA_ROOT, 'images')
    image_files = os.listdir(media_path)
    image_urls = [os.path.join(settings.MEDIA_URL, 'images', image) for image in image_files]
    blog_embed = render_to_string('blog/blog-home.html')
    return render(request, 'home.html', {'image_urls': image_urls, 'blog_embed' : blog_embed, 'posts': Personal.objects.all()})
