from string         import ascii_uppercase, digits

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

WITH_AND_JOINERS = ( 'with', 'and', '&' )

DROP_AFTER_THIS = (
    '(?<=[\W.,!?:;])'  # look back for this if u find any of the following
    '(?:'              # non grouping (saves CPU ticks)
        r'for\b|'
        r'fits\b|'
        r'holds\b|'
        r'tests*\b|'
        r'tested (?:on|with)\b|'
        r'from\b|'
        r'ala\b|'
        r'used* (?:with|in|on)\b|'
        r'same as\b|'
        r'=\b|'
        r'not\b|'
        r'like\b|'
        r'compatible with\b|'
        r'variant of\b|'
        r'similar to\b)' )

SCRIPT_TEST_FILE        = '/tmp/auction_script_test.txt'

if settings.TESTING:
    SEARCH_FILES_ROOT = '/tmp/searches-test'
else:
    SEARCH_FILES_ROOT = '/tmp/searches'


getMakeDir( SEARCH_FILES_ROOT )


def getPriorityChoices( oModel = None, oUser = None, sInclude = None ):
    #
    '''get list of priorities for Search.cPriority'''
    #
    tAlpha = tuple( ascii_uppercase )
    tNums  = tuple( digits )[1:]
    #
    # iterAll = ( '%s%s' % (A, N) for N in tNums for A in tAlpha )
    #
    setAll = set( ( '%s%s' % (A, N) for N in tNums for A in tAlpha ) )
    #
    if sInclude:
        def doOmitFromChoices( s ): return s != sInclude
    else:
        def doOmitFromChoices( s ): return True
    #
    if oUser and oModel:
        #
        oSearches = oModel.objects.filter( iUser = oUser )
        #
        setAll.difference_update( ( oSearch.cPriority
                                    for oSearch in oSearches
                                    if doOmitFromChoices( oSearch.cPriority ) ) )
        #
    #
    lAll = list( setAll )
    #
    lAll.sort()
    #
    return tuple( ( ( s, s ) for s in lAll ) )


ALL_PRIORITIES = getPriorityChoices()

