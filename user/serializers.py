from django.contrib.auth import (
    get_user_model,
    authenticate
    )
from rest_framework import serializers
from django.utils.translation import gettext as _
#json input > validates it > converts to Python Object or Model
#ModelSerializer base class for model serializer

class UserSerializers(serializers.ModelSerializer):
    """
        Serializer for User Model
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'password','name']
        extra_kwargs = {'password':{'write_only': True, 'min_length':5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user

class UserTokenSerializer(serializers.Serializer):
    """
        Serializer for User Auth Token
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input type' : 'password'}, #for browser -----> swagger ui
        trim_whitespace=False #not letting DRF to remove space, by default it removes
    )
    
    def validate(self, attrs):
        """
            Autheticate User
        """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg = _("Not valid credentials")
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
