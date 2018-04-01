from django.contrib.auth        import get_user_model

oUserModel = get_user_model()

oUserOne = oUserModel.objects.filter( id = 1 ).first()
# oUserOne = None # oUserModel.objects.filter( id = 1 ).first()

# can get 'field does not exist; error when trying to add a field via migrate
# workaround: use the commented lines above and below

#if False: # not oUserOne:
if not oUserOne:
    #
    oUserOne = oUserModel(
        username        = 'netvigator',
        email           = 'gravesricharde@yahoo.com',
        password        = None,
        first_name      = 'Rick',
        last_name       = 'Graves', )
    #
    if oUserOne.id != 1:
        oUserOne.id = 1
    #
    oUserOne.save()
