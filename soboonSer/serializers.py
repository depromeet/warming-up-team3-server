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
from django.db.models import Count

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

# 간단 유저 정보 (글 작성자 정도)
class CustomUserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')

# 마이페이지 - 유저 정보 불러오기 // TODO 내 소분 개수 및 참여 소분 개수 및 찜한 소분 개수 가져와야 함
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


# 각자 글 참여 개수 가져오기 // TODO 어떤 게시글의 참여 내역 불러오기 안되고 있다
class JoinCountModelSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post_id')
    # join = serializers.StringRelatedField(many=True)
    currentJoinNum = serializers.SerializerMethodField()

    class Meta:
        model = Join
        fields = ('postId','currentJoinNum')

    def get_currentJoinNum(self, obj):
        return Join.objects.all().count()

# 참여 상세 내용 가져오기 // TODO 참여 상세 가져오기 안되고 있음
class JoinDetailModelSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post_id')
    participantId = serializers.IntegerField(source='participant_id')
    currentJoinNum = serializers.SerializerMethodField()

    class Meta:
        model = Join
        fields = ('postId', 'participantId', 'currentJoinNum')

    def get_currentJoinNum(self, obj):
        return Post.objects.annotate(Count('join'))

# 댓글 리스트 가져오기 // TODO depth 생각해야 하는지?
class CommentListModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    writer = CustomUserInfoModelSerializer()
    createdAt = serializers.DateTimeField(source='created_time')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'writer', 'createdAt']

# 글 피드 가져오기 (리스트) // TODO 현재 참여 정보 불러오기 안되고 있음
class PostListModelSerializer(serializers.ModelSerializer):
    # currentJoinNum = JoinDetailModelSerializer(source='')
    postId = serializers.IntegerField(source='id')
    postTitle = serializers.CharField(source='title')
    postGoalNum = serializers.IntegerField(source='goal_num')
    postProductPrice = serializers.IntegerField(source='price')
    postSoboonPrice = serializers.IntegerField(source='soboon_price')
    postClosingTime = serializers.DateTimeField(source='closing_time')
    postCreatedAt = serializers.DateTimeField(source='created_time')

    class Meta:
        model = Post
        fields = ('postId', 'postTitle', 'postGoalNum',
                  'postProductPrice','postSoboonPrice','postClosingTime', 'postCreatedAt')

# 글 제목 및 상태 간단히 가져오기
class PostSummaryModelSerializer(serializers.ModelSerializer):
    category = CategoryModelSerializer()
    postId = serializers.IntegerField(source='id')
    postTitle = serializers.CharField(source='title')
    postStatus = serializers.CharField(source='status')
    postCreatedAt = serializers.DateTimeField(source='created_time')

    class Meta:
        model = Post
        fields = ('postId', 'category', 'postTitle','postStatus', 'postCreatedAt')

# 글 상세 보기 // TODO 참여 정보 불러와야 함
class PostDetailModelSerializer(serializers.ModelSerializer):
    writer = CustomUserInfoModelSerializer()
    postId = serializers.IntegerField(source='id')
    category = CategoryModelSerializer()
    # categoryId = serializers.IntegerField(source='category_id')
    # writerId = serializers.IntegerField(source='writer_id')
    # currentJoinNum = JoinCountModelSerializer()

    post_comments = CommentListModelSerializer(many=True)

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
        fields = ('postId', 'category','writer', 'postTitle', 'postProductUrl',
                  'postContent', 'postGoalNum', 'postProductPrice','postClosingTime',
                  'postShippingAddress', 'postClosingTime', 'postFinishedTime',
                  'postStatus', 'postCreatedAt', 'post_comments'
                  )

# 유저의 작성 글 리스트 가져오기
class UserPostsListModelSerialzier(serializers.ModelSerializer):
    posts = PostSummaryModelSerializer(many=True,read_only=True)
    userId = serializers.IntegerField(source='id')
    userEmail = serializers.CharField(source='email')
    userName = serializers.CharField(source='name')

    # postswriter = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['userId','userEmail','userName','posts']

# 유저의 참여 리스트 가져오기 // TODO 참여랑 post 정보랑 같이 불러와야 함
class UserJoinedPostListModelSerializer(serializers.ModelSerializer):
    join_posts = PostSummaryModelSerializer(many=True, read_only=True)
    userId = serializers.IntegerField(source='id')
    userEmail = serializers.CharField(source='email')
    userName = serializers.CharField(source='name')

    class Meta:
        model = User
        fields = ['userId','userEmail','userName','join_posts']