from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book  # نربط الفورم بجدول الكتب
        fields = '__all__'  # نطلب من الجانغو يسوي فورم لكل الحقول الموجودة في الجدول