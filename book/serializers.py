from django.db import transaction
from rest_framework import serializers

from book.models import Book, Author, Menu, Store, BookInStore


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publisher', 'published_date', 'available_copies', 'total_copies']


class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']


class MenuInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'title', 'pages']


# Author
class AuthorListSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'books']

    @classmethod
    def get_books(cls, obj):
        return [{
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'published_date': book.published_date,
            'available_copies': book.available_copies,
            'total_copies': book.total_copies,
        } for book in obj.books.all()]


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
    authors = serializers.SerializerMethodField()
    menus = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'available_copies', 'total_copies', 'authors', 'menus']

    @classmethod
    def get_menus(cls, obj):
        return [{
            'id': menu.id,
            'title': menu.title,
            'pages': menu.pages
        } for menu in obj.menus.all()]

    @classmethod
    def get_authors(cls, obj):
        return [{
            'id': author.id,
            'first_name': author.first_name,
            'last_name': author.last_name
        } for author in obj.authors.all()]


class BookCreateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True
    )
    menus = MenuInfoSerializer(many=True, read_only=True)
    menu_list = serializers.JSONField(default=list)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publisher', 'published_date', 'available_copies', 'total_copies',
                  'menu_list', 'menus']
        extra_kwargs = {
            'menu_list': {'write_only': True},
            'menus': {'read_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        menu_list = validated_data.pop('menu_list', [])
        book = Book.objects.create(**validated_data)
        if authors:
            book.authors.set(authors)

        bulk_info = []
        for item in menu_list:
            bulk_info.append(Menu(book=book, **item))

        book.menus.all().delete()
        Menu.objects.bulk_create(bulk_info)

        return book


class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorInfoSerializer(many=True, read_only=True)
    menus = MenuInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publisher', 'published_date', 'available_copies', 'total_copies',
                  'demo_file', 'menus']


class BookUpdateSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True
    )
    menu_list = serializers.JSONField(default=list)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'publisher', 'published_date', 'available_copies', 'total_copies',
                  'menu_list']

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', [])

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if len(authors) != 0:
            authorsInstances = []
            for author in authors:
                authorsInstances.append(Author.objects.get(id=author.id))
            instance.authors.set(authorsInstances)

        menu_list = validated_data.pop('menu_list', [])
        if authors:
            instance.authors.set(authors)

        bulk_info = []
        for item in menu_list:
            bulk_info.append(Menu(book=instance, **item))

        instance.menus.all().delete()
        Menu.objects.bulk_create(bulk_info)

        return instance


class BookUploadDemoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'demo_file']


# Store
class BookInStoreSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = BookInStore
        fields = ['book', 'copies']


class StoreCreateSerializer(serializers.ModelSerializer):
    book_in_store = BookInStoreSerializer(many=True, write_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'book_in_store']

    def create(self, validated_data):
        book_in_store = validated_data.pop('book_in_store', [])
        store = Store.objects.create(**validated_data)

        for book in book_in_store:
            BookInStore.objects.create(store=store, **book)

        return store


class StoreListSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'updated_at', 'created_at', 'books']

    @classmethod
    def get_books(cls, obj):
        book_in_store = BookInStore.objects.filter(store=obj)
        return [{
            'id': bis.book.id,
            'title': bis.book.title,
            'publisher': bis.book.publisher,
            'published_date': bis.book.published_date,
            'copies': bis.copies,
            'sold_copies': bis.sold_copies,
            'remaining_copies': bis.remaining_copies,
        } for bis in book_in_store]


class StoreUpdateSerializer(serializers.ModelSerializer):
    book_in_store = BookInStoreSerializer(many=True, write_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'book_in_store']

    def update(self, instance, validated_data):
        book_in_store = validated_data.pop('book_in_store', [])
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        for bis_data in book_in_store:
            book = bis_data['book']
            copies = bis_data['copies']

            book_in_store_obj, created = BookInStore.objects.get_or_create(
                store=instance, book=book,
                defaults={'copies': copies}
            )

            if not created:
                book_in_store_obj.copies = copies
                book_in_store_obj.save()

        return instance


class StoreTransBookToStoreSerializer(serializers.Serializer):
    from_store_id = serializers.UUIDField()
    to_store_id = serializers.UUIDField()
    book_id = serializers.UUIDField()
    copies = serializers.IntegerField(min_value=1)

    def validate(self, data):
        from_store_id = data.get('from_store_id')
        to_store_id = data.get('to_store_id')
        book_id = data.get('book_id')
        copies = data.get('copies')

        if from_store_id == to_store_id:
            raise serializers.ValidationError("from_store_id and to_store_id must not be the same")

        # Check exists store
        try:
            from_store = Store.objects.get(id=from_store_id)
        except:
            raise serializers.ValidationError("from_store_id does not exist")

        try:
            to_store = Store.objects.get(id=to_store_id)
        except:
            raise serializers.ValidationError("to_store_id does not exist")

        try:
            book_in_store = BookInStore.objects.get(store=from_store, book_id=book_id)
        except:
            raise serializers.ValidationError("BookInStore does not exist")

        if book_in_store.copies < copies:
            raise serializers.ValidationError("copies cannot be less than the number of copies")

        return data

    def create(self, validated_data):
        from_store_id = validated_data['from_store_id']
        to_store_id = validated_data['to_store_id']
        book_id = validated_data['book_id']
        copies = validated_data['copies']

        from_store = Store.objects.get(id=from_store_id)
        to_store = Store.objects.get(id=to_store_id)
        book = Book.objects.get(id=book_id)

        from_bis = BookInStore.objects.get(store=from_store, book=book)
        from_bis.copies -= copies
        from_bis.save()

        to_bis, created = BookInStore.objects.get_or_create(
            store=to_store,
            book=book,
            defaults={'copies': 0}
        )
        to_bis.copies += copies
        to_bis.save()

        return {
            'from_store_id': from_store_id,
            'to_store_id': to_store_id,
            'book_id': book_id,
            'copies_transferred': copies,
        }


class BookMultiSaleItemSerializer(serializers.Serializer):
    store_id = serializers.UUIDField()
    book_id = serializers.UUIDField()
    sold_copies = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            bis = BookInStore.objects.get(store__id=data['store_id'], book__id=data['book_id'])
        except BookInStore.DoesNotExist:
            raise serializers.ValidationError(f"BookInStore not found for book {data['book_id']}")

        if data['sold_copies'] > bis.remaining_copies:
            raise serializers.ValidationError(f"Not enough remaining copies for book {bis.book.title}")

        data['book_in_store'] = bis
        return data


class BookMultiSaleSerializer(serializers.Serializer):
    sales = BookMultiSaleItemSerializer(many=True)

    def validate(self, data):
        if not data.get('sales'):
            raise serializers.ValidationError("Sales list cannot be empty.")
        return data

    @transaction.atomic
    def create(self, validated_data):
        updated_items = []
        for sale_data in validated_data['sales']:
            bis = sale_data['book_in_store']
            sold_copies = sale_data['sold_copies']
            bis.sold_copies += sold_copies
            bis.save()
            updated_items.append({
                'store_id': bis.store_id,
                'book_id': bis.book_id,
                'book_title': bis.book.title,
                'copies': bis.copies,
                'sold_copies': bis.sold_copies,
                'remaining_copies': bis.remaining_copies
            })
        return updated_items

