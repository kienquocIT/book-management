import uuid
from django.db import models


class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(CommonModel):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    available_copies = models.IntegerField(blank=True, null=True)
    total_copies = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class Author(CommonModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    books = models.ManyToManyField('book.Book', related_name='authors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
