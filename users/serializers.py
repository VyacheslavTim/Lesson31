from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]


class UserCreateSerializer(ModelSerializer):
    location = SlugRelatedField(required=False, queryset=Location.objects.all(), slug_field="name", many=True)

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        password = validated_data.pop("password")
        new_user = User.objects.create(**validated_data)
        new_user.set_password(password)
        new_user.save()

        for loc in self._location:
            location, _ = Location.objects.get_or_create(name=loc)
            new_user.location.add(location)
        return new_user

    class Meta:
        model = User
        fields = "__all__"


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
