from django.test import TestCase

import datetime

# Create your tests here.

from .utils     import oUserOne, getDateTimeObj

from .ebay_wrapper  import oEbayConfig

class CoreUserTests(TestCase):
    """User tests."""

    def test_get_user(self):
        
        self.assertEquals( oUserOne.username, 'netvigator')


class EbayWrapperTests(TestCase):
    '''ebay wrapper tests'''
    
    def test_get_ini_values(self):
        
        self.assertEquals( oEbayConfig['call']['global_id'], 'EBAY-US' )
        
        self.assertEquals( oEbayConfig['research']['Token'], 'ENTER_HERE' )
        


class DateTimeImportTests(TestCase):
    '''test converting ebay string dates into python datetime objects'''
    def test_convert_ebay_string_DateTime(self):
        #
        self.assertEquals( getDateTimeObj( "2017-12-15T05:22:47.000Z" ),
                           datetime.datetime(2017, 12, 15, 5, 22, 47) )

'''
oTest = {
    'cNationality': ('Nationality', 'C'),
    'iUser_id': ('Owner', 1), 
    'cLookFor': ('Considered A Hit If This Text Is Found (Each Line '
                 'Evaluated Separately, Put Different Look For Tests '
                 'On Different Lines)', None),
    'iLegacyKey': ('Legacy Key', 3140),
    'cComment': ('Comments', ''),
    'tLegacyModify': ('Legacy Row Updated On', None),
    'tModify': ('Updated On',
            datetime.datetime(2017, 11, 5, 6, 9, 49, 259192, tzinfo=<UTC>)),
    'id': ('Id', 1021),
    'cTitle': ('Brand Name', 'Addison'),
    'tLegacyCreate': ('Legacy Row Created On',
            datetime.datetime(2001, 9, 16, 23, 49, 9, tzinfo=<UTC>)),
    'tCreate': ('Created On',
            datetime.datetime(2017, 11, 5, 6, 9, 49, 259160, tzinfo=<UTC>)),
    'bAllOfInterest': ('Want Everything From This Brand?', False),
    'bWanted': ('Want Anything From This Brand?', True),
    'cExcludeIf': ('Not A Hit If This Text Is Found (Each Line Evaluated '
                   'Separately, Put Different Exclude Tests On Different '
                   'Lines)', ''),
    'iStars': ('Desireability, 10 Star Brand Is Most Desireable', 5),
    'iUser_id': ('Owner', 1),
    'NotOnList': ('blah blah blah', None }
'''