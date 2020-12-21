
from django.shortcuts import render, redirect
from business.models import BaseUser, Business
from business.constants import BUSINESS_OWNER, business_roles


context= {
    'business_roles': business_roles
}


# Local function
def get_authenticated_context(request):
    user = BaseUser.objects.get(username=request.session['business_username'])
    context['user'] = user.details()
    return context


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
    return render(request, 'business/layouts/base.html', get_authenticated_context(request))


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


def my_businesses(request):
    if request.session.has_key('business_username'):
        # Business owner session still authenticated
        user = BaseUser.get_user_by_username(request.session['business_username'])
        context = get_authenticated_context(request)
        context['businesses'] = user.get_businesses()
        return render(request, 'business/account/businesses.html', context)

    else:
        return redirect('business:login')


def add_businesses(request):
    if request.session.has_key('business_username'):
        # admin session still authenticated
        if request.method == 'POST':
            name = request.POST.get('name')
            category = request.POST.get('category')
            location = request.POST.get('location')
            photo = request.FILES.get('photo')

            user = BaseUser.get_user_by_username(username=request.session['business_username'])

            business = Business(name=name, category=category, location=location, photo=photo)

            errors = business.validate()

            if(len(errors.keys())):
                business.save()
                business.users.add(user)
                business.save()

                business.add_role(user, BUSINESS_OWNER)
                return redirect('business:my_businesses')

            else:
                context['errors'] = errors
                return render(request, 'business/business/add.html', context)

        else:
            context = get_authenticated_context(request)
            return render(request, 'business/business/add.html', context)

    else:
        return redirect('business:login')
