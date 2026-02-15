from django.contrib import admin
from django.urls import path, include  # 1. أضفنا include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include("apps.bookmodule.urls")),  # 2. أي رابط يبدأ بـ books نرسله لملف التطبيق
]