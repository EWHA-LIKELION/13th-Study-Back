from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','password','email','first_name','last_name','image','part','generation','level',)

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['email'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            image = validated_data['image'],
            part = validated_data['part'],
            generation = validated_data['generation'],
            level = validated_data['level'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)

            if user.check_password(password):
                token = RefreshToken.for_user(user)

                return {
                    'access_token': str(token.access_token),
                    'refresh_token': str(token),
                }
            else:
                raise serializers.ValidationError()