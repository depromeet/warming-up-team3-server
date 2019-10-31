#-*- coding:utf-8 -*-
from rest_framework import serializers
from soboonSer.models import (
    User,
    Post,
    Category,
    Comment,
    Join,
    Like
    )

# 사용자 회원 가입
class CustomUserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name','token','telephone','profile_image')

# 사용자 로그인
class CustomUserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','token')

# 사용자 정보
class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name','token','telephone','created_time','modified_time')

# 마이페이지 - 유저 정보
class MyPageModelGetSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='id')
    userEmail = serializers.CharField(source='email')
    userName = serializers.CharField(source='name')
    userTelephone = serializers.CharField(source='telephone')
    userProfileImage = serializers.CharField(source='profile_image')
    createdAt = serializers.DateTimeField(source='created_time')
    modifiedAt = serializers.DateTimeField(source='modified_time')

    class Meta:
        model = User
        fields = ('userId', 'userEmail','userName','userTelephone', 'userProfileImage', 'createdAt', 'modifiedAt')

# 카테고리 가져오기
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category', 'seq')

# 글 피드 가져오기 (리스트)
class PostListModelSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='id')
    postTitle = serializers.CharField(source='title')
    postGoalNum = serializers.IntegerField(source='goal_num')
    postProductPrice = serializers.IntegerField(source='price')
    postSoboonPrice = serializers.IntegerField(source='soboon_price')
    postClosingTime = serializers.DateTimeField(source='closing_time')

    class Meta:
        model = Post
        fields = ('postId', 'postTitle', 'postGoalNum',
                  'postProductPrice','postSoboonPrice','postClosingTime')

# 글 상세 보기
class PostDetailModelSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='id')
    categoryId = serializers.IntegerField(source='category_id')
    writerId = serializers.IntegerField(source='writer_id')
    postTitle = serializers.CharField(source='title')
    postProductUrl = serializers.CharField(source='product_url')
    postContent = serializers.CharField(source='content')
    postGoalNum = serializers.IntegerField(source='goal_num')
    postProductPrice = serializers.IntegerField(source='price')
    postShippingAddress = serializers.CharField(source='shipping_address')
    postClosingTime = serializers.DateTimeField(source='closing_time')
    postFinishedTime = serializers.DateTimeField(source='finished_time')
    postStatus = serializers.CharField(source='status')
    postCreatedAt = serializers.DateTimeField(source='created_time')

    class Meta:
        model = Post
        fields = ('postId', 'categoryId','writerId', 'postTitle', 'postProductUrl',
                  'postContent', 'postGoalNum', 'postProductPrice','postClosingTime',
                  'postShippingAddress', 'postClosingTime', 'postFinishedTime',
                  'postStatus', 'postCreatedAt'
                  )

# 각자 글 참여 개수 가져오기
class JoinCountModelSerializer(serializers.ModelSerializer):
    join_count = serializers.SerializerMethodField()

    class Meta:
        model = Join
        fields = ('id', 'name', 'user_count')

    def get_join_count(self, obj):
        return obj.user_set.count()

# 참여 리스트 가져오기
class JoinModelSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post_id')
    participantId = serializers.IntegerField(source='participant_id')

    class Meta:
        model = Join
        fields = ('postId','participantId')

