from .models import Book
from django.shortcuts import render

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