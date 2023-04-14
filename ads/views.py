import json

# from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
# from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Job, Selection
from ads.permissions import IsOwner, IsStaff
from ads.serializers import JobSerializer, JobDetailSerializer, JobListSerializer, SelectionSerializer, \
    SelectionCreateSerializer, CategorySerializer
from users.models import User

PAGE_NUMBER = 4


# Create your views here.


def root(request):
    return JsonResponse({"status": "ok"})


class CatViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class JobDetailView(DetailView):
    model = Job

    def get(self, request, *args, **kwargs):
        job = self.get_object()
        return JsonResponse({"id": job.pk,
                             "name": job.name,
                             "author": f"{job.author.first_name} {job.author.last_name}",
                             "category": job.category.name,
                             "price": job.price,
                             "description": job.description,
                             "is_published": job.is_published
                             })


class JobViewSet(ModelViewSet):
    default_serializer = JobSerializer
    queryset = Job.objects.order_by("-price")
    serializers = {
                   "retrieve": JobDetailSerializer,
                   "list": JobListSerializer
                   }

    default_permission = [AllowAny]
    permissions = {"retrieve": [IsAuthenticated],
                   "update": [IsAuthenticated, IsOwner | IsStaff],
                   "partial_update": [IsAuthenticated, IsOwner | IsStaff],
                   "destroy": [IsAuthenticated, IsOwner | IsStaff]
                   }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)
        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)

# class JobListView(ListView):
#     model = Job
#     queryset = Job.objects.order_by("-price").select_related("author")
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         paginator = Paginator(self.object_list, PAGE_NUMBER)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#
#         return JsonResponse(
#             {"total": page_obj.paginator.count,
#              "num_pages": page_obj.paginator.num_pages,
#              "items": [{"id": job.id,
#                         "name": job.name,
#                         "author_id": job.author_id,
#                         "author": job.author.first_name,
#                         "price": job.price,
#                         "description": job.description,
#                         "is_published": job.is_published,
#                         "category_id": job.category_id,
#                         "image": job.image.url if job.image else None} for job in page_obj]}
#         )
#

@method_decorator(csrf_exempt, name='dispatch')
class JobCreateView(CreateView):
    model = Job
    fields = "__all__"

    def post(self, request, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, username=ad_data["username"])
        category = get_object_or_404(Category, name=ad_data["category"])

        job = Job.objects.create(
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category=category
        )
        return JsonResponse({"id": job.id,
                             "name": job.name,
                             "author": job.author.username,
                             "category": job.category.name,
                             "price": job.price,
                             "description": job.description,
                             "is_published": job.is_published,
                             })


@method_decorator(csrf_exempt, name='dispatch')
class JobUpdateView(UpdateView):
    model = Job
    fields = "__all__"

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #     ad_data = json.loads(request.body)
    #     self.object.author = get_object_or_404(User, username=ad_data["username"])
    #     self.object.category = get_object_or_404(Category, name=ad_data["category"])
    #     self.object.price = ad_data["price"]
    #     self.object.is_published = ad_data["is_published"]
    #     self.object.description = ad_data["description"]
    #     self.object.name = ad_data["name"]
    #     self.object.save()
    #     return JsonResponse({"id": self.object.pk,
    #                          "name": self.object.name,
    #                          "author": self.object.author.username,
    #                          "category": self.object.category.name,
    #                          "price": self.object.price,
    #                          "description": self.object.description,
    #                          "is_published": self.object.is_published
    #                          }, safe=False)

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.author = get_object_or_404(User, username=ad_data["username"])
        self.object.category = get_object_or_404(Category, name=ad_data["category"])
        self.object.price = ad_data["price"]
        self.object.is_published = ad_data["is_published"]
        self.object.description = ad_data["description"]
        self.object.name = ad_data["name"]
        self.object.save()

        return JsonResponse({"id": self.object.id,
                             "name": self.object.name,
                             "author": self.object.author.username,
                             "category": self.object.category.name,
                             "price": self.object.price,
                             "description": self.object.description,
                             "is_published": self.object.is_published
                             })


@method_decorator(csrf_exempt, name='dispatch')
class JobDeleteView(DeleteView):
    model = Job
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        job_id = job.id
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": job_id}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class JobImageUpload(UpdateView):
    model = Job
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse({"name": self.object.name, "image": self.object.image.url})


# @method_decorator(csrf_exempt, name='dispatch')
# class JobListCreateView(View):
#     def get(self, request):
#         job_list = Job.objects.all()
#         return JsonResponse([{"id": job.pk,
#                               "name": job.name,
#                               "author": job.author,
#                               "price": job.price,
#                               "description": job.description,
#                               "address": job.address,
#                               "is_published": job.is_published
#                               } for job in job_list], safe=False)
#
#     def post(self, request):
#         ad_data = json.loads(request.body)
#         new_ad = Job.objects.create(**ad_data)
#         return JsonResponse({"id": new_ad.pk,
#                              "name": new_ad.name,
#                              "author": new_ad.author,
#                              "price": new_ad.price,
#                              "description": new_ad.description,
#                              "address": new_ad.address,
#                              "is_published": new_ad.is_published
#                              })

# @method_decorator(csrf_exempt, name='dispatch')
# class CatListCreateView(View):
#     def get(self, request):
#         cat_list = Category.objects.all()
#         return JsonResponse([{"id": cat.pk,
#                               "name": cat.name
#                               } for cat in cat_list], safe=False)
#
#     def post(self, request):
#         ad_data = json.loads(request.body)
#         new_cat = Category.objects.create(**ad_data)
#         return JsonResponse({"id": new_cat.pk,
#                              "name": new_cat.name
#                              })
class SelectionViewSet(ModelViewSet):
    serializer_class = SelectionSerializer
    queryset = Selection.objects.all()

    default_permission = [AllowAny]
    permissions = {"create": [IsAuthenticated],
                   "update": [IsAuthenticated, IsOwner],
                   "partial_update": [IsAuthenticated, IsOwner],
                   "destroy": [IsAuthenticated, IsOwner]
                   }

    default_serializer = SelectionSerializer
    serializers = {
        "create": SelectionCreateSerializer,
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)
