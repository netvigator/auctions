from django.contrib import admin

# Register your models here.


# from:
# https://stackoverflow.com/questions/12048176/how-can-i-rename-a-column-label-in-django-admin-for-a-field-that-is-a-method-pr

'''
https://stackoverflow.com/questions/9708455/django-admin-listview-customize-column-name

It's buried in the admin docs.
https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display

The other items like this are similiarly buried in the admin docs, but here's a summary:

short_description: the column title to use (string)
allow_tags: what the name says... let's you use HTML (True or False)
admin_order_field: a field on the model to order this column by (string, field name)
boolean: indicates the return value is boolean and signals the admin to use the nice graphic green check/red X (True or False)
'''

def admin_method_attributes(**outer_kwargs):
    """ Wrap an admin method with passed arguments as attributes and values.
    DRY way of extremely common admin manipulation such as setting short_description, allow_tags, etc.
    """
    def method_decorator(func):
        for kw, arg in outer_kwargs.items():
            setattr(func, kw, arg)
        return func
    return method_decorator
