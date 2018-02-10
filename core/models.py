from django.db import models

sTitleHelpText = (
    'Put the %s name here -- '
    'Bot will search for this in the auction titles.<br/>'
    'Optionally, you can put additional description in parentheses ().  '
    'While searching auction titles, bot will ignore anything in parentheses.' )

sLookForHelpText = (
    'Put nick names, common misspellings and alternate %s names here -- '
    'leave blank if Bot only needs to look for the %s name.<br>'
    'Each line is evaluated separately, '
    'Bot will know item is in this %s if any one line matches.' )

sKeyWordsHelpText = (
    'Optionally, words that must be found in the title '
    '<b>IN ADDITION TO</b> %s name.<br>'
    'Put alternate key words on separate lines -- '
    'Bot will know item is for this %s if words '
    'on any one line match.' )

sExcludeIfHelpText = (
    'Bot will know item is <b>NOT</b> of this %s if '
    'any one line matches (each line evaluated separately, '
    'put different exclude tests on different lines)')

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


# from https://stackoverflow.com/questions/19498740/how-can-i-make-all-charfield-in-uppercase-direct-in-model

class UpperCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(UpperCaseCharField, self).__init__(*args, **kwargs)
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseCharField, self).pre_save(model_instance, add)

# Create your models here.



