from django.db import models
from datetime import date

class CommonInfo(models.Model):
    name = models.CharField("Tên", max_length=100)

    class Meta:
        abstract = True
        ordering = ["name"]

class Place(models.Model):
    name = models.CharField(max_length=50, help_text="Nhập tên địa điểm")
    address = models.CharField(max_length=80, help_text="Nhập địa chỉ")

    def __str__(self):
        return self.name

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False, help_text="Có phục vụ hot dog không?")
    serves_pizza = models.BooleanField(default=False, help_text="Có phục vụ pizza không?")

    place_ptr = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.name} (Restaurant)"

class Supplier(Place):
    customers = models.ManyToManyField(Place, related_name='providers', help_text="Chọn các khách hàng của nhà cung cấp")

    def __str__(self):
        return f"{self.name} (Supplier)"

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        pass

class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True

class NewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class MyPersonWithManager(Person):
    objects = NewManager()

    class Meta:
        proxy = True

class Album(models.Model):
    artist = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='albums', verbose_name="Nhạc sĩ")
    name = models.CharField("Tên album", max_length=100, help_text="Nhập tên album")
    release_date = models.DateField("Ngày phát hành", help_text="Nhập ngày phát hành album")
    num_stars = models.IntegerField("Số sao đánh giá", help_text="Nhập số sao đánh giá album")

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save(**kwargs)

class Musician(CommonInfo):
    first_name = models.CharField("Tên đầu tiên của nhạc sĩ", max_length=50, help_text="Nhập tên đầu tiên của nhạc sĩ")
    last_name = models.CharField("Họ của nhạc sĩ", max_length=50, help_text="Nhập họ của nhạc sĩ")
    instrument = models.CharField("Loại nhạc cụ", max_length=100, help_text="Nhập loại nhạc cụ")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, **kwargs):
        super().save(**kwargs)

class Fruit(CommonInfo):
    name = models.CharField("Tên loại trái cây", max_length=100, help_text="Nhập tên của loại trái cây", unique=True)

    def __str__(self):
        return self.name

class Manufacturer(CommonInfo):
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Nhà sản xuất")
    model = models.CharField("Mô hình xe", max_length=100)

    def __str__(self):
        return self.model

class Group(models.Model):
    name = models.CharField("Tên nhóm", max_length=128)
    members = models.ManyToManyField(Person, through="Membership", related_name="%(app_label)s_%(class)s_members", verbose_name="Danh sách thành viên")

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Người tham gia", related_name="%(app_label)s_%(class)s_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Nhóm", related_name="%(app_label)s_%(class)s_memberships")
    date_joined = models.DateField("Ngày tham gia")
    invite_reason = models.CharField("Lý do mời", max_length=64)

    def __str__(self):
        return f"{self.person.first_name} - {self.group.name}"

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"

    def __str__(self):
        return f"Ox with horn length {self.horn_length}"

class PersonWithStatus(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class EntryManager(models.Manager):
    pass
#queryset
class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)
    objects = models.Manager()
    entries = EntryManager()

    def __str__(self):
        return self.headline

class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = models.JSONField(null=True)

    def __str__(self):
        return self.name

class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    details = models.TextField()

class Event(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
    )
    date = models.DateField()

class City(models.Model):
    pass

class Person(models.Model):
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

class Book(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)

class Topping(models.Model):
    name = models.CharField(max_length=30)

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return f"{self.name} ({', '.join(topping.name for topping in self.toppings.all())})"
