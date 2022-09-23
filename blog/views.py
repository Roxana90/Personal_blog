from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from .models import Post, Likes
from .forms import CommentForm, ContactForm
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required


# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but do not save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def contact_page(request):
    forms = ContactForm()
    if request.method == 'POST':
        forms = ContactForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.add_message(request, messages.INFO, 'Submitted!')
            return redirect(reverse('blog:contact'))
    context = {
        'forms': forms
    }
    return render(request, 'contact.html', context)


@login_required
def like_post(request, slug):
    if request.method != 'POST':
        raise Http404('This method is not supported.')

    post = get_object_or_404(Post, slug=slug)
    like = post.likes.filter(user=request.user).first()
    if like is None:
        Likes.objects.create(user=request.user, content_object=post)
    else:
        like.delete()

    return redirect(reverse('blog:post_detail', args=[slug]))
