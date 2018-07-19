"""DemoProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  Demo  import  categories,reservation
from  Demo  import  entries
from  Demo  import  book
from  Demo  import  user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('orgRegistry/', entries.orgRegistry),
    path('userAdd/', entries.userAdd),
    path('login/', entries.login),
    path('main/', entries.main),
    path('logout/', entries.logout),
    path('manageBooks/',book.manageBooks),
    path('showCategoryAddForm/', categories.showCategoryAddForm),
    path('categoryList/', categories.categoryList),
    path('deleteCategory/', categories.deleteCategory),
    path('modifyCategory/', categories.modifyCategory),
    path ('subCategory/', categories.subCategory),
    path ('subCategoryChannge/', categories.subCategoryChannge),
    path ('book/', book.book),
    path ('bookList/', book.bookList),
    path ('bookList/copies/', book.copies),
    path ('bookList/copies/delete/', book.deleteCopy),
    path ('book/add/', book.bookAdd),
    path ('book/modify/', book.bookModify),
    path ('book/delete/', book.bookDelete),
    path ('book/search/', book.bookSearch),
    path ('manageUsers/', user.manageUsers),
    path ('user/', user.userAdd),
    path ('user/list/', user.userList),
    path ('user/chuser/', user.chuser),
    path ('user/delete/', user.delete),
    path ('user/modify/', user.modify),
    path ('user/search/', user.search),
    path ('bookList/copies/reserve/',reservation.setReserve),
    path('reserve/bookCopy/', reservation.status),
    path('reserve/bookCopy/delete', reservation.delete),
    path('reserve/book/reservation', reservation.bookReservation),
    path('user/reservation/', reservation.userReservations),
    path('reserve/expired/', reservation.expireReservation),
]
