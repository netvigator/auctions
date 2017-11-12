from django.db import models

class IntegerRangeField(models.PositiveSmallIntegerField):
    def __init__(self,
            verbose_name=None, name=None, min_value=None, max_value=None,
            **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.PositiveSmallIntegerField.__init__(
            self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

# Create your models here.



