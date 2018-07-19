from django.db import models

class RegisterOrganisation(models.Model):
    orgId = models.AutoField(primary_key=True)
    orgName = models.CharField(max_length=255, blank=True)
    orgAdress = models.CharField(max_length=255, blank=True)
    orgPhone = models.CharField(max_length=255, blank=True)
    orgEmail = models.EmailField(max_length=255, blank=True)
    orgCode =  models.CharField(max_length=255,unique=True, blank=True)
    is_active = models.IntegerField(default=1)

class UserAuth(models.Model):
    userId = models.AutoField(primary_key=True)
    orgCode = models.CharField(max_length=255, blank=True)
    userEmail = models.EmailField(max_length=255, blank=True)
    userPassword = models.CharField(max_length=255, blank=True)
    userPin = models.CharField(max_length=255, blank=True,unique=True)
    userRole = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

class UserInfo(models.Model):
    userId = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255, blank=True)
    lastName = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    adress = models.CharField(max_length=255, blank=True)

class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    orgCode = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(default=1)

class SubCategory(models.Model):
    subCategoryId = models.AutoField(primary_key=True)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    orgCode = models.CharField(max_length=255, blank=True)
    subCategory = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(default=1)

class Book(models.Model):
    bookId = models.AutoField(primary_key=True)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCategoryId = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    orgCode = models.CharField(max_length=255, blank=True)
    bookName = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=255, blank=True)
    remark = models.CharField(max_length=400, blank=True)
    is_cd = models.CharField(max_length=255, blank=True)
    copies = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

class BookCopy(models.Model):
    bookCopyId = models.AutoField(primary_key=True)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookCopyCode = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(default=1)
    is_reserved = models.IntegerField(default=0)

class Reservation(models.Model):
    reservationId = models.AutoField(primary_key=True)
    bookCopyId = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    userAuthId = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    bookCopyCode = models.CharField(max_length=255, blank=True)
    orgCode = models.CharField(max_length=255, blank=True)
    dateReserved = models.DateField()
    dateFrom = models.DateField()
    dateTo = models.DateField()
    is_active = models.IntegerField(default=1)
    is_reserved = models.IntegerField(default=0)