from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Job, Category
from users.models import User


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobDetailSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Job
        fields = "__all__"


class JobListSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    address = SerializerMethodField()

    def get_address(self, job):
        return job.author.location.name

    class Meta:
        model = Job
        fields = "__all__"
