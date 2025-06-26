from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password', 'birth_date', 'phone_number']

    def create(self, validated_data): #입력받은 유저 데이터 저장을 처리한다. 
        user = User.objects.create(   #전달받은 데이터 중 이메일과 유저네임 정보는 그대로 넣어주고 비밀번호는 set_password 함수를 이용하여 암호화한 후 저장
            email=validated_data['email'],
            username=validated_data['username'],
            birth_date=validated_data.get('birth_date'),      
            phone_number=validated_data.get('phone_number') 
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data): #입력받은 데이터의 유효성을 검증함
        email=data.get('email',None)
        password=data.get('password',None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)

                data = {
                    'id': user.id,
                    'email': user.email ,
                    'access_token': access
                }
                return data
