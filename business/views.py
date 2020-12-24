
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
        context = get_authenticated_context(request)
        context['text_title'] = 'Add Business'
        context['text_button'] = 'Submit'
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
            return render(request, 'business/business/add.html', context)

    else:
        return redirect('business:login')



def edit_businesses(request, business_id):
    if request.session.has_key('business_username'):
        # admin session still authenticated
        context = get_authenticated_context(request)
        business = Business.get_by_id(business_id)
        context['name'] = business.name
        context['category'] = business.category
        context['location'] = business.location
        context['photo'] = business.photo
        context['action'] = f'/business/{business_id}/edit'
        context['text_title'] = 'Edit Business'
        context['text_button'] = 'Update'

        if request.method == 'POST':
            name = request.POST.get('name')
            category = request.POST.get('category')
            location = request.POST.get('location')
            photo = request.FILES.get('photo')

            user = BaseUser.get_user_by_username(username=request.session['business_username'])
            business.name = name
            business.category = category
            business.location = location
            if photo:
                business.photo = photo

            errors = business.validate()
            if(len(errors.keys())):
                context['errors'] = errors
                return render(request, 'business/business/add.html', context)

            else:
                business.save()
                business.add_role(user, BUSINESS_OWNER)
                business.save()
                return redirect('business:my_businesses')

        else:
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
        context = get_business_context(request)
        context['text_title'] = 'Add Category'
        context['text_button'] = 'Submit'

        if request.method == 'POST':
            name = request.POST.get('name')
            photo = request.FILES.get('photo')

            category = Category(name=name, photo=photo, business=context.get('business'))
            
            errors = category.validate()
            if len(errors.keys()):
                context['errors'] = errors
                return render(request, 'business/catalog/category/add.html', context)

            else:
                # Everything is okay, persist category to db
                category.save()
                return redirect('business:categories')

        else:
            return render(request, 'business/catalog/category/add.html', context)

    else:
        return redirect('business:login')


def edit_category(request, id):
    if request.session.has_key('business_username'):
        context = get_business_context(request)
        context['text_title'] = 'Edit Category'
        context['text_button'] = 'Update'
        category = Category.objects.filter(id=id).first()

        if request.method == 'POST':
            name = request.POST.get('name')
            photo = request.FILES.get('photo')

            category.name = name
            if photo:
                category.photo = photo 
            
            errors = category.validate()
            if len(errors.keys()):
                context['errors'] = errors
                context['name'] = name
                return render(request, 'business/catalog/category/add.html', context)

            else:
                # Everything is okay, persist category to db
                category.save()
                return redirect('business:categories')

        else:
            context['name'] = category.name
            context['photo'] = category.photo
            context['action'] = f'/business/catalog/category/{id}/edit'
            return render(request, 'business/catalog/category/add.html', context)

    else:
        return redirect('business:login')




def delete_category(request, id):
    category = Category.get_by_id(id)
    category.delete()
    return redirect(f'/business/catalog/categories')




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
        context = get_business_context(request)
        context['text_title'] = 'Add Product'
        context['text_button'] = 'Submit'
        context['action'] = '/business/catalog/product/add'

        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_id = request.POST.get('category_id')
            photo = request.FILES.get('photo')

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
            business = context.get('business')
            categories = business.business_categories.all()
            context['categories'] = categories
            return render(request, 'business/catalog/product/add.html', context)

    else:
        return redirect('business:login')



def edit_product(request, product_id):
    if request.session.has_key('business_username'):
        context = get_business_context(request)
        context['text_title'] = 'Edit Product'
        context['text_button'] = 'Update'
        context['action'] = f'/business/catalog/product/{product_id}/edit'

        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_id = request.POST.get('category_id')
            photo = request.FILES.get('photo')

            product = Product.get_by_id(product_id)
            product.name = name
            product.price = price
            product.stock = stock
            if photo:
                product.photo = photo
            
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
            business = context.get('business')
            categories = business.business_categories.all()
            context['categories'] = categories

            product = Product.get_by_id(product_id)
            context['name'] = product.name
            context['price'] = product.price
            context['stock'] = product.stock
            context['category_id'] = product.category.id
            context['photo'] = product.photo
            return render(request, 'business/catalog/product/add.html', context)

    else:
        return redirect('business:login')


def delete_product(request, product_id):
    product = Product.get_by_id(product_id)
    product.delete()
    return redirect(f'/business/catalog/products')


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
        context['modifiable'] = not (role_id == BUSINESS_OWNER)
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
        context['text_title'] = f'Add {role_title}'
        context['action'] = f'/business/users/role/{role_id}/add'
        context['btn_text'] = 'Submit'

        if request.method == 'POST':
            post = request.POST
            first_name = post.get('first_name')
            last_name = post.get('last_name')
            username = post.get('username')
            email = post.get('email')
            phone = post.get('phone')
            password = post.get('password')

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
                context['errors'] = errors
                context['first_name'] = first_name
                context['last_name'] = last_name
                context['username'] = username
                context['email'] = email
                context['phone'] = phone
                return render(request, 'business/user/add.html', context)

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


def edit_user(request, user_id, role_id):
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
        context['text_title'] = f"Edit {context['role_title']}"
        context['action'] = f'/business/users/{user_id}/role/{role_id}/edit'
        context['btn_text'] = 'Update'

        if request.method == 'POST':
            post = request.POST
            first_name = post.get('user_id')
            first_name = post.get('first_name')
            last_name = post.get('last_name')
            username = post.get('username')
            email = post.get('email')
            phone = post.get('phone')
            password = post.get('password')

            base_user = BaseUser.get_by_id(user_id)
            base_user.update(first_name, last_name, username, email, phone, password)
            errors = base_user.validate()
            if len(errors.keys()):
                context['errors'] = errors
                context['first_name'] = first_name
                context['last_name'] = last_name
                context['username'] = username
                context['email'] = email
                context['phone'] = phone
                return render(request, 'business/user/add.html', context)

            else:
                base_user.save()
                return redirect(f'/business/users/{role_id}/role')

        else:
            base_user = BaseUser.get_by_id(user_id)
            context['first_name'] = base_user.first_name
            context['last_name'] = base_user.last_name
            context['username'] = base_user.username
            context['email'] = base_user.email
            context['phone'] = base_user.phone
            context['password'] = ''
            return render(request, 'business/user/add.html', context)

    else:
        return redirect('business:login')


def delete_user(request, user_id, role_id):
    user = BaseUser.get_by_id(user_id)
    user.delete()
    return redirect(f'/business/users/{role_id}/role')
