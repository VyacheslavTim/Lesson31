from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserListSerializer(ModelSerializer):
    total_ads = SerializerMethodField()

    def get_total_ads(self, user):
        return user.job_set.filter(is_published=True).count()

    class Meta:
        model = User
        exclude = ["username"]


class UserDetailSerializer(ModelSerializer):
    location = SlugRelatedField(queryset=Location.objects.all(), slug_field="name")

    class Meta:
        model = User
        exclude = ["password"]


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
