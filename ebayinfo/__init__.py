from pyPks.Dir.Get import getMakeDir

# ### notes on how to update ebay categories ###
# ### at the bottom of ebayinfo/utils.py     ###

EBAY_FILES_FOLDER = '/tmp/ebay_files'

getMakeDir( EBAY_FILES_FOLDER )

dMarketsRelated = {
          0 : 100,  # EBAY-US    : EBAY-MOTOR
        100 :   0,  # EBAY-MOTOR : EBAY-US
          2 : 210,  # EBAY-ENCA  : EBAY-FRCA
        210 :   2,  # EBAY-FRCA  : EBAY-ENCA
         23 : 123,  # EBAY-FRBE  : EBAY-NLBE
        123 :  23,  # EBAY-NLBE  : EBAY-FRBE
          3 :   0,  # EBAY-GB    : EBAY-US
          0 :   3 } # EBAY-US    : EBAY-GB


# https://developer.ebay.com/devzone/finding/callref/types/ShippingInfo.html
_tEBAY_SHIPPING_TYPES = (
    ( 0,    'Calculated',
            'Calculated' ),
    ( 1,    'CalculatedDomesticFlatInternational',
            'Calculated Domestic Flat International' ),
    ( 2,    'Flat',
            'Flat' ),
    ( 3,    'FlatDomesticCalculatedInternational',
            'Flat Domestic Calculated International' ),
    ( 4,    'Free',
            'Free' ),
    ( 5,    'FreePickup',
            'Pick Up ONLY!' ),
    ( 6,    'Freight',
            'Freight' ),
    ( 7,    'FreightFlat',
            'Freight Flat' ),
    ( 8,    'NotSpecified',
            'Not Specified' ),
    ( 9,    'FreePickupOption',
            'Free Pick Up Option' ) )
# latter added, some but not all FreePickup items are pick up only!
# utils.setShippingTypeLocalPickupOptional() accesses this info
# tested in searching/tests/test_models.py

# EBAY_SHIPPING_CHOICES tuple used in finders & keepers model definitions
EBAY_SHIPPING_CHOICES = tuple(
        [ ( t[0], t[2] ) for t in _tEBAY_SHIPPING_TYPES ] )

# dEBAY_SHIPPING_CHOICE_CODE used in getEbayShippingChoiceCode()
dEBAY_SHIPPING_CHOICE_CODE = dict(
        [ ( t[1], t[0] ) for t in _tEBAY_SHIPPING_TYPES ] )


def getEbayShippingChoiceCode( sChoice ):
    #
    # logically this would be in ebayinfo.utils
    # but that gets hard to debug errors
    #
    return dEBAY_SHIPPING_CHOICE_CODE.get( sChoice )
