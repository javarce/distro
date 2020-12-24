
from django.shortcuts import render, redirect, reverse
from business.models import BaseUser, Business, Category, Product
from business.constants import BUSINESS_OWNER, business_roles


'''
    @key => curr_business_id => session key to key current active business
'''


# Local function
def get_authenticated_context(request):
    context= {
        'business_roles': business_roles
    }
    user = BaseUser.objects.get(username=request.session['business_username'])
    context['user'] = user.details()
    context['curr_business_id'] = request.session.get('curr_business_id')
    return context

# Business Context
def get_business_context(request):
    context = get_authenticated_context(request)
    context['business'] = Business.objects.get(id=context['curr_business_id'])
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


def logout(request):
    request.session.pop('business_username', 1)
    return redirect('business:login')


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

        # Get current viewed business_id from session
        context['curr_business_id'] = request.session.get('curr_business_id')
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


def activate_business_session(request, id):
    if request.session.has_key('business_username'):
        request.session['curr_business_id'] = id
        return redirect('business:my_businesses')

    else:
        return redirect('business:login')



def categories(request):
    if request.session.has_key('business_username'):
        context = get_business_context(request)
        business = context.get('business')
        context['categories'] = business.business_categories.all()
        return render(request, 'business/catalog/category/list.html', context)
    
    else:
        return redirect('business:login')


def add_category(request):
    if request.session.has_key('business_username'):
        if request.method == 'POST':
            name = request.POST.get('name')
            photo = request.FILES.get('photo')

            cont = get_business_context(request)
            category = Category(name=name, photo=photo, business=cont.get('business'))
            
            errors = category.validate()
            if len(errors.keys()):
                cont['errors'] = errors
                return render(request, 'business/catalog/category/add.html', cont)

            else:
                # Everything is okay, persist category to db
                category.save()
                return redirect('business:categories')

        else:
            return render(request, 'business/catalog/category/add.html', {'business_roles': business_roles})

    else:
        return redirect('business:login')


def products(request):
    if request.session.has_key('business_username'):
        context = get_business_context(request)
        business = context.get('business')
        context['products'] = business.business_products.all()
        return render(request, 'business/catalog/product/list.html', context)

    else:
        return redirect('business:login')


def add_product(request):
    if request.session.has_key('business_username'):
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_id = request.POST.get('category_id')
            photo = request.FILES.get('photo')

            context = get_business_context(request)

            product = Product(name=name, price=price, stock=stock, photo=photo)
            
            errors = product.validate(category_id)
            if len(errors.keys()):
                context['errors'] = errors
                return render(request, 'business/catalog/product/add.html', context)

            else:
                # Everything is okay, persist category to db
                business=context.get('business')
                category = Category.objects.get(id=category_id)
                product.business = business
                product.category = category
                product.save()
                return redirect('business:products')

        else:
            context = get_business_context(request)
            business = context.get('business')
            categories = business.business_categories.all()
            context['categories'] = categories
            return render(request, 'business/catalog/product/add.html', context)

    else:
        return redirect('business:login')



def users(request, role_id):
    if request.session.has_key('business_username'):
        context = get_business_context(request)
        business = context.get('business')
        users = business.get_users(role_id)
        context['users'] = users

        # Current role
        role_title = None
        for r in business_roles:
            if r['id'] == int(role_id):
                role_title = r['title']
                break
        context['role_title'] = role_title
        context['role_id'] = int(role_id)
        return render(request, 'business/user/list.html', context)


    else:
        return redirect('business:login')


def add_user(request, role_id):
    if request.session.has_key('business_username'):
        context = get_business_context(request)
        business = context.get('business')
            # Current role
        role_title = None
        for r in business_roles:
            if r['id'] == int(role_id):
                role_title = r['title']
                break
        context['role_title'] = role_title
        context['role_id'] = int(role_id)

        if request.method == 'POST':
            post = request.POST
            first_name = post.get('first_name')
            last_name = post.get('last_name')
            username = post.get('username')
            email = post.get('email')
            phone = post.get('phone')
            password = post.get('password')

            if BaseUser.usernameExists(username):
                context['errors'] = {'error_username': 'Username already exists'}
                context['first_name'] = first_name
                context['last_name'] = last_name
                context['username'] = username
                context['email'] = email
                context['phone'] = phone
                return render(request, 'business/user/add.html', context)

            elif BaseUser.phoneExists(phone):
                context['errors'] = {'error_phone': 'User with this phone already exists'}
                context['first_name'] = first_name
                context['last_name'] = last_name
                context['username'] = username
                context['email'] = email
                context['phone'] = phone
                return render(request, 'business/user/add.html', context)

            elif BaseUser.emailExists(email):
                context['errors'] = {'error_email': 'User with this email already exists'}
                context['first_name'] = first_name
                context['last_name'] = last_name
                context['username'] = username
                context['email'] = email
                context['phone'] = phone
                return render(request, 'business/user/add.html', context)

            else:
                base_user = BaseUser(
                    role=role_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    phone=phone,
                    password=password
                )
                errors = base_user.validate()
                if len(errors.keys()):
                    return render(request, 'business/user/add.html', {errors: errors})

                else:
                    base_user.save()
                    business_id = request.session.get('curr_business_id')
                    business = Business.get_by_id(business_id)
                    business.add_role(base_user, role_id)
                    return redirect(f'/business/users/{role_id}/role')


        else:
            return render(request, 'business/user/add.html', context)

    else:
        return redirect('business:login')