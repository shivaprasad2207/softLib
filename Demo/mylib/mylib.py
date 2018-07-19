from django.middleware import csrf
from ..models import RegisterOrganisation, UserAuth, UserInfo
import hashlib

def get_or_create_csrf_token(request):
    token = request.META.get('CSRF_COOKIE', None)
    if token is None:
        token = csrf._get_new_csrf_key()
        request.META['CSRF_COOKIE'] = token
    request.META['CSRF_COOKIE_USED'] = True
    return token

def addOrgEntry (request,orgCode):
    org = RegisterOrganisation()
    org.orgName = request.POST.get('orgName', '')
    org.orgAdress = request.POST.get('orgAdress', '')
    org.orgPhone = request.POST.get('orgPhone', '')
    org.orgEmail = request.POST.get('orgEmail', '')
    org.orgCode = orgCode
    org.save()

def addUserAuth(data):
    user = UserAuth()
    user.userEmail = data['userEmail']
    user.orgCode = data['orgCode']
    user.userPassword =  hashlib.md5(data['userPassword'].encode('utf-8')).hexdigest()
    user.userPin = data['userPin']
    user.userRole = data['userRole']
    user.save()
    return user

def addUserInfo (data):
    user = UserInfo()
    user.userId = data['userId']
    user.firstName = data['firstName']
    user.lastName = data['lastName']
    user.adress = data['adress']
    user.phone = data['phone']
    user.save()
