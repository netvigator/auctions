

from core.ebay_api_calls    import getApiConfValues
from core.tests.base_class  import TestCasePlus

from pyPks.Time.Convert     import getDateTimeObjFromString
from pyPks.Time.Delta       import getDeltaDaysFromObjs



class ConfFileTokenExpiredTests( TestCasePlus ):
    '''ebay API conf file values tests'''

    def not_here_test_token_expiration(
            self, sWhichToken = None, iDaysTillExpire = None ):
        '''tokens expire, keep tabs'''
        #
        # this test is called in ../test_utils.ConfFileTokenExpiredTests
        #
        if sWhichToken is None:
            sWhichToken  =  'OAuth'
        elif sWhichToken == 'auth-n-auth':
            sWhichToken  =  'Auth-n-Auth'
        #

        if iDaysTillExpire is None: # allows manual testing of expiration msg
            #
            dConfValues     = getApiConfValues()
            #
            sExpiration     = dConfValues[ sWhichToken.lower() ]['expires']
            #
            oExpiration     = getDateTimeObjFromString( sExpiration )
            #
            iDaysTillExpire = - int( getDeltaDaysFromObjs( oExpiration ) )
            #
        #
        if iDaysTillExpire == 0:
            #
            print('')
            print( '### eBay %s token has expired or will soon!!! ###' %
                    sWhichToken )
            #
        elif iDaysTillExpire < 0:
            #
            print('')
            print( '### eBay %s token has expired already!!!      ###' %
                    sWhichToken )
            #
        elif iDaysTillExpire < 32:
            #
            print('')
            print( '### eBay %s token expires in %s days!!! ###' %
                    ( sWhichToken, iDaysTillExpire ) )
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
            print( 'eBay %s token will expire in %s days.' %
                    ( sWhichToken, iDaysTillExpire ) )
            #
        #
        self.assertGreater( iDaysTillExpire, 15 )


