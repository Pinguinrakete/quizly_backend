from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirmed_password', 'email']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'required': True},
        }
    
    def validate_confirmed_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError("Passwords do not match")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Invalid credentials.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Invalid credentials.")
        return value
    
    def save(self):
        pw = self.validated_data['password']

        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        account.set_password(pw)
        account.save() 
        return account
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both fields must be filled out.")

        user = authenticate(username=username, password=password)  
        if user is None:
            raise serializers.ValidationError(("Invalid username or password."))

        attrs['user'] = user
        return attrs