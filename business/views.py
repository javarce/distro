
from django.shortcuts import render, redirect
from business.models import BaseUser
from business.constants import BUSINESS_OWNER, business_roles


context= {
    'business_roles': business_roles
}


def index(request):
    if request.session.has_key('business_username'):
        return redirect('business:dashboard')

    else:
        return redirect('business:login')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        base_user = BaseUser.objects.filter(username=username, password=password)
        if base_user:
            request.session['business_username'] = username
            return redirect('business:dashboard')

        else:
            return render(request, 'business/account/login.html', {'error': 'Username or password is incorrect'})

    else:
        return render(request, 'business/account/login.html')


def dashboard(request):
    return render(request, 'business/layouts/base.html', context)


def register(request):
    if request.method == 'POST':
        # Save business account
        post = request.POST
        first_name = post.get('first_name')
        last_name = post.get('last_name')
        username = post.get('username')
        email = post.get('email')
        phone = post.get('phone')
        password = post.get('password')
        re_password = post.get('re_password')

        if password != re_password:
            errors = {}
            errors['error_password'] = 'Passwords do not match'
            return render(request, 'business/account/register.html', {errors: errors})

        elif BaseUser.usernameExists(username):
            return render(request, 'business/account/register.html', {errors: {'error_username': 'Username already in user'}})

        else:
            base_user = BaseUser(
                role=BUSINESS_OWNER,
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone=phone,
                password=password
            )
            errors = base_user.validate()
            if len(errors.keys()):
                return render(request, 'business/account/register.html', {errors: errors})

            else:
                base_user.save()
                request.session['business_username'] = username
                return redirect('business:dashboard')

    else:
        # Return registration page
        return render(request, 'business/account/register.html')
