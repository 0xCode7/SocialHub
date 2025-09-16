from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages

from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


@login_required
def home_feed(request):
    user = request.user
    allowed_privacy = ['public']
    posts = Post.objects.filter(
        Q(privacy__in=allowed_privacy) | Q(author=user)
    ).order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comment_form': form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:home_feed')
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


def post_delete(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:  # Only author can delete
            post.delete()
            messages.success(request, "Your post was deleted successfully.")
        else:
            messages.error(request, "You are not allowed to delete this post.")
    return redirect('posts:home_feed')


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": post.likes.count(),
    })


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()

    if content:
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        return JsonResponse({
            "success": True,
            "author": comment.author.username,
            "content": comment.content,
            "comment_id": comment.id,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "comments_count": post.comments.count(),
            "can_delete": request.user == comment.author or request.user == post.author,

        })

    return JsonResponse({"success": False, "error": "Empty comment"}, status=400)


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only author or post owner can delete
    if comment.author == request.user or comment.post.author == request.user:
        comment.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Not allowed"}, status=403)
