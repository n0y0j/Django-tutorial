from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    # 모든 필드에 값이 있는지를 판단
    if form.is_valid():
      # 폼을 저장하고 작성자를 추가, commit=False는 넘겨진 데이터를 바로 Post 모델에 저장하지 말 것
      # why? Authot 필드가 없지만 추가를 해야하기 때문
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      # 새 글을 작성후 post_detail로 바로 이동
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm()
  return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm(instance=post)
  return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_draft_list(request):
  # 코드로 발행되지 않은 글 목록을 가져옴, 오름차순 정렬
  posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
  return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST" :
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = CommentForm()
  return render(request, 'blog/add_comment_to_post.html', {'form' : form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)