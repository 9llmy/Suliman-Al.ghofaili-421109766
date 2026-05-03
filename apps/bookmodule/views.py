from .models import Book
from django.db.models import Q
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Avg, Max, Min
from .models import Book, Address, Student, Publisher, Author
from django.utils import timezone
from datetime import date
from .forms import BookForm

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

def init_lab9(request):
    Book.objects.all().delete()
    Publisher.objects.all().delete()
    Author.objects.all().delete()

    # إضافة دور النشر
    pub1 = Publisher.objects.create(name='دار القلم', location='دمشق')
    pub2 = Publisher.objects.create(name='دار المنهاج', location='جدة')

    # إضافة المؤلفين
    auth1 = Author.objects.create(name='ابن قيم الجوزية', DOB=date(1292, 1, 1))
    auth2 = Author.objects.create(name='الذهبي', DOB=date(1274, 10, 5))

    # إضافة الكتب وربطها بالناشر
    b1 = Book.objects.create(title='كتاب الداء والدواء', price=50.0, quantity=10, pubdate=timezone.now(), rating=5, publisher=pub1)
    b1.authors.add(auth1) # ربط المؤلف بالكتاب

    b2 = Book.objects.create(title='كتاب سير أعلام النبلاء', price=150.0, quantity=5, pubdate=timezone.now(), rating=5, publisher=pub2)
    b2.authors.add(auth2)

    return render(request, 'bookmodule/index.html')

def task1_lab9(request):
    # نحسب إجمالي كمية كل الكتب في المكتبة
    total_quantity = Book.objects.aggregate(total=Sum('quantity'))['total'] or 0
    
    books = Book.objects.all()
    # نمر على كل كتاب ونحسب نسبته المئوية (كحقل مؤقت)
    for book in books:
        if total_quantity > 0:
            book.percentage = round((book.quantity / total_quantity) * 100, 2)
        else:
            book.percentage = 0.0
            
    return render(request, 'bookmodule/task1_lab9.html', {'books': books})

def task2_lab9(request):
    # نستخدم annotate عشان نحسب مجموع (Sum) حقل quantity للكتب المرتبطة بكل ناشر
    # لاحظ أننا استخدمنا book__quantity للوصول لجدول الكتب من جدول الناشر
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'bookmodule/task2_lab9.html', {'publishers': publishers})

def task3_lab9(request):
    # نستخدم annotate عشان نجيب أقدم تاريخ نشر (Min) لكل دار نشر
    publishers = Publisher.objects.annotate(oldest_book_date=Min('book__pubdate'))
    return render(request, 'bookmodule/task3_lab9.html', {'publishers': publishers})

def task4_lab9(request):
    # حساب المتوسط (Avg)، أقل سعر (Min)، وأعلى سعر (Max) لكل ناشر
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )
    return render(request, 'bookmodule/task4_lab9.html', {'publishers': publishers})

def task5_lab9(request):
    # أول شيء نفلتر الكتب اللي تقييمها 4 أو أعلى، بعدين نعدها لكل ناشر
    publishers = Publisher.objects.filter(book__rating__gte=4).annotate(book_count=Count('book'))
    return render(request, 'bookmodule/task5_lab9.html', {'publishers': publishers})

def task6_lab9(request):
    # نفلتر الكتب بناءً على الشروط المعقدة، ثم نعدّها لكل ناشر
    publishers = Publisher.objects.filter(
        book__price__gt=50,
        book__quantity__lt=5,
        book__quantity__gte=1
    ).annotate(book_count=Count('book'))
    
    return render(request, 'bookmodule/task6_lab9.html', {'publishers': publishers})

def listbooks(request):
    # جلب جميع الكتب من قاعدة البيانات
    books = Book.objects.all()
    return render(request, 'bookmodule/listbooks.html', {'books': books})

def addbook(request):
    if request.method == 'POST':
        # استلام البيانات من الفورم
        title = request.POST.get('title')
        price = request.POST.get('price')
        
        # إنشاء كتاب جديد وحفظه مع إضافة تاريخ النشر الحالي لتفادي الخطأ
        Book.objects.create(title=title, price=float(price), pubdate=timezone.now())
        
        # بعد الحفظ، نرجع المستخدم لصفحة عرض الكتب
        return redirect('books.listbooks')
    
    # إذا كان الطلب GET، نعرض له صفحة الفورم
    return render(request, 'bookmodule/addbook.html')

def editbook(request, id):
    # جلب الكتاب المطلوب من قاعدة البيانات باستخدام الـ ID
    book = Book.objects.get(id=id)
    
    if request.method == 'POST':
        # تحديث بيانات الكتاب بالبيانات الجديدة الجاية من الفورم
        book.title = request.POST.get('title')
        book.price = float(request.POST.get('price'))
        
        # حفظ التعديلات
        book.save()
        
        # الرجوع لقائمة الكتب
        return redirect('books.listbooks')
    
    # إذا كان الطلب GET، نعرض صفحة التعديل ونرسل لها بيانات الكتاب الحالية
    return render(request, 'bookmodule/editbook.html', {'book': book})

def deletebook(request, id):
    # نجيب الكتاب من قاعدة البيانات باستخدام الـ ID
    book = Book.objects.get(id=id)
    
    # نحذف الكتاب نهائياً
    book.delete()
    
    # نرجع المستخدم لقائمة الكتب عشان يشوف أن الكتاب اختفى
    return redirect('books.listbooks')

def addbook_part2(request):
    if request.method == 'POST':
        # نمرر البيانات اللي جاتنا من المستخدم للفورم
        form = BookForm(request.POST)
        
        # حارس الأمن (is_valid) يتأكد إن البيانات صحيحة 100%
        if form.is_valid():
            form.save()  # سطر واحد يحفظ البيانات في قاعدة البيانات!
            return redirect('books.listbooks') # نرجع لقائمة الكتب مؤقتاً
    else:
        # إذا كان الطلب GET، نرسل فورم فاضي
        form = BookForm()
        
    return render(request, 'bookmodule/addbook_part2.html', {'form': form})

def editbook_part2(request, id):
    # نجيب الكتاب اللي نبي نعدله
    book = Book.objects.get(id=id)
    
    if request.method == 'POST':
        # نمرر البيانات الجديدة، ونقول للجانغو "حدث هذا الكتاب بالذات" باستخدام instance
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books.listbooks') # نرجع للقائمة بعد الحفظ
    else:
        # إذا كان الطلب GET، نرسل الفورم معبأ ببيانات الكتاب الحالية
        form = BookForm(instance=book)
        
    return render(request, 'bookmodule/editbook_part2.html', {'form': form, 'book': book})