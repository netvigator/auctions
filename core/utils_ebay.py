


def getValueOffItemDict( k, dItem, dFields, **kwargs ):
    #
    t = dFields[ k ]
    #
    uValue  = dItem[ t[1] ]
    #
    tRest   = t[ 2 : ]
    #
    for sKey in tRest:
        uValue = uValue[ sKey ]
    #
    sValue  = uValue
    #
    if t[0] is None:
        uReturn = sValue
    else:
        f = t[0]
        uReturn = f( sValue )
    #
    return uReturn




def storeEbayInfo( dItem, dFields, Form, getValue, **kwargs ):
    #
    '''can store a row in either ItemFound or UserItemFound'''
    #
    dNewResult = kwargs
    #
    dNewResult.update( { k: getValue( k, dItem, dFields, **kwargs ) for k in dFields } )
    #
    #if 'iSearch' in dNewResult:
        #print( "dNewResult['iSearch']:", dNewResult['iSearch'] )
    #
    form = Form( data = dNewResult )
    #
    if form.is_valid():
        #
        form.save()
        #
    else:
        #
        print( 'log this error, form did not save' )
        #
        if form.errors:
            for k, v in form.errors.items():
                print( k, ' -- ', str(v) )
        else:
            print( 'no form errors at bottom!' )
    
