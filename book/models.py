import uuid
from django.db import models


class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(CommonModel):
    title = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    available_copies = models.IntegerField(blank=True, null=True)
    total_copies = models.IntegerField(blank=True, null=True)
    demo_file = models.FileField(upload_to="books/", null=True)

    def __str__(self):
        return f"{self.title}"


class Author(CommonModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    books = models.ManyToManyField('book.Book', related_name='authors', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Store(CommonModel):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class BookInStore(CommonModel):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    copies = models.IntegerField(default=0)
    sold_copies = models.IntegerField(default=0)

    @property
    def remaining_copies(self):
        return max(self.copies - self.sold_copies, 0)

    class Meta:
        unique_together = ('store', 'book')

    def __str__(self):
        return f"{self.book.title} @ {self.store.name} ({self.copies} copies)"

class Menu(CommonModel):
    title = models.CharField(max_length=200)
    pages = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey('book.Book', related_name='menus', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
