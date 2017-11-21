# misc utils can go here

from django.contrib.auth import get_user_model


User = get_user_model()

oUserOne = User.objects.filter( id = 1 ).first()

if not oUserOne:
    #
    oUser = User()
    #
    oUser.first_name    = 'Rick'
    oUser.last_name     = 'Graves'
    oUser.email         = 'gravesricharde@yahoo.com'
    oUser.username      = 'aardvigator'
    oUser.password      = 'tba'
    #
    oUser.save()
    #
    oUserOne = oUser

