#-*- coding:utf-8 -*-
# from django.shortcuts import render
#
# # Create your views here.
from django.conf import settings
import json, os, base64
#
from datetime import datetime
#
# # from cryptography.fernet import Fernet
# # from cryptography.hazmat.backends import default_backend
# # from cryptography.hazmat.primitives import hashes
# # from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated

from soboonSer.models import (
    User,
    Category,
    Post,
    Comment,
    Join,
    Like
    )

from soboonSer.serializers import (
    CustomUserModelSerializer,
    CustomUserSignUpSerializer,
    CustomUserSignInSerializer,
    MyPageModelGetSerializer,
    CategoryModelSerializer,
    PostListModelSerializer,
    PostDetailModelSerializer
    )

from rest_framework.authtoken.models import Token
from django.http import Http404

from soboonSer.logger_handler import LoggerHandler


from rest_framework.parsers import (
    FileUploadParser,
    MultiPartParser,
    FormParser,
    JSONParser
)

# 카테고리 가져오기
class CategoryListAPIView(APIView):
    permission_classes = (AllowAny, )

    # [GET] /api/categorise 카테고리 리스트 가져오기
    def get(self, request, *args, **kwargs):
        try:
            category_queryset = Category.objects.order_by('seq')
            category_serializer = CategoryModelSerializer(category_queryset, many=True)
            return Response(
                {
                    'id' : 0,
                    'categoryList': category_serializer.data
                }, status = status.HTTP_200_OK)
        except:
            return Response({ 'err_detail': 'data를 불러오지 못했습니다'}, status=status.HTTP_200_OK )

# 피드 가져오기
class FeedListAPIView(APIView):
    """
        Feed List
    """
    permission_classes = (AllowAny, )

    # [GET] /api/posts 글 리스트 가져오기
    def get(self,request,*args,**kwargs):
        try:
            post_queryset = Post.objects.order_by('-created_time')[:10]
            post_serializer = PostListModelSerializer(post_queryset, many=True)
            return Response(
                {
                    'id': 0,
                    'post': post_serializer.data
                }, status=status.HTTP_200_OK)
        except:
            return Response({'err_detail': 'data를 불러오지 못했습니다'}, status=status.HTTP_200_OK)

# class UserSignUpAPIView(APIView):
#     """
#         User SignUp
#     """
#
#     permission_classes = (AllowAny,)
#     # [POST] /api/jipsa/auth/signup 인증된 사용자 회원가입 (유저 테이블에 추가)
#     def post(self, request, *args, **kwargs):
#         received_data = json.dumps(request.data)
#
#         LoggerHandler.server_logger.debug(received_data)
#
#         received_data = json.loads(received_data)
#
#         # Model에 저장 위해 직렬화
#
#         serializer = CustomUserModelSerializer(data=request.data)
#         print(serializer.is_valid())
#
#         if not serializer.is_valid():
#             return Response({'err_detail': serializer.errors}, status=status.HTTP_200_OK)
#
#         serializer.save()
#
#         # 회원 가입 완료
#         return Response(
#                         {
#                             'id': 0,
#                              'userId' : serializer.data['id'],
#                              'userEmail' : serializer.data['email'],
#                              'userNickName' : serializer.data['nickname'],
#                              'userProfileImage' : serializer.data['profile_image'],
#                              'createdAt' : serializer.data['created_time']
#                          }
#                         , status=status.HTTP_200_OK)
#
# class UserSignInAPIView(APIView):
#     """
#         User SignIn
#     """
#     permission_classes = (AllowAny,)
#
#     # [POST] /api/jipsa/auth/signin 로그인
#     def post(self, request, *args, **kwargs):
#         try:
#             user = User.objects.get(
#                 email = request.data['email'],
#                 pwd = request.data['pwd']
#             )
#         except:
#             return Response({'error_msg': '가입된 사용자 정보가 없습니다. 이메일과 비밀번호를 확인해주세요.'}, status=status.HTTP_200_OK)
#
#         token, _ = Token.objects.get_or_create(user=user)
#
#         user_serialized = CustomUserModelSerializer(user)
#
#         return Response(
#                         {
#                             'id': 0,
#                             'userId' : user_serialized.data['id'],
#                             'userEmail' : user_serialized.data['email'],
#                             'userNickName' : user_serialized.data['nickname'],
#                             'userProfileImage' : user_serialized.data['profile_image'],
#                             'createdAt' : user_serialized.data['created_time'],
#                             'token': token.key
#                          }
#                         , status=status.HTTP_200_OK)
#
#
# class PostWriteAPIView(APIView):
#     """
#         Diary Write
#     """
#     permission_classes = (IsAuthenticated,)
#
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#
#     # [POST] /api/jipsa/diary/{userId} 새로운 글 작성하기 (이미지랑 같이)
#     def post(self, request, *args, **kwargs):
#         writer = int(self.kwargs['userId']) # 작성자 id
#         title = request.data['title']
#         converted_date = get_date(self,request.data['datetime'])
#         body = request.data['body']
#
#         try:
#             user = User.objects.get(pk=writer)  # 작성자 정보 가져오기
#         except:
#             return Response({'error_msg': '해당 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         # 새로운 일기 작성 (생성)
#         new_diary = Diary.objects.create(
#             writer=user,
#             title=title,
#             body=body,
#             date=converted_date
#         )
#
#         LoggerHandler.server_logger.debug(new_diary.pk)
#
#         diary_serializer = DiaryModelSerializer(new_diary) # 작성한 diary serializer
#
#         for file in request.FILES.getlist('file'):
#             print('durl 들어오냐')
#             print(file)
#
#         # 업로드 할 파일
#         image_file = None
#         if 'image' not in request.data:
#             image_file = None
#         else:
#             image_file = request.data['image']
#
#         # 업로드 할 파일이 없는 경우 --> 다이어리만 저장 후 바로 response
#         if image_file is None:
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': writer,
#                     'diary': {
#                         'diaryId': new_diary.pk,
#                         'title': diary_serializer.data['title'],
#                         'datetime': diary_serializer.data['date'],
#                         'body': diary_serializer.data['body'],
#                         'image': [
#                         ]
#                     }
#                 }
#                 , status=status.HTTP_201_CREATED)
#
#         # 다중 파일 업로드
#         # cnt=0
#         #     if file is None:
#         #         break
#         #     else:
#         #         print(file.name)
#         #         image_url = upload_file(file)
#         #         image_url = 'https://%s/%s/' % (settings.AWS_S3_CUSTOM_DOMAIN, settings.MEDIAFILES_LOCATION) + file.name
#         #         image_instance = Image(
#         #             diary=new_diary,
#         #             seq=cnt,
#         #             s3_url=image_url
#         #         )
#         #         image_instance.save()
#         #     cnt=cnt+1
#
#         s3_file_name = upload_file(image_file, new_diary.pk)
#
#         s3_url = 'https://%s/' % (settings.AWS_S3_CUSTOM_DOMAIN)
#
#         s3_url = s3_url + s3_file_name
#
#         image = Image.objects.create(
#             s3_url=s3_url,
#             diary=new_diary,
#             seq=0
#         )
#
#         image_serializer = Image.objects.filter(diary_id=new_diary.pk)
#
#         diary_serializer = DiaryDetailSerializer(instance=new_diary)
#
#         if image_serializer is not None:
#             # image_serializer.save()
#             # print(image.get_filename)
#             return Response(
#                         {
#                             'id': 0,
#                             'userId' : writer,
#                             'diary': diary_serializer.data
#                          }
#                         , status=status.HTTP_201_CREATED)
#         else:
#             return Response({'result_msg' : 'error'}, status=status.HTTP_200_OK)
#
#     # [GET] /api/jipsa/diary/{userId} 사용자의 작성 글 리스트 조회 (다중 배열로 뽑기)
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         try:
#             diary_serializer = DiaryDetailSerializer(queryset, many=True)
#             # image_serializer = ImageModelSerializer(diary=diary_serializer, many=True)
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': self.kwargs['userId'],
#                     'diary': diary_serializer.data
#             }, status=status.HTTP_200_OK)
#             # image_serializer = ImageModelSerializer(diary_uid=)
#         except:
#             return Response({'err_detail' : diary_serializer.errors}, status=status.HTTP_200_OK)
#
#     def get_queryset(self, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#         LoggerHandler.server_logger.debug(user_id)
#         queryset = Diary.objects.filter(writer_id=user_id)
#         return queryset
#
# class DiaryCntAPIView(APIView):
#     """
#         Diary Count
#     """
#     permission_classes = (IsAuthenticated,)
#
#     # [GET] /api/jipsa/main/{userId}
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#
#         diary_cnt = queryset.count()
#
#         LoggerHandler.server_logger.debug(diary_cnt)
#
#         return Response(
#                         {
#                             'id': 0,
#                             'userId' : self.kwargs['userId'],
#                             'diaryCnt': diary_cnt
#                          }
#                         , status=status.HTTP_200_OK)
#
#     def get_queryset(self, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#         LoggerHandler.server_logger.debug(user_id)
#         queryset = Diary.objects.filter(writer_id=user_id)
#         return queryset
#
# class SpecificDiaryAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#
#     # [GET] /api/jipsa/diary/{userId}/{diaryId} 특정 글 조회
#     def get(self, request, *args, **kwargs):
#         query = self.get_query()
#         try:
#             diary_serializer = DiaryDetailSerializer(instance=query)
#             # image_serializer = ImageModelSerializer(diary=diary_serializer, many=True)
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': self.kwargs['userId'],
#                     'diary': diary_serializer.data
#                 }, status=status.HTTP_200_OK)
#             # image_serializer = ImageModelSerializer(diary_uid=)
#         except:
#             return Response({'err_detail': diary_serializer.errors}, status=status.HTTP_200_OK)
#
#     def get_query(self, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#         diary_id = int(self.kwargs['diaryId'])
#         LoggerHandler.server_logger.debug(user_id)
#         LoggerHandler.server_logger.debug(diary_id)
#         query = Diary.objects.get(pk=diary_id,writer_id=user_id)
#         return query
#
#     # [PUT] /api/jipsa/diary/{userId}/{diaryId} 특정 글 수정
#     def put(self, request, *args, **kwargs):
#         writer = int(self.kwargs['userId']) # 작성자 id
#         diaryId = int(self.kwargs['diaryId']) # diary id
#
#         title = request.data['title']
#         # datetime = received_data['datetime']
#         converted_date = get_date(self,request.data['datetime'])
#         body = request.data['body']
#
#         try:
#             user = User.objects.get(pk=writer)  # 작성자 정보 가져오기
#         except:
#             return Response({'error_msg': '해당 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         try:
#             diary = Diary.objects.get(pk=diaryId)
#         except:
#             return Response({'error_msg': '해당 일기 정보가 없어 수정할 수 없습니다.'}, status=status.HTTP_200_OK)
#
#         # 새로운 일기 작성 (생성)
#         Diary.objects.filter(id=diary.pk).update(
#             writer=user,
#             title=title,
#             body=body,
#             date=converted_date,
#             modified_time=datetime.now()
#         )
#
#         diary = Diary.objects.get(pk=diaryId)
#
#         # LoggerHandler.server_logger.debug(modified_diary.pk)
#
#         diary_serializer = DiaryDetailSerializer(instance=diary) # 작성한 diary serializer
#
#         # 업로드 할 파일
#         image_file = None
#         if 'image' not in request.data:
#             image_file = None
#         else:
#             image_file = request.data['image']
#
#         # print(image_file)
#
#         # 업로드 할 파일이 없는 경우 --> 다이어리만 저장 후 바로 response
#         if image_file is None:
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': writer,
#                     'diary': diary_serializer.data
#                 }
#                 , status=status.HTTP_201_CREATED)
#
#         # 다중 파일 업로드
#         # cnt=0
#         # for file in request.FILES.getlist('image'):
#         #     if file is None:
#         #         break
#         #     else:
#         #         print(file.name)
#         #         image_url = upload_file(file)
#         #         image_url = 'https://%s/%s/' % (settings.AWS_S3_CUSTOM_DOMAIN, settings.MEDIAFILES_LOCATION) + file.name
#         #         image_instance = Image(
#         #             diary=new_diary,
#         #             seq=cnt,
#         #             s3_url=image_url
#         #         )
#         #         image_instance.save()
#         #     cnt=cnt+1
#
#         s3_file_name = upload_file(image_file, diary.pk)
#         print(s3_file_name)
#
#         s3_url = 'https://%s/' % (settings.AWS_S3_CUSTOM_DOMAIN)
#
#         s3_url = s3_url + s3_file_name
#
#         print('s3 url???? ', end=' ')
#         print(s3_url)
#         # received_data_to_json = json.loads(received_data)
#
#         get_image_query = Image.objects.get_or_create(diary_id=diaryId,seq=0)
#
#         get_image_query = Image.objects.filter(diary_id=diaryId, seq=0)
#
#         image = get_image_query.update(
#             s3_url=s3_url,
#             diary=diary,
#             seq=0,
#             modified_time=datetime.now()
#         )
#
#         image_serializer = Image.objects.get(diary_id=diary.pk)
#
#         diary_serializer = DiaryDetailSerializer(instance=diary)
#
#         if image_serializer is not None:
#             # image_serializer.save()
#             # print(image.get_filename)
#             return Response(
#                         {
#                             'id': 0,
#                             'userId' : writer,
#                             'diary': diary_serializer.data
#                             # 'diary' : {
#                             #     'diaryId': diary.pk,
#                             #     'title': diary_serializer.data['title'],
#                             #     'datetime': diary_serializer.data['date'],
#                             #     'body': diary_serializer.data['body'],
#                             #     'image' : [
#                             #         {
#                             #             'seq':image_serializer.seq,
#                             #             'imageId': image_serializer.pk,
#                             #             'imageUrl': image_serializer.s3_url
#                             #         }
#                             #     ]
#                             # }
#                          }
#                         , status=status.HTTP_201_CREATED)
#         else:
#             return Response({'result_msg' : 'error'}, status=status.HTTP_200_OK)
#
#     # [DELETE] /api/jipsa/diary/{userId}/{diaryId} 특정 글 삭제
#     def delete(self, request, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#         diary_id = int(self.kwargs['diaryId'])
#
#         try:
#             Diary.objects.get(writer_id=user_id, pk=diary_id)
#         except:
#             return Response({'result_msg':'삭제하고자 하시는 일기는 존재하지 않습니다.'},status=status.HTTP_200_OK)
#
#         to_delete_diary = Diary.objects.get(writer_id=user_id, pk=diary_id)
#
#         if to_delete_diary is not None:
#             to_delete_diary.delete()
#             return Response({'result_msg' : 'delete 완료'}, status=status.HTTP_200_OK)
#
# class DiaryInPeriodView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         queryset = self.get_queryset(request)
#
#         # user_diary_list = queryset.filter(date__range=(from_date,to_date)).order_by('-date')
#
#         # diary_serializer = DiaryDetailSerializer(user_diary_list, many=True)
#
#         try:
#             diary_serializer = DiaryDetailSerializer(queryset, many=True)
#             # image_serializer = ImageModelSerializer(diary=diary_serializer, many=True)
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': self.kwargs['userId'],
#                     'diary': diary_serializer.data
#             }, status=status.HTTP_200_OK)
#             # image_serializer = ImageModelSerializer(diary_uid=)
#         except:
#             return Response({'error_msg' : 'data를 불러오지 못했습니다'}, status=status.HTTP_200_OK)
#
#
#     def get_queryset(self, request, *args, **kwargs):
#         user_id = self.kwargs['userId']
#         from_date = request.data['fromDate']
#         to_date = request.data['toDate']
#
#         LoggerHandler.server_logger.debug(user_id)
#         queryset = Diary.objects.filter(writer_id=user_id,date__range=(from_date,to_date)).order_by('-date')
#         return queryset
#
# class MyPageAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#
#     def get(self, request, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '해당 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         user_serializer = MyPageModelGetSerializer(instance=user)
#
#         if user_serializer is not None:
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': user_serializer.data['userId'],
#                     'userEmail': user_serializer.data['userEmail'],
#                     'userNickname': user_serializer.data['userNickname'],
#                     'userPwd': user_serializer.data['userPwd'],
#                     'userProfileImage' : user_serializer.data['userProfileImage'],
#                     'createdAt': user_serializer.data['createdAt']
#                 }, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'result_msg': '해당 user 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         user_email = request.data['userEmail']
#         user_nickname = request.data['userNickname']
#         user_pwd = request.data['userPwd']
#
#         # 업로드 할 파일
#         image_file = None
#         if 'userProfileImage' not in request.data:
#             image_file = None
#         else:
#             image_file = request.data['userProfileImage']
#
#
#         # 업로드 할 파일이 없는 경우 --> 다이어리만 저장 후 바로 response
#         if image_file is None:
#             User.objects.filter(id=user_id).update(
#                 email=user_email,
#                 nickname=user_nickname,
#                 pwd=user_pwd,
#                 profile_image=None,
#                 modified_time=datetime.now()
#             )
#
#             user = User.objects.get(pk=user_id)
#             user_serializer = MyPageModelGetSerializer(instance=user)
#
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': user_serializer.data['userId'],
#                     'userEmail': user_serializer.data['userEmail'],
#                     'userNickname': user_serializer.data['userNickname'],
#                     'userPwd': user_serializer.data['userPwd'],
#                     'userProfileImage' : user_serializer.data['userProfileImage'],
#                     'modifiedAt': user_serializer.data['modifiedAt']
#                 }
#                 , status=status.HTTP_201_CREATED)
#
#         s3_file_name = upload_file(image_file, user.pk)
#
#         s3_url = 'https://%s/' % (settings.AWS_S3_CUSTOM_DOMAIN)
#
#         s3_url = s3_url + s3_file_name
#
#         User.objects.filter(id=user_id).update(
#             email=user_email,
#             nickname=user_nickname,
#             pwd=user_pwd,
#             profile_image=s3_url,
#             modified_time=datetime.now()
#         )
#
#         user = User.objects.get(pk=user_id)
#         user_serializer = MyPageModelGetSerializer(instance=user)
#
#         return Response(
#             {
#                 'id': 0,
#                 'userId': user_serializer.data['userId'],
#                 'userEmail': user_serializer.data['userEmail'],
#                 'userNickname': user_serializer.data['userNickname'],
#                 'userPwd': user_serializer.data['userPwd'],
#                 'userProfileImage': user_serializer.data['userProfileImage'],
#                 'modifiedAt': user_serializer.data['modifiedAt']
#                 # }
#             }
#             , status=status.HTTP_201_CREATED)
#
#     def delete(self, request, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '삭제할 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         to_delete_user = User.objects.get(pk=user_id)
#
#         if to_delete_user is not None:
#             to_delete_user.delete()
#             return Response({'result_msg': '사용자 탈퇴 완료'}, status=status.HTTP_200_OK)
#
# class MyPetListAPIView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     parser_classes = (MultiPartParser, FormParser, JSONParser)
#
#     def get(self,request,*args,**kwargs):
#         user_id = int(self.kwargs['userId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '해당 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         try:
#             pet_queryset = Pet.objects.filter(companion_id=user_id)
#             pet_serializer = PetDetailModelSerializer(pet_queryset, many=True)
#             return Response(
#                 {
#                     'id': 0,
#                     'userId': user_id,
#                     'pet': pet_serializer.data
#                 }, status=status.HTTP_200_OK)
#         except:
#             return Response({'err_detail': 'data를 불러오지 못했습니다'}, status=status.HTTP_200_OK)
#
#     def post(self,request, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '해당 user 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         pet_name = request.data['petName']
#         pet_sex = request.data['petSex']
#         pet_birthday = request.data['petBirthDay']
#         pet_species = request.data['petSpecies']
#
#         # 업로드 할 파일
#         image_file = None
#         if 'petProfileImage' not in request.data:
#             image_file = None
#             s3_url = None
#         else:
#             image_file = request.data['petProfileImage']
#
#         # 업로드 할 파일이 없는 경우 --> 다이어리만 저장 후 바로 response
#         if image_file is not None:
#             s3_file_name = upload_file(image_file, user.pk)
#
#             s3_url = 'https://%s/' % (settings.AWS_S3_CUSTOM_DOMAIN)
#
#             s3_url = s3_url + s3_file_name
#
#         pet = Pet.objects.create(
#             name=pet_name,
#             birthday=pet_birthday,
#             sex=pet_sex,
#             species=pet_species,
#             profile_image=s3_url,
#             companion_id=user
#         )
#
#         pet_serializer = PetDetailModelSerializer(instance=pet)
#
#         return Response(
#             {
#                 'id': 0,
#                 'userId': user_id,
#                 'petId': pet_serializer.data['petId'],
#                 'petName': pet_serializer.data['petName'],
#                 'petBirthDay': pet_serializer.data['petBirthDay'],
#                 'petSex': pet_serializer.data['petSex'],
#                 'petSpecies': pet_serializer.data['petSpecies'],
#                 'petProfileImage': pet_serializer.data['petProfileImage'],
#                 'createdAt': pet_serializer.data['createdAt']
#             }
#             , status=status.HTTP_201_CREATED)
#
# class MyPetDetailAPIView(APIView):
#     def get(self,request,*args,**kwargs):
#         user_id = int(self.kwargs['userId'])
#         pet_id = int(self.kwargs['petId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '해당 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         try:
#             pet_query = Pet.objects.get(pk=pet_id)
#         except:
#             return Response({
#                 'id': 0,
#                 'userId': user_id,
#                 'error_msg': '등록된 주인님이 없습니다.'
#             }, status=status.HTTP_200_OK)
#
#         pet_serializer = PetDetailModelSerializer(instance=pet_query)
#
#         return Response(
#             {
#                 'id': 0,
#                 'userId': user_id,
#                 'petId': pet_serializer.data['petId'],
#                 'petName': pet_serializer.data['petName'],
#                 'petBirthDay': pet_serializer.data['petBirthDay'],
#                 'petSex': pet_serializer.data['petSex'],
#                 'petSpecies': pet_serializer.data['petSpecies'],
#                 'petProfileImage': pet_serializer.data['petProfileImage'],
#                 'createdAt': pet_serializer.data['createdAt']
#             }
#             , status=status.HTTP_201_CREATED)
#
#     def put(self, request, *args, **kwargs):
#         user_id = self.kwargs['userId']
#         pet_id = self.kwargs['petId']
#
#         user_id = int(self.kwargs['userId'])
#         pet_id = int(self.kwargs['petId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '해당 사용자 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#         try:
#             pet_query = Pet.objects.get(pk=pet_id)
#         except:
#             return Response({
#                 'id': 0,
#                 'userId': user_id,
#                 'result_msg': '등록된 주인님이 없습니다.'
#             }, status=status.HTTP_200_OK)
#
#         pet_name = request.data['petName']
#         pet_sex = request.data['petSex']
#         pet_birthday = request.data['petBirthDay']
#         pet_species = request.data['petSpecies']
#
#         # 업로드 할 파일
#         image_file = None
#         if 'petProfileImage' not in request.data:
#             image_file = None
#             s3_url = None
#         else:
#             image_file = request.data['petProfileImage']
#
#         # 업로드 할 파일이 없는 경우 --> 다이어리만 저장 후 바로 response
#         if image_file is not None:
#             s3_file_name = upload_file(image_file, user.pk)
#             # print(s3_file_name)
#
#             s3_url = 'https://%s/' % (settings.AWS_S3_CUSTOM_DOMAIN)
#
#             s3_url = s3_url + s3_file_name
#
#             # received_data_to_json = json.loads(received_data)
#
#         pet = Pet.objects.filter(id=pet_id).update(
#             name=pet_name,
#             birthday=pet_birthday,
#             sex=pet_sex,
#             species=pet_species,
#             profile_image=s3_url,
#             companion_id=user,
#             modified_time=datetime.now()
#         )
#
#         pet = Pet.objects.get(id=pet_id)
#
#         pet_serializer = PetDetailModelSerializer(instance=pet)
#
#         return Response(
#             {
#                 'id': 0,
#                 'userId': user_id,
#                 'petId': pet_serializer.data['petId'],
#                 'petName': pet_serializer.data['petName'],
#                 'petBirthDay': pet_serializer.data['petBirthDay'],
#                 'petSex': pet_serializer.data['petSex'],
#                 'petSpecies': pet_serializer.data['petSpecies'],
#                 'petProfileImage': pet_serializer.data['petProfileImage'],
#                 'modifiedAt': pet_serializer.data['modifiedAt']
#             }
#             , status=status.HTTP_201_CREATED)
#
#     def delete(self, request, *args, **kwargs):
#         user_id = int(self.kwargs['userId'])
#         pet_id = int(self.kwargs['petId'])
#
#         try:
#             user = User.objects.get(pk=user_id)
#         except:
#             return Response({'error_msg': '해당 user 정보가 없습니다.'}, status=status.HTTP_200_OK)
#
#
#         try:
#             pet_query = Pet.objects.get(pk=pet_id)
#         except:
#             return Response({
#                 'id': 0,
#                 'userId': user_id,
#                 'result_msg': '등록된 주인님이 없습니다.'
#             }, status=status.HTTP_200_OK)
#
#
#         to_delete_pet = Pet.objects.get(pk=pet_id)
#
#         if to_delete_pet is not None:
#             to_delete_pet.delete()
#             return Response({'result_msg': '주인님 삭제가 완료되었습니다.'}, status=status.HTTP_200_OK)
#
# class ImageUploadTestAPIView(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (MultiPartParser, FormParser)
#
#     # LoggerHandler.server_logger.debug('ImageUpload')
#
#     def post(self,request, *args, **kwargs):
#         file = request.data['file']
#         LoggerHandler.server_logger.debug('ImageUpload ')
#
#         f = json.dumps(request.data['user'])
#         LoggerHandler.server_logger.debug(f)
#
#         user_id = int(request.data['user'])
#         user = User.objects.get(pk=user_id)
#         LoggerHandler.server_logger.debug(user)
#
#
#         title = request.data['title']
#         body = request.data['body']
#
#         diary = Diary.objects.create(
#             writer=user,
#             title=title,
#             body=body,
#             date=datetime.now()
#         )
#
#         request.data['diary_no'] = diary.pk
#         print(type(request.data))
#         LoggerHandler.server_logger.debug(diary.pk)
#
#         # image_serializer = ImageFileUploadTestSerializer(data=request.data)
#         #
#         # if image_serializer.is_valid():
#         #     image_serializer.save()
#         #
#         #     send_data = {
#         #         'diary_id': diary.pk,
#         #         'title': diary.title,
#         #         'body': diary.body
#         #     }
#         #     data_json = json.dumps(send_data)
#         #
#         #     return Response({'diary' : send_data,'image_data':image_serializer.data}, status=status.HTTP_201_CREATED)
#         # else:
#         #     return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# def get_date(self, str):
#     converted_date = datetime.strptime(str, "%Y-%m-%d").date()
#     print('converted_date', end=' : ')
#     print(converted_date)
#     return converted_date
#
# #
# # def s3_url(self, file_name):
# #