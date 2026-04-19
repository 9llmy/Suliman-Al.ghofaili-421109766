from .models import Book
from django.db.models import Q
from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Max, Min
from .models import Book, Address, Student

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')
def links(request):
    return render(request, 'bookmodule/links.html')
def formatting(request):
    return render(request, 'bookmodule/formatting.html')
def listing(request):
    return render(request, 'bookmodule/listing.html')
def tables(request):
    return render(request, 'bookmodule/tables.html')
def getBooksList():
    book1 = {'id': 12344321, 'title': 'كتاب الداء والدواء', 'author': 'ابن قيم الجوزية'}
    book2 = {'id': 56788765, 'title': 'كتاب سير أعلام النبلاء', 'author': 'الذهبي'}
    book3 = {'id': 43211234, 'title': 'كتاب صحيح البخاري', 'author': 'الإمام البخاري'}
    return [book1, book2, book3]
def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        
        # جلب الكتب والفلترة
        books = getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower(): contained = True
            
            if contained: newBooks.append(item)
            
        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
    
    return render(request, 'bookmodule/search.html')

def init_db(request):
    # مسح البيانات القديمة (عشان لو حدثت الصفحة بالغلط ما تتكرر الكتب)
    Book.objects.all().delete()
    
    # إضافة الكتب الإسلامية مع السعر ورقم الطبعة
    Book.objects.create(title='كتاب الداء والدواء', author='ابن قيم الجوزية', price=50.0, edition=1)
    Book.objects.create(title='كتاب سير أعلام النبلاء', author='الذهبي', price=150.0, edition=3)
    Book.objects.create(title='كتاب صحيح البخاري', author='الإمام البخاري', price=120.0, edition=5)
    
    return render(request, 'bookmodule/index.html') # نرجعه للصفحة الرئيسية بعد الإضافة

def simple_query(request):
    # نبحث عن أي كتاب يحتوي عنوانه على كلمة "كتاب"
    mybooks = Book.objects.filter(title__icontains='كتاب') 
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    # تطبيق الفلاتر المتعددة لنجلب الكتب المطابقة للشروط
    mybooks = Book.objects.filter(author__isnull=False) \
                          .filter(title__icontains='كتاب') \
                          .filter(edition__gte=2) \
                          .exclude(price__lte=100)[:10]
    
    # إذا لقينا كتب مطابقة للشروط نعرضها، وإذا ما لقينا نرجعه للصفحة الرئيسية
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    
def task1(request):
    # جلب الكتب التي سعرها أقل من أو يساوي 80 باستخدام Q
    mybooks = Book.objects.filter(Q(price__lte=80))
    # راح نستخدم نفس صفحة العرض حقت اللاب الماضي عشان نوفر وقت
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task2(request):
    # ندمج الشروط بـ & (وَ) و | (أَوْ)
    mybooks = Book.objects.filter(
        Q(edition__gt=2) & (Q(title__icontains='نبلاء') | Q(author__icontains='البخاري'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task3(request):
    # استخدام علامة ~ لنفي الشروط (NOT)
    mybooks = Book.objects.filter(
        ~Q(edition__gt=2) & ~(Q(title__icontains='نبلاء') | Q(author__icontains='البخاري'))
    )
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task4(request):
    # جلب جميع الكتب وترتيبها أبجدياً حسب حقل العنوان (title)
    mybooks = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def task5(request):
    # حساب الإحصائيات للمكتبة
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/task5.html', {'stats': stats})

def init_students(request):
    # مسح البيانات القديمة لتجنب التكرار
    Student.objects.all().delete()
    Address.objects.all().delete()
    
    # إضافة مدن
    riyadh = Address.objects.create(city='الرياض')
    qassim = Address.objects.create(city='القصيم')
    
    # إضافة طلاب وربطهم بالمدن
    Student.objects.create(name='أحمد', age=20, address=riyadh)
    Student.objects.create(name='عمر', age=22, address=riyadh)
    Student.objects.create(name='سالم', age=21, address=qassim)
    Student.objects.create(name='علي', age=23, address=qassim)
    Student.objects.create(name='خالد', age=19, address=qassim)
    
    return render(request, 'bookmodule/index.html')

def task7(request):
    # دالة annotate تقوم بجمع المدن وعدّ الطلاب المرتبطين بكل مدينة
    cities = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/task7.html', {'cities': cities})