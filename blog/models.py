from django.conf import settings
from django.db import models
from django.utils import timezone

# 객체를 정의, 모델의 이름 Post
class Post(models.Model):
    #models.CharField - 글자 수가 제한된 텍스트를 정의할 때 사용
    #models.TextField - 글자 수에 제한이 없는 긴 텍스트를 위한 속성
    #models.DateTimeField - 날짜와 시간을 의미.
    #models.ForeignKey - 다른 모델에 대한 링크를 의미 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True, upload_to="")
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    #models.BoolenField - 참/거짓 필드
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text