from typing import Any
from django.forms.models import model_to_dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView, 
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Personal, Images
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .forms import PersonalForm, ImageForm, ContactForm

posts = [
    {
        'author': 'SoTrusted',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'June 3, 2024'
    },
    {
        'author': 'SoTrusted',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'June 3, 2024'
    }
]


def home(request):
    context = {
        'posts': Personal.objects.all().order_by('-id')
    }
    return render(request, 'blog/blog-home.html', context)


class PersonalListView(ListView):
    model = Personal
    template_name = 'blog/blog-home.html' # <app>/<model>_<viewtype>.html template name 
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 5

class UserPersonalListView(ListView):
    model = Personal
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html template name 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Personal.objects.filter(author=user).order_by('-date_posted')

class PersonalDetailView(DetailView):
    model = Personal
    template_name = 'blog/personal_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs) 
        print(data)

        post = data['post'] 
        print(post)
        print(model_to_dict(post))
        data['pics'] = post.get_images()
        print(data['pics'])
        # Get previous and next posts
        data['prev_post'] = Personal.objects.filter(id__lt=post.id).order_by('-id').first()
        data['next_post'] = Personal.objects.filter(id__gt=post.id).order_by('id').first()
        return data
         
    
   
class PersonalUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Personal
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PersonalDeleteView(LoginRequiredMixin, DeleteView):
    model = Personal
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/blog-about.html', {'title' : 'About'})

ImageFormSet = inlineformset_factory(Personal, Images, min_num=0, extra=5, fields=('image', ))
FORMS = [
    ("personal", PersonalForm),
]

TEMPLATES = {
    "personal" : "blog/personal_form.html",
}

class PostWizard(SessionWizardView):
    form_list = FORMS
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
    
    template_name = 'blog/personal_form.html'

    def done(self, form_list, **kwargs):
        post_form = form_list[0]

        personal = Personal(
            title=post_form.cleaned_data.get('title', ''),
            city=post_form.cleaned_data.get('city', ''),
            description=post_form.cleaned_data.get('description', ''),
            image1=post_form.cleaned_data.get('image1', ''),
            image2=post_form.cleaned_data.get('image2', ''),
            image3=post_form.cleaned_data.get('image3', ''),
            image4=post_form.cleaned_data.get('image4', ''),
            image5=post_form.cleaned_data.get('image5', ''),
            image6=post_form.cleaned_data.get('image6', ''),
            phone=post_form.cleaned_data.get('phone', ''),
            email=post_form.cleaned_data.get('email', ''),
            social_link=post_form.cleaned_data.get('social_link', ''),
            author=self.request.user if self.request.user.is_authenticated else None
        )

        personal.save() 

        print(post_form.cleaned_data)
        images = [post_form.cleaned_data.get(f'image{i}') for i in range(6)]
        if images:
            for image in images:
                 new_image = Images(personal=personal, image=image)
                 new_image.save()

        '''
        images = post_form.cleaned_data.get('images')
        
        if images:
            for image in images:
                print(f"Saving image: {image.name}")
                img = PersonalImage(personal=personal, image=image)
                img.save()
        ''' 
        messages.success(self.request, 'Successfully posted!')

        personal.save()


        return redirect('home')
'''
    def process_step(self, form):
        if self.steps.current == 'personal':  # Adjust based on your form order
            images = self.request.FILES.getlist('images')
            if len(images) > 5:
                form.add_error('images', 'You can upload a maximum of 5 images.')
        return super().process_step(form)
        '''

ImageFormSet = modelformset_factory(Images,
                                form=ImageForm, extra=5)
ImageFormSet = inlineformset_factory(Personal, Images, form=ImageForm, 
                                     min_num = 0, extra = 5, can_delete=True)



class PersonalCreateView(CreateView):
    model = Personal
    fields = ['title', 'city', 'description', 'phone', 'email', 'social_link']
    template_name = 'blog/personal_form.html'


    def get(self, request, *args, **kwargs):
        context = {
            'personalForm': PersonalForm(),
            'imageForm': ImageForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        personalForm = PersonalForm(request.POST)
        files = request.FILES.getlist('image')

        if personalForm.is_valid(): 
            personal_form = personalForm.save(commit=False)
            personal_form.user = request.user
            personal_form.save()

            for img in files:
                Images.objects.create(personal=personal_form, image=img)
            messages.success(request, "successfully posted")

            return redirect(personal_form.get_absolute_url())

        else:
            print(personalForm.errors)
            



        






def post(request):
    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=5)

    if request.method == 'POST':

        postForm = PersonalForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, 
                               queryset=Images.objects.none())

        if post_form.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Images(post=post_form, image=image)
                    photo.save()
            
            messages.success(request, "successfully posted to the home page!")
            return HttpResponseRedirect('/')
        else:
            print(postForm.errors, formset.errors)
    
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'index.html', 
                  {'postForm': postForm, 'formset': formset})
