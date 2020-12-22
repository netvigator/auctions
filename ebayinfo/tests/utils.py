

from pyPks.Utils.Config     import getBoolOffYesNoTrueFalse as getBool
from pyPks.Utils.DataBase   import getTableDict


def getMarketsDict( sMarketsTable ):
    #
    dConverts = dict(
        bHasCategories  = getBool,
        iEbaySiteID     = int,
        iCategoryVer    = int,
        iUtcPlusOrMinus = int )
    #
    setNone4Empty = ( 'cUseCategoryID', )
    #
    dMarkets = getTableDict(
                sMarketsTable, 'iEbaySiteID', dConverts, setNone4Empty )
    #
    return dMarkets

