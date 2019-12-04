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

