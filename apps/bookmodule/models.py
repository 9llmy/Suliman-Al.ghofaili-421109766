from django.db import models

# جدول عناوين الطلاب من اللاب الماضي (خله زي ما هو)
class Address(models.Model):
    city = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

# ----------------- الجداول الجديدة للاب 9 -----------------

# جدول الناشر
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

# جدول المؤلف
class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)

# جدول الكتب (تم تحديثه)
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField()
    rating = models.SmallIntegerField(default=1)
    
    # العلاقات
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Author)