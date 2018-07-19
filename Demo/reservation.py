from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from .models import  Book, BookCopy , Reservation, UserAuth, UserInfo
from .mylib.myutil import getCookieInfo, showJsonResponse
from datetime import datetime
import json

def userReservations (request):
    data = getCookieInfo(request)
    userAuthId = request.GET.get('userAuthId', '')
    userInfoId = request.GET.get('userInfoId', '')
    data['user'] = getUserInfo  (userInfoId,data['orgCode'])
    data['userAuthId'] = userAuthId
    data['userInfoId'] = userInfoId
    data['reservations']  = getUserReservation (userInfoId,data['orgCode'])
    #print(json.dumps(data, indent=4, sort_keys=True))
    t = get_template('user_reservation_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response


def getUserInfo(userAuthId,orgCode):
    userAuth = UserAuth.objects.filter(userId=userAuthId, is_active=1).get()
    userInfo = UserInfo.objects.filter(userId=userAuth).get()
    user = {}
    user['firstName'] = userInfo.firstName
    user['lastName'] = userInfo.lastName
    user['phone'] = userInfo.phone
    user['adress'] = userInfo.adress
    user['email'] = userAuth.userEmail
    return user

def expireReservation(request):
    data = getCookieInfo(request)
    data['reservations']= getExpiredReservation(data['orgCode'])
    t = get_template('expired_reservation_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response

def getExpiredReservation(orgCode):
    #dateNow = datetime.today().strftime('%Y-%m-%d')
    dateNow = '2018-07-22'
    reservs = Reservation.objects.filter(
                                            dateTo__lt=datetime.strptime(dateNow, '%Y-%m-%d'),
                                            orgCode=orgCode,
                                            is_active= 1,
                                            is_reserved = 1
             )
    copyReservations = []
    for reserv in reservs:
        copyReserv = {}
        copyReserv['dateFrom'] = str(reserv.dateFrom)
        copyReserv['dateTo'] = str(reserv.dateTo)
        copyReserv['dateReserved'] = str(reserv.dateReserved)
        copyReserv['reservationId'] = reserv.reservationId
        copyReserv['bookCopyCode'] = reserv.bookCopyCode
        copyReserv['bookCopyId'] = reserv.bookCopyId.bookCopyId
        copy = BookCopy.objects.filter(bookCopyCode=copyReserv['bookCopyCode'],
                                       bookCopyId=int(copyReserv['bookCopyId'])).get()
        copyReserv['bookId'] = copy.bookId.bookId
        copyReserv['bookName'] = Book.objects.filter(bookId=copyReserv['bookId']).get().bookName
        userAuthId = reserv.userAuthId.userId
        userAuth = UserAuth.objects.filter(userId=int(userAuthId), is_active=1).get()
        userInfo = UserInfo.objects.filter(userId=userAuth).get()
        copyReserv['firstName'] = userInfo.firstName
        copyReserv['lastName'] = userInfo.lastName
        copyReserv['phone'] = userInfo.phone
        copyReserv['adress'] = userInfo.adress
        copyReserv['email'] = userAuth.userEmail
        copyReservations.append(copyReserv)
    #print(json.dumps(copyReservations, indent=4, sort_keys=True))
    return copyReservations

def getUserReservation (userAuthId,orgCode):
    userAuth = UserAuth.objects.filter(userId=userAuthId, is_active=1).get()
    userInfo = UserInfo.objects.filter(userId=userAuth).get()
    reservs = Reservation.objects.filter(is_active=1, is_reserved=1,orgCode=orgCode,userAuthId = userAuth)
    copyReservations = []
    for reserv in reservs:
        copyReserv = {}
        copyReserv['dateFrom'] = str(reserv.dateFrom)
        copyReserv['dateTo'] = str(reserv.dateTo)
        copyReserv['dateReserved'] = str(reserv.dateReserved)
        copyReserv['reservationId'] = reserv.reservationId
        copyReserv['bookCopyCode'] = reserv.bookCopyCode
        copyReserv['bookCopyId'] = reserv.bookCopyId.bookCopyId
        copy = BookCopy.objects.filter(bookCopyCode=copyReserv['bookCopyCode'],bookCopyId=int(copyReserv['bookCopyId'])).get()
        copyReserv['bookId'] = copy.bookId.bookId
        copyReserv['bookName'] = Book.objects.filter(bookId=copyReserv['bookId']).get().bookName
        copyReservations.append(copyReserv)
    #print(json.dumps(copyReservations, indent=4, sort_keys=True))
    return copyReservations

def getReservationOfBookCopy(bookCopyId,bookCopyCode):
    reservs = Reservation.objects.filter(
        bookCopyId=bookCopyId, bookCopyCode=bookCopyCode,
        is_active=1, is_reserved=1
    )
    copyReservations = []
    for reserv in reservs:
        copyReserv = {}
        userAuth = UserAuth.objects.filter(userId=reserv.userAuthId.userId, is_active=1).get()
        userInfo = UserInfo.objects.filter(userId=userAuth).get()
        copyReserv['dateFrom'] = str(reserv.dateFrom)
        copyReserv['dateTo'] = str(reserv.dateTo)
        copyReserv['dateReserved'] = str(reserv.dateReserved)
        copyReserv['reservationId'] = reserv.reservationId
        copyReserv['firstName'] = userInfo.firstName
        copyReserv['lastName'] = userInfo.lastName
        copyReserv['phone'] = userInfo.phone
        copyReserv['adress'] = userInfo.adress
        copyReserv['email'] = userAuth.userEmail
        copyReservations.append(copyReserv)
    return copyReservations

def bookReservation(request):
    data = getCookieInfo(request)
    data['bookId'] = request.GET.get('bookId', '')
    bookReservations = {'bookName': Book.objects.filter().get(bookId=int(data['bookId'])).bookName }
    bookReservations['copies'] = []
    for bookCopy in BookCopy.objects.filter(bookId=data['bookId'], is_active=1):
        bookCopyId = bookCopy.bookCopyId
        bookCopyCode = bookCopy.bookCopyCode
        bookCopyInfo = {'bookCopyCode':bookCopyCode}
        bookCopyInfo['bookId'] = data['bookId']
        bookCopyInfo['bookCopyId'] = bookCopyId
        bookCopyInfo['reservations'] = getReservationOfBookCopy (bookCopyId,bookCopyCode)
        bookReservations['copies'].append(bookCopyInfo)
    data['info'] = bookReservations
    #print ( json.dumps(bookReservations, indent=4, sort_keys=True) )
    t = get_template('book_reservation_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response


def delete (request):
    data = getCookieInfo(request)
    data['bookId'] = request.GET.get('bookId', '')
    data['bookCopyId'] = request.GET.get('bookCopyId', '')
    data['bookCopyCode'] = request.GET.get('bookCopyCode', '')
    data['reservationId'] = request.GET.get('reservationId', '')
    reserv = Reservation.objects.filter(
        bookCopyId=data['bookCopyId'], bookCopyCode=data['bookCopyCode'],
        is_active=1, is_reserved=1,reservationId=data['reservationId']
    ).get()
    reserv.is_reserved = 0
    reserv.save()
    if request.GET.get('redirect', '') == 'to_user':
        url ='/user/reservation/?userInfoId='+request.GET.get('userInfoId', '')+'&userAuthId=' +request.GET.get('userAuthId', '')
    else:
        url = '/reserve/bookCopy/?bookCopyCode=' + data['bookCopyCode'] + '&bookId=' + data['bookId'] + '&bookCopyId=' + data['bookCopyId']
    return redirect( url)

def status (request):
    data = getCookieInfo(request)
    data['bookId'] = request.GET.get('bookId', '')
    data['bookCopyId'] = request.GET.get('bookCopyId', '')
    data['bookCopyCode'] = request.GET.get('bookCopyCode', '')
    data['bookName'] = Book.objects.filter().get(bookId=int(data['bookId'])).bookName
    reservs = Reservation.objects.filter(
        bookCopyId=data['bookCopyId'], bookCopyCode=data['bookCopyCode'],
        is_active=1, is_reserved=1
    )
    copyReservations = []
    for reserv in reservs:
        copyReserv = {}
        userAuth  = UserAuth.objects.filter(userId=reserv.userAuthId.userId, is_active=1).get()
        userInfo =  UserInfo.objects.filter( userId=userAuth).get()
        copyReserv['dateFrom'] = str(reserv.dateFrom)
        copyReserv['dateTo'] = str(reserv.dateTo)
        copyReserv['dateReserved'] = str(reserv.dateReserved)
        copyReserv['reservationId'] = reserv.reservationId
        copyReserv['firstName'] = userInfo.firstName
        copyReserv['lastName'] =  userInfo.lastName
        copyReserv['phone'] =  userInfo.phone
        copyReserv['adress'] = userInfo.adress
        copyReserv['email'] = userAuth.userEmail
        copyReservations.append(copyReserv)
    data['reservations'] = copyReservations
    t = get_template('reservation_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response

def setReserve (request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        data['bookId'] = request.GET.get('bookId', '')
        data['bookCopyId'] = request.GET.get('bookCopyId', '')
        data['bookCopyCode'] = request.GET.get('bookCopyCode', '')
        data['bookName'] = Book.objects.filter().get(bookId=int(data['bookId'])).bookName
        t = get_template('reservation.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response
    else:
        bookCopyCode =request.POST.get('bookCopyCode', '')
        bookCopyId = request.POST.get('bookCopyId', '')
        sdateFrom = request.POST.get('fromDate', '')
        sdateTo = request.POST.get('toDate', '')
        is_reserved = getReservationStatus ( bookCopyCode, bookCopyId, sdateFrom, sdateTo)
        if is_reserved == 1:
            dateFrom = datetime.strptime(request.POST.get('fromDate', ''), '%m/%d/%Y').strftime('%Y-%m-%d')
            dateTo = datetime.strptime(request.POST.get('toDate', ''), '%m/%d/%Y').strftime('%Y-%m-%d')
            reserv = Reservation ()
            reserv.bookCopyCode = bookCopyCode
            reserv.orgCode = data['orgCode']
            reserv.dateFrom = dateFrom
            reserv.dateTo = dateTo
            reserv.dateReserved = datetime.now().strftime('%Y-%m-%d')
            reserv.is_active = 1
            reserv.is_reserved = 1
            reserv.bookCopyId = BookCopy.objects.filter(bookCopyId=bookCopyId).get()
            reserv.userAuthId = UserAuth.objects.filter(orgCode=data['orgCode'], userPin=data['userPin'],is_active=1).get()
            reserv.save()
            reserv.bookCopyId.is_reserved = 1
            reserv.bookCopyId.save()
            data['status'] = 'SUCCESS'
            data['message'] = '*****  The book is Reserved For you ******'
            return showJsonResponse(data)
        elif is_reserved == -1:
            data['status'] = 'ERROR'
            data['message'] = 'From Date cannot be earlier then Present Day'
            return showJsonResponse(data)
        elif is_reserved == -2:
            data[ 'status'] = 'ERROR'
            data['message'] = 'To Date cannot be earlier then Present Day'
            return showJsonResponse(data)
        elif is_reserved == -3:
            data['status'] = 'ERROR'
            data['message'] = 'Resevation done already'
            return showJsonResponse(data)
        else:
            data['status'] = 'ERROR'
            data['message'] = 'Resevation Not done, Something went wrong'
            return showJsonResponse(data)

def getReservationStatus ( bookCopyCode, bookCopyId, dateFrom, dateTo):
    dateFrom = datetime.strptime(dateFrom, '%m/%d/%Y')
    dateTo = datetime.strptime(dateTo, '%m/%d/%Y')
    reservs = Reservation.objects.filter(
                                            bookCopyId=bookCopyId,bookCopyCode=bookCopyCode,
                                            is_active=1,is_reserved=1
                                         )
    currentDate = datetime.now()
    if dateFrom < currentDate:
        return -1
    elif dateTo < currentDate:
        return -2
    else:
        for reserv in reservs:
            rdateFrom = datetime.strptime(str(reserv.dateFrom), '%Y-%m-%d')
            rdateTo = datetime.strptime(str(reserv.dateTo) , '%Y-%m-%d')
            if dateFrom > rdateFrom and  dateFrom < rdateTo:
                return -3
            elif dateTo > rdateFrom and dateTo < rdateTo :
                return  -3
        return 1