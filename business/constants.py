
ADMIN = 1
PUBLIC_USER = 2
BUSINESS_OWNER = 3
STORE_MANAGER = 4
DISPATCH_MANAGER = 5


ROLES = (
    (ADMIN, 'Administrator'),
    (PUBLIC_USER, 'Public User'),
    (BUSINESS_OWNER, 'Business Owner'),
    (STORE_MANAGER, 'Store Manager'),
    (DISPATCH_MANAGER, 'Dispatch Manager'),
)


business_roles = [
    {
        'id': BUSINESS_OWNER,
        'title': 'Business Owner'
    },
    {
        'id': STORE_MANAGER,
        'title': 'Store Manager'
    },
    {
        'id': DISPATCH_MANAGER,
        'title': 'Dispatch Manager'
    },
]
