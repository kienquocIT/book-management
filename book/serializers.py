from rest_framework import serializers

from book.models import Book, Author

class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title', 'publisher', 'published_date', 'available_copies', 'total_copies']

class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','first_name', 'last_name']

# Author
class AuthorListSerializer(serializers.ModelSerializer):
    books = BookInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'books']

class AuthorDetailSerializer(serializers.ModelSerializer):
    books = BookInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', "created_at", "updated_at", "books"]

class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        books = validated_data.pop('books', [])
        author = Author.objects.create(**validated_data)
        if books:
            author.books.set(books)
        return author

class AuthorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', "created_at", "updated_at", "books"]

    def update(self, instance: Author, validated_data):
        books = validated_data.pop('books', [])
        print(books[0])
        if len(books) != 0:
            booksInstances = []
            for book in books:
                booksInstances.append(Book.objects.get(id=book.id))
            instance.books.set(booksInstances)

        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        return instance

# Book
class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'authors', 'title']


class BookCreateSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(default=list)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publisher','published_date', 'available_copies', 'total_copies']

    def create(self, validated_data):
        title = validated_data.get('title')
        book = Book.objects.filter(title=title)
        if book.exists():
            raise serializers.ValidationError("Book already exists")
        else:
            authors = validated_data.pop('authors', [])
            book = Book.objects.create(**validated_data)
            if authors:
                book.authors.set(authors)
            return book


class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publisher','published_date', 'available_copies', 'total_copies']

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publisher','published_date', 'available_copies', 'total_copies']

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', [])

        if len(authors) != 0:
            authorsInstances = []
            for author in authors:
                authorsInstances.append(Author.objects.get(id=author.id))
            instance.authors.set(authorsInstances)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance




