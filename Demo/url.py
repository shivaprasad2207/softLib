from django.urls import path
from . import entries
from . import categories
from . import book
from . import user,reservation


urlpatterns = [
    path('', entries.orgRegistry, name='orgRegistry'),
    path('', entries.userAdd, name='userAdd'),
    path('', entries.login, name='login'),
    path('', entries.main, name='main'),
    path('', entries.logout, name='logout'),
    path('', book.manageBooks, name='manageBooks'),
    path('', categories.showCategoryAddForm, name='showCategoryAddForm'),
    path('', categories.categoryList, name='categoryList'),
    path('', categories.deleteCategory, name='deleteCategory'),
    path('', categories.modifyCategory, name='modifyCategory'),
    path('', categories.subCategory, name='subCategory'),
    path('', categories.subCategoryChannge, name='subCategoryChannge'),
    path('', book.book, name='book'),
    path('', book.bookList, name='book'),
    path('', book.copies, name='copies'),
    path('', book.deleteCopy, name='deleteCopy'),
    path('', book.bookAdd, name='bookAdd'),
    path('', book.bookModify, name='bookModify'),
    path('', book.bookDelete, name='bookDelete'),
    path('', book.bookSearch, name='bookSearch'),
    path('', user.manageUsers, name='manageUsers'),
    path('', user.userAdd, name='userAdd'),
    path('', user.userList, name='userList'),
    path('', user.chuser, name='chuser'),
    path('', user.delete, name='delete'),
    path('', user.modify, name='modify'),
    path('', user.search, name='search'),
    path('', reservation.setReserve, name='setReserve'),
    path('', reservation.status, name='status'),
    path('', reservation.delete, name='delete'),
    path('', reservation.userReservations, name='userReservations'),
    path('', reservation.expireReservation, name='expireReservation'),
]