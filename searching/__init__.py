from django.conf    import settings

from pyPks.Dir.Get  import getMakeDir

WORD_BOUNDARY_MAX           = 5

RESULTS_FILE_NAME_PATTERN   = 'Search_%s_%s_ID_%s_p_%s_.json'
# variables: sMarket, sUserName, iSearchID, iPageNumb
# sName.split('_') gives this:
# ['Search',sMarket,sUserName,'ID',iSearchID,'p',iPageNumb,'.json' ]
#   0       1       2          3   4          5  6          7
#
# when selling on the ebay site, condition is optional
# https://developer.ebay.com/DevZone/guides/ebayfeatures/Development/Desc-ItemCondition.html


DROP_AFTER_THIS = (
    '(?<=[\W.,!?:;])'  # look back for this if u find any of the following
    '(?:'              # non grouping (saves CPU ticks)
        r'for\b|'
        r'fits\b|'
        r'tests*\b|'
        r'tested (?:on|with)\b|'
        r'from\b|'
        r'ala\b|'
        r'used (?:with|in|on)\b|'
        r'same as\b|'
        r'compatible with\b|'
        r'variant of\b|'
        r'similar to\b)' )

SCRIPT_TEST_FILE            = '/tmp/auction_script_test.txt'

if settings.TESTING:
    SEARCH_FILES_FOLDER     = '/tmp/searches-test'
else:
    SEARCH_FILES_FOLDER     = '/tmp/searches'


getMakeDir( SEARCH_FILES_FOLDER )

