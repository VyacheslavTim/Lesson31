from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField()
    is_published = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ad_picture", null=True, blank=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    items = models.ManyToManyField(Job)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

        def __str__(self):
            return self.name
