from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from rest_framework import serializers
from lxpapiapp.models import *
from datetime import datetime
### LXP APP Started
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_full_name = serializers.CharField()
    email = serializers.CharField()
    utype = serializers.CharField()
    mobile = serializers.CharField()
    whatsappno = serializers.CharField()
    profile_pic = serializers.ImageField()
    profile_updated = serializers.BooleanField()
    status = serializers.BooleanField()
    created =  serializers.DateTimeField()
    is_superuser = serializers.BooleanField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    last_login = serializers.DateTimeField()
    
class UserProfileSerializer(serializers.ModelSerializer):
    # You can choose the fields that can be updated
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_full_name', 'email', 'mobile', 'whatsappno', 'profile_pic', 'profile_updated',
                    'regdate','skills','bio'                  
                  ]
    