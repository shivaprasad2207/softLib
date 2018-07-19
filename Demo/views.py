from  .  import  categories  as libCateGories
from  .  import  entries as entries
from  .  import  book as bookLibs


def manageBooks(request):
    return bookLibs.manageBooks(request)

def showCategoryAddForm(request):
    return libCateGories.showCategoryAddForm(request)

def subCategory ( request ):
    return libCateGories.subCategory(request)

def subCategoryChannge (request):
    return libCateGories.subCategoryChannge(request)

def categoryList (request):
    return libCateGories.categoryList(request)

def deleteCategory (request):
    return libCateGories.deleteCategory(request)

def modifyCategory (request):
    return libCateGories.modifyCategory(request)

def book (request):
    return bookLibs.book(request)

def login(request):
    return entries.login(request)

def main (request ):
    return entries.main(request)

def orgRegistry(request):
    return entries.orgRegistry(request)

def userAdd(request):
    return entries.userAdd(request)

def logout (request):
    return entries.logout(request)
