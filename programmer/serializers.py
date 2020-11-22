from rest_framework import serializers
from programmer.models import User
from programmer.models import Post

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        # fields = ('username','password')
        fields = '__all__'
