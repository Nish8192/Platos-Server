from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, UserManager
from ..schedules.models import Schedule, Day

def index(request):
    return render(request, 'login_register/index.html')

def logout(request):
    del request.session['active_user_id']
    return redirect(reverse('login_register:index'))

def login(request):
    if request.method == "POST":
        chk_email = request.POST['email']
        chk_password = request.POST['password']

        if User.objects.filter(email = chk_email).exists():
            user_active = User.objects.get(email = chk_email)
            passwordMatch = User.objects.check_password_match(chk_password, user_active.password)
            if passwordMatch:
                request.session['active_user_id'] = user_active.id
                return redirect(reverse('main:index'))
            else:
                messages.error(request,'Incorrect password')
        else:
            messages.error(request,'Email does not exist. Sign up?')

    return redirect(reverse('login_register:index'))

def register(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        error_messages = User.objects.register(firstname, lastname, email, password, cpassword)

        if error_messages == []:
            diffpassword = User.objects.encrypt(password)
            User.objects.create(
                firstname = firstname,
                lastname = lastname,
                email = email,
                password = diffpassword
            )
            user_active = User.objects.get(email = email)
            request.session['active_user_id'] = user_active.id
            mon = Day.objects.create()
            tue = Day.objects.create()
            wed = Day.objects.create()
            thu = Day.objects.create()
            fri = Day.objects.create()
            sat = Day.objects.create()
            sun = Day.objects.create()
            schedule = Schedule.objects.create(user = user_active, mon = mon, tue = tue, wed = wed, thu = thu, fri = fri, sat = sat, sun = sun)


            return redirect(reverse('main:index'))
        else:
            for i in range(0, len(error_messages)):
                messages.error(request, error_messages[i])

    return redirect(reverse('login_register:index'))
