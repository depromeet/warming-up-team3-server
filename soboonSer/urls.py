#-*- coding:utf-8 -*-
from django.conf.urls import include
from django.urls import path

from soboonSer import views
# from rest_framework_swagger.views import get_swagger_view
#
# schema_view = get_swagger_view(title="API")
#
# urlpatterns = [
#     url('^$', schema_view)
# ]


urlpatterns = [
    # [POST] /api/jipsa/auth/signup 회원가입
    # path('auth/signup/', views.UserSignUpAPIView.as_view()),
    #
    # path('image/upload/',views.ImageUploadTestAPIView.as_view()),
    # # [POST] /api/jipsa/auth/signin 로그인
    # path('auth/signin/', views.UserSignInAPIView.as_view()),
    #
    # # [GET] /api/jipsa/main/{userId} 글 작성 개수 가져오기
    # path('main/<int:userId>/', views.DiaryCntAPIView.as_view()),

    # [GET] /api/categorise 카테고리 가져오기
    path('categorise/', views.CategoryListAPIView.as_view()),

   # [GET] /api/posts 소분 피드 가져오기
    path('posts/', views.FeedListAPIView.as_view()),

]