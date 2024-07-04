from django import template

register = template.Library()

@register.simple_tag
def get_first_nonempty_image(post):
    images = [post.image1, post.image2, post.image3, post.image4, post.image5, post.image6]
    for image in images:
        if image:
            return image
    return None
