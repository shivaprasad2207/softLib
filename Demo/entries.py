from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from .mylib.mylib import get_or_create_csrf_token as getCsrf
from .mylib.mylib import addOrgEntry,addUserAuth,addUserInfo
from .models import RegisterOrganisation, UserAuth, UserInfo
from .mylib.myutil import getCookieInfo, showJsonResponse
import json
import hashlib

def manageBooks(request):
    t = get_template('manage_books.html')
    html = t.render(getCookieInfo(request))
    response = HttpResponse(html)
    return response

def login(request):
    if request.method == 'POST':
        orgCode = request.POST.get('orgCode', '')
        userPin = request.POST.get('userPin', '')
        password = request.POST.get('password', '')
        data = {}
        if RegisterOrganisation.objects.filter(orgCode=orgCode).count() <= 0 :
            data['status'] = 'ERROR'
            data['message'] = 'No such ' + orgCode + '  Library code exist'
            return showJsonResponse(data)
        elif UserAuth.objects.filter(userPin=userPin).count() <= 0 :
            data['status'] = 'ERROR'
            data['message'] = userPin + '  No such user pin exist'
            return showJsonResponse(data)
        else:
            userPassword = UserAuth.objects.filter(userPin=userPin).get().userPassword
            userOrgCode = UserAuth.objects.filter(userPin=userPin).get().orgCode
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
            if userOrgCode != orgCode :
                data['status'] = 'ERROR'
                data['message'] = 'No such registered user in this Library'
                return showJsonResponse(data)
            elif userPassword != password :
                data['status'] = 'ERROR'
                data['message'] = '  .. wrong password'
                return showJsonResponse(data)
            else:
                user = UserAuth.objects.filter(userPin=userPin).get()
                userId = user.userId
                data['status'] = 'SUCCESS'
                data['firstName'] = UserInfo.objects.filter(userId=userId).get().firstName
                data['lastName'] = UserInfo.objects.filter(userId=userId).get().lastName
                data['userPin'] = userPin
                data['userEmail'] = user.userEmail
                data['userRole'] = user.userRole
                data['orgCode'] = orgCode
                data['orgName'] = RegisterOrganisation.objects.filter(orgCode=orgCode).get().orgName
                data['csrfmiddlewaretoken'] = getCsrf(request)
                userInfo = ';'.join(['%s=%s' % x for x in data.items()])
                response = HttpResponse()
                response['Content-Type'] = "text/javascript"
                response.set_cookie('userInfo', userInfo)
                response.write(json.dumps(data))
                return response
    else:
        csrf = {
            'csrfmiddlewaretoken': getCsrf(request)
        }
        t = get_template('login.html')
        html = t.render(csrf)
        return HttpResponse(html)


def main (request ):
    if request.method == 'POST':
        t = get_template('main.html')
        print(json.dumps(getCookieInfo(request), indent=4, sort_keys=True))
        html = t.render(getCookieInfo(request))
        response = HttpResponse(html)
        return response
    else:
        t = get_template('main.html')
        print(json.dumps(getCookieInfo(request), indent=4, sort_keys=True))
        html = t.render(getCookieInfo(request))
        response = HttpResponse(html)
        return response

def orgRegistry(request):
    if request.method == 'POST':
        data = {}
        orgCode = get_random_string(length=8)
        userPin = get_random_string(length=8)
        if RegisterOrganisation.objects.filter(orgName=request.POST.get('orgName', '')).count() > 0 :
            data['status'] = 'ERROR'
            data['message'] = 'Same Organisation Name Already Exist'
        elif RegisterOrganisation.objects.filter(orgCode=orgCode).count() > 0 :
            data['status'] = 'ERROR'
            data['message'] = 'Orgnisation Code already Exist..Please report the Error'
        elif UserAuth.objects.filter(userPin=userPin).count() > 0 :
            data['status'] = 'ERROR'
            data['message'] = 'Same Admin loginId already Exist..Please report the Error'
        else:
            addOrgEntry(request, orgCode)
            authParam = {}
            authParam['userEmail'] = request.POST.get('orgEmail', '')
            authParam['userPassword'] = request.POST.get('password', '')
            authParam['orgCode'] = orgCode
            authParam['userPin'] = userPin
            authParam['userRole'] = 0
            user = addUserAuth(authParam)
            param = {}
            param['userId'] = user
            param['firstName'] = 'Admin'
            param['lastName'] = 'Admin'
            param['phone'] = request.POST.get('orgPhone', '')
            param['adress'] = request.POST.get('orgAdress', '')
            addUserInfo(param)
            data['status'] = 'SUCCESS'
            data['message'] = 'Your Organisation Code is <u>' + orgCode + '</u>.<br> ' + \
                              'Admin Login Id is  <u>' + user.userPin + '</u>.<br> ' + \
                              'Same details Sent to your Email, Click link to Confirm.'
        return showJsonResponse(data)
    else:
        csrf = {
            'csrfmiddlewaretoken': getCsrf(request)
        }
        t = get_template('org_reg.html')
        html = t.render(csrf)
        return HttpResponse(html)

def userAdd(request):
    if request.method == 'POST':
        data = {}
        userPin = get_random_string(length=8)
        if UserAuth.objects.filter(userPin=userPin).count() > 0 :
            data['status'] = 'ERROR'
            data['message'] = 'Same Admin loginId already Exist..Please report the Error'
        else:
            authParam = {}
            authParam['userEmail'] = request.POST.get('userEmail', '')
            authParam['userPassword'] = request.POST.get('password', '')
            orgCode = authParam['orgCode'] = request.POST.get('orgCode', '')
            authParam['userPin'] = userPin
            authParam['userRole'] = 1
            user = addUserAuth(authParam)
            param = {}
            param['userId'] = user
            param['firstName'] = request.POST.get('firstName', '')
            param['lastName'] = request.POST.get('lastName', '')
            param['phone'] = request.POST.get('userPhone', '')
            param['adress'] = request.POST.get('userAdress', '')
            addUserInfo(param)
            data['status'] = 'SUCCESS'
            data['message'] = \
                                'Your Login Id is  <u>' + user.userPin + '</u> is created.<br> ' + \
                                'You can use login to Library Code is <u>' + orgCode + '</u>.<br> ' + \
                                'Same details Sent to your Email, Click link to Confirm.'
        return showJsonResponse(data)
    else:
        csrf = {
            'csrfmiddlewaretoken': getCsrf(request)
        }
        t = get_template('user_add.html')
        html = t.render(csrf)
        return HttpResponse(html)


def logout (request):
    csrf = {
        'csrfmiddlewaretoken': getCsrf(request)
    }
    t = get_template('login.html')
    html = t.render(csrf)
    response = HttpResponse(html)
    response.delete_cookie('userInfo')
    return response
