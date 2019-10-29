#-*- coding:utf-8 -*-

import os

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
import datetime
from depromeet7SoBoon import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.six import python_2_unicode_compatible

# Create your models here.

# 사용자 정보
class User(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    email = models.CharField(max_length=254, null=False, unique=True) # 사용자 이메일
    name  = models.CharField(max_length=45, null=False) # 사용자 이름
    pwd = models.CharField(max_length=100, null=True) # 사용자 비밀번
    token = models.CharField(max_length=254) # 토큰
    telephone = models.CharField(max_length=11) # 전화번호
    legion = models.CharField(max_length=254) # 지역
    profile_image = models.TextField(null=True,blank=True) # 사용자 프로필 이미지 URL (없으면 빈 스트링 돌려주기)
    created_time = models.DateTimeField(auto_now_add=True,editable=False, blank=True) # 사용자 회원 가입 시각
    modified_time = models.DateTimeField(auto_now=True, null=True, blank=True) # 최근 사용자의 정보 변경 시각
    deleted_time = models.DateTimeField(auto_now=True, null=True, blank=True) # 사용자 정보 삭제 시각

    class Meta:
        ordering = ['-created_time',]
        verbose_name = '이용자'
        verbose_name_plural = '이용자들'

# 카테고리
class Category(models.Model):
    id = models.AutoField(primary_key=True) # 카테고리 id
    category = models.CharField(max_length=100, unique=True, null=False) # 카테고리명
    seq = models.IntegerField(null=False) # 카테고리 seq
    created_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True)  # 사용자 회원 가입 시각
    modified_time = models.DateTimeField(auto_now=True, null=True ,blank=True)  # 최근 사용자의 정보 변경 시각
    deleted_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 사용자 정보 삭제 시각

    class Meta:
        ordering = ['seq',]

# 글 정보
class Post(models.Model):
    id = models.AutoField(primary_key=True) # post ID
    title = models.TextField(null=False) # 글 제목
    product_url = models.TextField(blank=True) # 상품 링크
    content = models.TextField(null=False) # 본문 내용
    goal_num = models.IntegerField(null=False, default=1) # 모집 인원
    price = models.IntegerField(null=False) # 원래 가격
    soboon_price = models.IntegerField(null=False, default=0) # 소분 가격
    shipping_address = models.TextField(blank=False) # 수령 장소
    closing_time = models.DateTimeField(null=False) # 마감 시각
    finished_time = models.DateTimeField(blank=True) # 완료 시각
    status = models.CharField(max_length=254,null=False) # 상태
    created_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True)  # 본문 생성 시각
    modified_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 본문 변경 시각
    deleted_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 본문 삭제 시각
    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    ) # 작성자 id
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False
    ) # 카테고리 id

    class Meta:
        ordering = ['-created_time',]

# 댓글
class Comment(models.Model):
    id = models.AutoField(primary_key=True) # comment ID
    content = models.TextField(null=False) # 댓글 내용
    created_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True)  # 댓글 생성 시각
    modified_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 댓글 변경 시각
    deleted_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 댓글 삭제 시각
    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    ) # 작성자 id
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False
    ) # 본문 id

    class Meta:
        ordering = ['-created_time', 'post_id',]

# 참여
class Join(models.Model):
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    ) # 사용자 id
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False
    ) # 본문 id
    created_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True)  # 댓글 생성 시각
    modified_time = models.DateTimeField(auto_now=True,null=True, blank=True)  # 댓글 변경 시각
    deleted_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 댓글 삭제 시각

# 찜
class Like(models.Model):
    liker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    ) # 사용자 id
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False
    ) # 본문 id
    created_time = models.DateTimeField(auto_now_add=True, editable=False, blank=True)  # 댓글 생성 시각
    modified_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 댓글 변경 시각
    deleted_time = models.DateTimeField(auto_now=True, null=True, blank=True)  # 댓글 삭제 시각