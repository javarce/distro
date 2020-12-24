
from django.db import models
from business.constants import ROLES


class BaseUser(models.Model):
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=False, null=False)
    first_name = models.CharField(max_length=40, blank=False, null=False)
    last_name = models.CharField(max_length=40, blank=False, null=False)
    username = models.CharField(max_length=20, blank=False, null=False)
    email = models.CharField(max_length=40, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=15, blank=False, null=False, unique=True)
    password = models.CharField(max_length=225, blank=False, null=False)

    def __str__(self):
        return self.username


    def validate(self):
        errors = {}

        if len(self.first_name) > 40:
            errors['error_first_name'] = 'First name cannot be more than 40 characters'

        if not self.first_name:
            errors['error_first_name'] = 'First name cannot be blank'

        if len(self.last_name) > 40:
            errors['error_last_name'] = 'Last name cannot be more than 40 characters'

        if not self.last_name:
            errors['error_last_name'] = 'Last name cannot be blank'

        if len(self.username) > 20:
            errors['error_username'] = 'Username cannot be more than 40 characters'

        if not self.username:
            errors['error_username'] = 'Username cannot be blank'

        if self.usernameExists():
            errors['error_username'] = 'User with this username already exists'

        if len(self.email) > 40:
            errors['error_email'] = 'Email cannot be more than 40 characters'

        if not self.email:
            errors['error_email'] = 'Email cannot be blank'

        if self.emailExists():
            errors['error_email'] = 'Email already in user by another user'

        if len(self.phone) > 40:
            errors['error_phone'] = 'Phone cannot be more than 40 characters'

        if not self.phone:
            errors['error_phone'] = 'Phone cannot be blank'

        if self.phoneExists():
            errors['error_phone'] = 'Phone already in user by another user'

        if len(self.password) > 225:
            errors['error_password'] = 'Password cannot be more than 40 characters'

        if not self.password:
            errors['error_password'] = 'Password cannot be blank'

        return errors

    @staticmethod
    def get_by_id(id):
        return BaseUser.objects.filter(id=id).first()

    
    def usernameExists(self):
        user = BaseUser.objects.filter(username=self.username).first()
        return user.id != self.id if user else False


    def phoneExists(self):
        user = BaseUser.objects.filter(phone=self.phone).first()
        return user.id != self.id if user else False


    def emailExists(self):
        user = BaseUser.objects.filter(email=self.email).first()
        return user.id != self.id if user else False


    def details(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'phone': self.phone
        }


    def get_businesses(self):
        businesses = self.business_set.all()
        return [b.details(self) for b in businesses]


    @staticmethod
    def get_user_by_username(username: str) -> 'BaseUser':
        return BaseUser.objects.get(username=username)

    def update(self, first_name, last_name, username, email, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password





class Business(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=False, null=False, default='None')
    location = models.CharField(max_length=100, blank=False, null=False)
    photo = models.ImageField(upload_to='uploads', blank=False, null=False, default='avatar.png')
    users = models.ManyToManyField(BaseUser)


    def validate(self) -> dict:
        errors = {}

        if len(self.name) > 100:
            errors['error_name'] = 'Name cannot be more than 100 characters'

        if not self.name:
            errors['error_name'] = 'Name cannot be blank'

        if len(self.category) > 100:
            errors['error_category'] = 'Category cannot be more than 100 characters'

        if not self.category:
            errors['error_category'] = 'Category cannot be blank'

        if len(self.location) > 100:
            errors['error_location'] = 'Location cannot be more than 100 characters'

        if not self.location:
            errors['error_location'] = 'Location cannot be blank'

        if not self.photo:
            errors['error_photo'] = 'Photo cannot be blank'

        return errors


    def details(self, user):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'photo': self.photo,
            'role': self.business_role(user)
        }


    @staticmethod
    def get_by_id(id: int) -> 'Business':
        return Business.objects.filter(id=id).first()


    def business_role(self, user) -> str:
        ''' Get role of the user on this business. '''
        b_role = BusinessRole.objects.filter(user=user, business=self).first()
        if b_role:
            return b_role.get_role_display()

    
    def get_users(self, role):
        return [u for u in self.users.all() if BusinessRole.objects.filter(user=u, business=self, role=role).first()]


    def add_role(self, user: 'BaseUser', role: int) -> None:
        '''
            Add user to this business, and their respective role.
            This method must be called when both the user and business have been saved
        '''
        self.users.add(user)
        self.save()
        business_role = BusinessRole(role=role, user=user, business=self)
        business_role.save()





class BusinessRole(models.Model):
    ''' Table to hold roles of accounts on businesses. '''
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=False, null=False)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=225)
    photo = models.ImageField(upload_to='uploads', blank=False, null=False, default='avatar.png')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_categories')


    def validate(self) -> dict:
        errors = {}

        if len(self.name) > 225:
            errors['error_name'] = 'Name cannot be more than 100 characters'

        if not self.name:
            errors['error_name'] = 'Name cannot be blank'

        if not self.photo:
            errors['error_photo'] = 'Photo cannot be blank'

        return errors


    @staticmethod
    def get_by_id(id):
        try:
            return Category.objects.get(id=id)

        except:
            return None


class Product(models.Model):
    name = models.CharField(max_length=225)
    price = models.BigIntegerField(null=False, blank=False)
    stock = models.BigIntegerField(null=False, blank=False)
    photo = models.ImageField(upload_to='uploads', blank=False, null=False, default='avatar.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_categories')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_products')

    def validate(self, category_id) -> dict:
        errors = {}
        # Validate category
        if not category_id:
            errors['error_category'] = 'Category cannot be blank'

        if not Category.objects.filter(id=category_id).first():
            errors['error_category'] = 'Category no longer exists, please choose another'

        if len(self.name) > 225:
            errors['error_name'] = 'Name cannot be more than 225 characters'

        if not self.name:
            errors['error_name'] = 'Name cannot be blank'

        if not self.price:
            errors['error_price'] = 'Price must be greater than 0'

        if not self.stock:
            errors['error_stock'] = 'Stock must be greater than 0'

        if not self.photo:
            errors['error_photo'] = 'Photo cannot be blank'

        return errors

    @staticmethod
    def get_by_id(id):
        try:
            return Product.objects.get(id=id)

        except:
            return None

    
    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'text_price': f"UGX {self.price}/=",
            'stock': self.stock,
            'photo': self.photo,
            'is_stock_available': self.stock > 0,
            'stock_status': 'In-Stock' if self.stock > 0 else 'Not-In-Stock'
        }
