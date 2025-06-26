from django.shortcuts import render
from .models import *
from rest_framework import views
from .serializers import *
from rest_framework.response import Response


#post 메소드를 처리한다.
class SignupView(views.APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입 성공","data":serializer.data})
        return Response({"message":'회원가입 실패','error':serializer.errors})
    
class LoginView(views.APIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer=UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response({"message":'로그인 성공','data':serializer.validated_data})
        return Response({"message":'로그인 실패','error':serializer.errors})


    




    

    
    
