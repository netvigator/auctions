
def getMarketsIntoDatabase():
    #
    '''fetches the markets table text dump,
    uses that to populate the markets table.
    useful for testing, where the database starts empty.'''
    #
    from ebayinfo           import sMarketsTable # in __init__.py
    #
    from core.utils_testing import getTableFromScreenCaptureGenerator
    #
    from .models            import Market
    #
    from Utils.Config       import getBoolOffYesNoTrueFalse as getBool
    #
    oTableIter = getTableFromScreenCaptureGenerator( sMarketsTable )
    #
    lHeader = next( oTableIter )
    #
    dNamePosition = {}
    #
    i = 0
    #
    for sName in lHeader:
        #
        dNamePosition[ sName ] = i
        #
        i += 1
        #
    #
    d = dNamePosition
    #
    for lParts in oTableIter:
        #
        oMarket = Market(
                iEbaySiteID     = int(      lParts[ d['iEbaySiteID'    ] ] ),
                cMarket         =           lParts[ d['cMarket'        ] ],
                cCountry        =           lParts[ d['cCountry'       ] ],
                cLanguage       =           lParts[ d['cLanguage'      ] ],
                bHasCategories  = getBool(  lParts[ d['bHasCategories' ] ] ),
                cCurrencyDef    =           lParts[ d['cCurrencyDef'   ] ],
                iUtcPlusOrMinus = int(      lParts[ d['iUtcPlusOrMinus'] ] ) )
        #
        if lParts[ d['iCategoryVer'] ]:
            oMarket.iCategoryVer= int(      lParts[ d['iCategoryVer'   ] ] )
        #
        if lParts[ d['cUseCategoryID' ] ]:
            oMarket.cUseCategoryID=         lParts[ d['cUseCategoryID' ] ]
        #
        oMarket.save()
        
