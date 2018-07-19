from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from .models import UserAuth, UserInfo
from .mylib.myutil import getCookieInfo, showJsonResponse
from .mylib.mylib import addUserAuth,addUserInfo

def manageUsers(request):
    t = get_template('manage_users.html')
    html = t.render(getCookieInfo(request))
    response = HttpResponse(html)
    return response

def userAdd (request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        t = get_template('lib_user_add.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response
    else:
        userPin = get_random_string(length=8)
        authParam = {}
        authParam['userEmail'] = request.POST.get('userEmail', '')
        authParam['userPassword'] = userPin
        authParam['orgCode'] = data['orgCode']
        authParam['userPin'] = userPin
        authParam['userRole'] = 1
        user = addUserAuth(authParam)
        authParam['userId'] = user
        authParam['firstName'] = request.POST.get('firstName', '')
        authParam['lastName'] = request.POST.get('lastName', '')
        authParam['phone'] = request.POST.get('userPhone', '')
        authParam['adress'] = request.POST.get('userAdress', '')
        addUserInfo(authParam)
        data['status'] = 'SUCCESS'
        data['message'] = \
                                'Login Id is  <u>' + user.userPin + '</u> is created.<br> ' + \
                                'with password '  + user.userPin  + ' You can change once login <u>'

        return showJsonResponse(data)

def userList (request):
    data = getCookieInfo(request)
    userInfoList = []
    for authInfo in  UserAuth.objects.filter(orgCode=data['orgCode'], is_active=1):
        userInfo = UserInfo.objects.filter(userId=authInfo.userId).get()
        userInfoList.append({
            'firstName':userInfo.firstName,
            'lastName':userInfo.lastName,
            'phone':userInfo.phone,
            'address': userInfo.adress,
            'userInfoId':userInfo.userId.userId,
            'email':authInfo.userEmail,
            'userRole':authInfo.userRole,
            'userAuthId':userInfo.id
        })
    data['users'] = userInfoList
    t = get_template('user_list.html')
    html = t.render(data)
    response = HttpResponse(html)
    return response

def chuser (request):
    data = getCookieInfo(request)
    userInfoId = request.GET.get('userInfoId', '')
    userAuth = UserAuth.objects.filter(orgCode=data['orgCode'], is_active=1, userId=userInfoId).get()
    if userAuth.userRole == 1 :
        userAuth.userRole = 0
    else:
        userAuth.userRole = 1
    userAuth.save()
    return redirect('/user/list')

def delete (request):
    data = getCookieInfo(request)
    userInfoId = request.GET.get('userInfoId', '')
    userAuth = UserAuth.objects.filter(orgCode=data['orgCode'], is_active=1, userId=userInfoId).get()
    userAuth.is_active = 0
    userAuth.save()
    return redirect('/user/list')

def modify (request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        userInfoId = request.GET.get('userInfoId', '')
        userAuth = UserAuth.objects.filter(orgCode=data['orgCode'], is_active=1, userId=userInfoId).get()
        userInfo = UserInfo.objects.filter(userId=userAuth.userId).get()
        user = {
            'firstName':userInfo.firstName,
            'lastName':userInfo.lastName,
            'phone':userInfo.phone,
            'address': userInfo.adress,
            'userInfoId':userInfo.id,
            'userAuthId': userInfo.userId.userId,
            'email':userAuth.userEmail,
            'userRole':userAuth.userRole
        }
        userData = data.copy()
        userData.update(user)
        t = get_template('lib_user_mod.html')
        html = t.render(userData)
        response = HttpResponse(html)
        return response
    else:
        userAuthId = request.POST.get('userAuthId', '')
        userAuth = UserAuth.objects.filter(orgCode=data['orgCode'], is_active=1, userId=userAuthId).get()
        userInfo = UserInfo.objects.filter(userId=userAuth.userId).get()
        userInfo.adress = request.POST.get('address', '')
        userInfo.phone = request.POST.get('phone', '')
        userInfo.firstName =  request.POST.get('firstName', '')
        userInfo.lastName =  request.POST.get('lastName', '')
        userAuth.userEmail = request.POST.get('userEmail', '')
        userAuth.save()
        userInfo.save()
        return redirect('/user/list')

def search(request):
    data = getCookieInfo(request)
    if request.method == 'GET':
        data['section'] = "SHOW_USER_SEARCH"
        t = get_template('user_list.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response
    else:
        searchField = request.POST.get('searchField', '')
        searchString = request.POST.get('searchString', '')
        if searchField == 'userEmail':
            userInfoList = []
            search = {}
            search[searchField + '__contains'] = searchString
            search['orgCode'] = data['orgCode']
            search['is_active'] = 1
            for authInfo in UserAuth.objects.filter(**search):
                userInfo = UserInfo.objects.filter(userId=authInfo.userId).get()
                if userInfo:
                    userInfoList.append({
                        'firstName': userInfo.firstName,
                        'lastName': userInfo.lastName,
                        'phone': userInfo.phone,
                        'address': userInfo.adress,
                        'userInfoId': userInfo.userId.userId,
                        'email': authInfo.userEmail,
                        'userRole': authInfo.userRole,
                        'userAuthId': userInfo.id
                    })
            data['users'] = userInfoList
            data['section'] = "SHOW_USER_SEARCH"
        elif searchField == 'userRole':
            userInfoList = []
            search = {}
            if searchString in 'admin' or searchString in 'ADMIN':
                search['userRole'] = 0
            elif searchString in 'user' or searchString in 'USER':
                search['userRole'] = 1
            else:
                return redirect('/user/search')
            search['orgCode'] = data['orgCode']
            search['is_active'] = 1
            for authInfo in UserAuth.objects.filter(**search):
                userInfo = UserInfo.objects.filter(userId=authInfo.userId).get()
                if userInfo:
                    userInfoList.append({
                        'firstName': userInfo.firstName,
                        'lastName': userInfo.lastName,
                        'phone': userInfo.phone,
                        'address': userInfo.adress,
                        'userInfoId': userInfo.userId.userId,
                        'email': authInfo.userEmail,
                        'userRole': authInfo.userRole,
                        'userAuthId': userInfo.id
                    })
            data['users'] = userInfoList
            data['section'] = "SHOW_USER_SEARCH"
        else:
            userInfoList = []
            search = {}
            search[searchField + '__contains'] = searchString
            for authInfo in UserAuth.objects.filter(orgCode=data['orgCode'], is_active=1):
                search['userId'] = authInfo.userId
                userInfo = getUserInfoObj (search)
                if userInfo  :
                    userInfoList.append({
                        'firstName': userInfo.firstName,
                        'lastName': userInfo.lastName,
                        'phone': userInfo.phone,
                        'address': userInfo.adress,
                        'userInfoId': userInfo.userId.userId,
                        'email': authInfo.userEmail,
                        'userRole': authInfo.userRole,
                        'userAuthId': userInfo.id
                    })
            data['users'] = userInfoList
            data['section'] = "SHOW_USER_SEARCH"
        t = get_template('user_list.html')
        html = t.render(data)
        response = HttpResponse(html)
        return response

def getUserInfoObj(search):
    try:
        return UserInfo.objects.filter(**search).get()
    except UserInfo.DoesNotExist:
        return None
