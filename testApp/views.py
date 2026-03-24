from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, SubContent
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# タイムライン（一覧）
def timeline(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(parent=None).order_by('-created_at')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'timeline.html', {'posts': posts, 'query': query})

# 投稿作成（Imagen API の導入箇所）
PROJECT_ID = "あなたのプロジェクトID" 
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        title_kana = request.POST.get('title_kana')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        
        # 投稿データを新しく作成
        post = Post(
            title=title,
            title_kana=title_kana,
            summary=summary,
            content=content,
            author=request.user,
            # 他に必要な項目（title_kanaなど）があればここに追加してください
        )

        # ★画像が選ばれていたらセットする★
        if 'image' in request.FILES:
            post.image = request.FILES['image']
            
        post.save()
        return redirect('timeline')
    
    return render(request, 'create_post.html')

# 詳細ページ（先ほどの回答の通り画像を出すようにしてください）
def post_detail(request, pk):
    parent_post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # 詳細ページ内での追加投稿（子投稿）
        Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            author=request.user,
            parent=parent_post
        )
        return redirect('post_detail', pk=pk)
    
    child_posts = parent_post.replies.all().order_by('created_at')
    return render(request, 'post_detail.html', {'post': parent_post, 'child_posts': child_posts})

# 編集・削除（既存のまま）
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 投稿者本人か確認
    if post.author != request.user:
        return redirect('timeline')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.title_kana = request.POST.get('title_kana')
        post.summary = request.POST.get('summary')
        post.content = request.POST.get('content') # ここで追記された本文を保存
        
        if 'image' in request.FILES:
            post.image = request.FILES['image']
            
        post.save()
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    parent_pk = post.parent.pk if post.parent else None
    if post.author == request.user or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
    return redirect('post_detail', pk=parent_pk) if parent_pk else redirect('timeline')

@login_required
def add_content(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # 投稿者本人か確認
    if post.author != request.user:
        return redirect('timeline')

    if request.method == 'POST':
        extra = request.POST.get('extra_content')
        if extra:
            # 元の本文の後に、改行を挟んで新しい内容を合体させる
            post.content = post.content + "\n\n--- 追記 ---\n" + extra
            post.save()
            
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'add_content.html', {'post': post})

@login_required
def add_sub_content(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        sub_title = request.POST.get('sub_title')
        sub_content = request.POST.get('sub_content')
        
        if sub_title and sub_content:
            # ★これだけでOK（一覧用のデータとして保存）
            SubContent.objects.create(
                post=post,
                title=sub_title,
                content=sub_content
            )
            
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'add_sub_content.html', {'post': post})

# 詳細情報の編集
@login_required
def edit_sub_content(request, pk):
    sub = get_object_or_404(SubContent, pk=pk)
    # 投稿者本人か確認
    if sub.post.author != request.user:
        return redirect('post_detail', pk=sub.post.pk)

    if request.method == 'POST':
        sub.title = request.POST.get('sub_title')
        sub.content = request.POST.get('sub_content')
        sub.save()
        return redirect('post_detail', pk=sub.post.pk)
    
    return render(request, 'edit_sub_content.html', {'sub': sub})

# 詳細情報の削除
@login_required
def delete_sub_content(request, pk):
    sub = get_object_or_404(SubContent, pk=pk)
    post_pk = sub.post.pk
    
    if sub.post.author == request.user:
        sub.delete()
        
    return redirect('post_detail', pk=post_pk)