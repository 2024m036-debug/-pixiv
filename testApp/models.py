from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    # ↓ 追加：よみがな
    title_kana = models.CharField(max_length=200, verbose_name="記事タイトルのよみがな", blank=True, null=True)
    # ↓ 追加：概要（250文字制限）
    summary = models.TextField(max_length=250, verbose_name="概要", blank=True, null=True)
    
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
    def __str__(self):
        return self
    
class SubContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='sub_contents')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title