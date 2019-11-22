
def setShippingTypeLocalPickupOptional( dNewResult ):
    #
    '''
    if shippingType is 5 FreePickup, it means
    9 Free Local Pick Up is optional if handlingTime is set, but`
    Pick Up ONLY! if handlingTime is not set
    this needs to be set after reading the api data and before the form
    tested in searching/tests/test_models.py
    '''
    #
    iShippingType = dNewResult.get( 'iShippingType' )
    iHandlingTime = dNewResult.get( 'iHandlingTime' )
    #
    if iShippingType == 5 and iHandlingTime and iHandlingTime > 0:
        #
        dNewResult[ 'iShippingType' ] = 9
        #
    #


