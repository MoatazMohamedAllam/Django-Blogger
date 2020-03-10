from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Comment
from users.models import Profile
from .forms import CommentForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin



#views functions===========================================
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def user_posts(request,username):
    user = get_object_or_404(User,username=username)
    posts = Post.objects.filter(author=user)
    context={
        'posts':posts
    }
    return render(request,'blog/user_posts.html',context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def post_detail(request,post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.filter(active=True)

    new_comment = None
    current_user = User.objects.get(id = request.user.id)
    user_profile = Profile.objects.get(user_id = current_user.id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.profile = user_profile
            new_comment.save()
            return redirect('blog:detail',post.id)
    else:
        comment_form = CommentForm()

    context={
        'post':post,
        'form':comment_form,
        'new_comment':new_comment,
        'comments':comments
    }
    return render(request,'blog/post_detail.html',context)


#Class based view============================================
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/update_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



