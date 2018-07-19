from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from .models import Category, SubCategory, Book, BookCopy
from .mylib.myutil import getCookieInfo, showJsonResponse


def manageBooks(request):
    t = get_template('manage_books.html')
    html = t.render(getCookieInfo(request))
    response = HttpResponse(html)
    return response

def book (request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        if request.GET.get('op', '') == 'getSubCategoryFrom':
           data['categoryId'] = request.GET.get('categoryId', '')
           categoryObj = Category.objects.filter().get(categoryId=data['categoryId'], orgCode=data['orgCode'])
           data['category'] = categoryObj.category
           data['subCategories'] = SubCategory.objects.filter(categoryId=categoryObj, orgCode=data['orgCode'])
           t = get_template('part_template.html')
           data['section'] = 'SHOW_SUBCATEGORY_OPTION'
           html = t.render(data)
           response = HttpResponse(html)
           return response
        elif request.GET.get('op', '') == 'getBookFrom':
            data['categoryId'] = request.GET.get('categoryId', '')
            data['subCategoryId'] = request.GET.get('subCategoryId', '')
            t = get_template('part_template.html')
            data['section'] = 'SHOW_REST_OF_BOOK_FORM'
            html = t.render(data)
            response = HttpResponse(html)
            return response
        else:
            data['categories'] = Category.objects.filter(orgCode=data['orgCode'], is_active=1)
            data['section'] = 'SHOW_BOOK_ADD_FORM'
            t = get_template('bookAddForm.html')
            html = t.render(data)
            response = HttpResponse(html)
            return response
    else:
        bookObj = Book()
        bookObj.categoryId = Category.objects.filter().get(categoryId=request.POST.get('categoryId', ''),orgCode=data['orgCode'])
        bookObj.subCategoryId = SubCategory.objects.filter().get(subCategoryId=request.POST.get('subCategoryId', ''))
        bookObj.bookName = request.POST.get('bookName', '')
        bookObj.author = request.POST.get('author', '')
        bookObj.publisher = request.POST.get('publisher', '')
        bookObj.isbn = request.POST.get('isbn', '')
        bookObj.remark = request.POST.get('remark', '')
        bookObj.is_cd = request.POST.get('is_cd', '')
        bookObj.copies = int (request.POST.get('copies', ''))
        bookObj.orgCode = data['orgCode']
        bookObj.save()
        for i in range(bookObj.copies):
            copy = BookCopy()
            copy.bookCopyCode = get_random_string(length=10)
            copy.bookId = bookObj
            copy.save()
        data['status'] = 'SUCCESS'
        data['message'] = '<br><b> Book Added <b>'
        return showJsonResponse(data)

def bookList (request):
    data = getCookieInfo(request)
    data['books'] = Book.objects.filter(orgCode=data['orgCode'], is_active=1)
    t = get_template('book_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response

def copies (request):
    data = getCookieInfo(request)
    bookId = request.GET.get('bookId', '')
    data['bookName'] = Book.objects.filter().get(bookId=int(bookId)).bookName
    data['copies'] = BookCopy.objects.filter(bookId=bookId, is_active=1)
    t = get_template('book_copy_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response

def deleteCopy(request):
    data = getCookieInfo(request)
    bookCopyCode = request.POST.get('bookCopyCode', '')
    bookCopyId = request.POST.get('bookCopyId', '')
    bookId = request.POST.get('bookId', '')
    orgCode = data['orgCode']
    copy = BookCopy.objects.filter().get(bookCopyId=int(bookCopyId),bookCopyCode=bookCopyCode)
    copy.is_active = 0
    copy.save()
    book = Book.objects.filter().get(bookId=int(bookId),orgCode=orgCode)
    book.copies = book.copies - 1
    book.save()
    return redirect ('/bookList/copies/?bookId=' + bookId)

def bookModify (request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        orgCode = data['orgCode']
        bookId = request.GET.get('bookId', '')
        book = Book.objects.filter().get(bookId=int(bookId), orgCode=orgCode)
        data['section'] = 'SHOW_BOOK_MOD_FORM'
        data['bookName'] = book.bookName
        data['author'] = book.author
        data['publisher'] = book.publisher
        data['is_cd'] = book.is_cd
        data['remark'] = book.remark
        data['isbn'] = book.isbn
        data['bookId'] = book.bookId
        t = get_template('bookAddForm.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response
    else:
        book = Book.objects.filter().get(bookId=int(request.POST.get('bookId', '')), orgCode=data['orgCode'])
        book.bookName = request.POST.get('bookName', '')
        book.author = request.POST.get('author', '')
        book.publisher = request.POST.get('publisher', '')
        book.isbn = request.POST.get('isbn', '')
        book.remark = request.POST.get('remark', '')
        book.save()
        #is_cd = request.POST.get('bookId', '')
        return redirect('/bookList/')

def bookDelete (request):
    data = getCookieInfo(request)
    orgCode = data['orgCode']
    bookId = request.POST.get('bookId', '')
    book = Book.objects.filter().get(bookId=int(bookId), orgCode=orgCode)
    book.is_active = 0
    book.save()
    return redirect('/bookList/')

def bookAdd ( request ):
    data = getCookieInfo(request)
    copies = request.POST.get('copies', '')
    bookId = request.POST.get('bookId', '')
    orgCode = data['orgCode']
    book = Book.objects.filter().get(bookId=int(bookId),orgCode=orgCode)
    book.copies = book.copies + int (copies)
    book.save()
    for i in range(int(copies)):
        copy = BookCopy()
        copy.bookCopyCode = get_random_string(length=10)
        copy.bookId = book
        copy.save()
    return redirect('/bookList/')

def bookSearch (request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        search = {}
        search['is_active'] = 1
        search['orgCode'] = data['orgCode']
        data['books'] = Book.objects.filter(**search)
        t = get_template('bookSearchForm.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response
    else:
        searchField = request.POST.get('searchField', '')
        searchString = request.POST.get('searchString', '')
        search = {}
        search[searchField + '__contains' ] = searchString
        search['is_active'] = 1
        search['orgCode'] = data['orgCode']
        data['books'] = Book.objects.filter(**search)
        t = get_template('bookSearchForm.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response


