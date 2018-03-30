from string    import ascii_uppercase, digits


# avoiding circular import problems!

def getPriorityChoices( oModel = None, oUser = None, sInclude = None ):
    #
    '''get list of priorities for Search.cPriority'''
    #
    tAlpha = tuple( ascii_uppercase )
    tNums  = tuple( digits )[1:]
    #
    iterAll = ( '%s%s' % (A, N) for N in tNums for A in tAlpha )
    #
    setAll = set( iterAll )
    #
    if sInclude:
        def doOmitFromChoices( s ): return s != sInclude
    else:
        def doOmitFromChoices( s ): return True
    #
    if oUser is not None and oModel is not None:
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
