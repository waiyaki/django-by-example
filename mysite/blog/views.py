from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{name} ({email}) recommends you reading {title}'.format(
                **clean_data, title=post.title
            )
            message = "Read '{}' at {}\n\n{name}'s comments: {comments}".format(
                post.title, post_url, **clean_data
            )
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [clean_data['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {'post': post, 'form': form, 'sent': sent}
    )
