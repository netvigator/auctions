

from core.ebay_api_calls    import getApiConfValues
from core.tests.base        import TestCasePlus

from pyPks.Time.Convert     import getDateTimeObjFromString
from pyPks.Time.Delta       import getDeltaDaysFromObjs



class ConfFileTokenExpiredTests( TestCasePlus ):
    '''ebay API conf file values tests'''

    def not_here_test_token_expiration( self ):
        '''tokens expire, keep tabs'''
        #
        dConfValues     = getApiConfValues()
        #
        sExpiration     = dConfValues['auth']['expires']
        #
        oExpiration     = getDateTimeObjFromString( sExpiration )
        #
        iDaysTillExpire = - int( getDeltaDaysFromObjs( oExpiration ) )
        #
        if iDaysTillExpire <= 0:
            #
            print('')
            print( '### eBay AUTH token has expired or will soon!!! ###' )
            #
        elif iDaysTillExpire < 32:
            #
            print('')
            print( '### eBay AUTH token expires in %s days!!! ###' % iDaysTillExpire )
        #
        if iDaysTillExpire < 32:
            #
            print( '### obtain new one from eBay developer webiste! ###' )
            print( '### remember to update server with new token!!! ###' )
            print('')
            #
        else:
            #
            print('')
            print( 'eBay AUTH token will expire in %s days.' % iDaysTillExpire )
            #
        #
        self.assertGreater( iDaysTillExpire, 15 )


