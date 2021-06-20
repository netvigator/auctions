

from core.ebay_api_calls    import getApiConfValues
from core.tests.base_class  import TestCasePlus

from pyPks.Time.Convert     import getDateTimeObjFromString
from pyPks.Time.Delta       import getDeltaDaysFromObjs



class ConfFileTokenExpiredTests( TestCasePlus ):
    '''ebay API conf file values tests'''

    def not_here_test_token_expiration( self, iDaysTillExpire = None ):
        '''tokens expire, keep tabs'''
        #
        # this test is called in ../test_utils.ConfFileTokenExpiredTests
        #
        if iDaysTillExpire is None: # allows manual testing of expiration msg
            #
            dConfValues     = getApiConfValues()
            #
            sExpiration     = dConfValues['auth']['expires']
            #
            oExpiration     = getDateTimeObjFromString( sExpiration )
            #
            iDaysTillExpire = - int( getDeltaDaysFromObjs( oExpiration ) )
            #
        #
        if iDaysTillExpire == 0:
            #
            print('')
            print( '### eBay AUTH token has expired or will soon!!! ###' )
            #
        elif iDaysTillExpire < 0:
            #
            print('')
            print( '### eBay AUTH token has expired already!!!      ###' )
            #
        elif iDaysTillExpire < 32:
            #
            print('')
            print( '### eBay AUTH token expires in %s days!!! ###' % iDaysTillExpire )
        #
        if iDaysTillExpire < 32:
            #
            print('')
            print( '### obtain new one from eBay developer webiste! ###' )
            print( '### remember to update server with new token!!! ###' )
            #
        else:
            #
            print('')
            print( 'eBay AUTH token will expire in %s days.' % iDaysTillExpire )
            #
        #
        self.assertGreater( iDaysTillExpire, 15 )


