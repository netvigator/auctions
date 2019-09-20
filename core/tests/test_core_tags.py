from django.utils                   import timezone

from core.utils_test                import TestCasePlus

from categories.models              import Category
from categories.tests.test_forms    import TestFormValidation

from ..templatetags.core_tags       import (
                                        getIsoDateTime,
                                        getDashForReturn,
                                        getLineBreakForReturn,
                                        getDashForReturnButDropLast,
                                        getLastDroppedFromCommaSeparatedString,
                                        model_name,
                                        model_name_plural,
                                        field_name )

from pyPks.Time.Test                import isISOdatetime

class GetDashForReturnTests( TestCasePlus ):
    '''get dash for return tests'''
    #
    s = 'abc\rdef\nghi\rklm'
    #

    def test_get_dash_for_return(self):
        #
        sExpect = 'abc - def - ghi - klm'
        #
        self.assertEqual( getDashForReturn( self.s ), sExpect )


    def test_get_dash_for_return_but_drop_last(self):
        #
        sExpect = 'abc - def - ghi'
        #
        self.assertEqual( getDashForReturnButDropLast( self.s ), sExpect )


    def test_get_line_break_for_return( self ):
        #
        sExpect = 'abc<BR>def<BR>ghi<BR>klm'
        #
        self.assertEqual( getLineBreakForReturn( self.s ), sExpect )



class GetDropLastForCommaSeparatorTests( TestCasePlus ):
    '''get drop last for comma separator tests'''
    #
    s = 'abc, def, ghi, klm'
    #

    def test_get_drop_last(self):
        #
        sExpect = 'abc, def, ghi'
        #
        self.assertEqual( getLastDroppedFromCommaSeparatedString( self.s ), sExpect )









class MiscCoreTagTests( TestCasePlus ):
    ''' test getIsoDateTime '''

    def test_get_ISO_date_time( self ):
        #
        self.assertTrue( isISOdatetime( getIsoDateTime( timezone.now() ) ) )
        #

    #def test_get_nbsp( self ):
        ##
        #s = 'a b c d e'
        ##
        #self.assertEquals( getNbsp(s), 'a&nbsp;b&nbsp;c&nbsp;d&nbsp;e' )
        ##

#class NbspTests( TestCasePlus ):
    #'test substituting &nbsp; for spaces'
    #def test_Nbsp(self):
        ##
        #self.assertEqual( getNbsp( "how now brown cow" ),
                           #"how&nbsp;now&nbsp;brown&nbsp;cow" )


class TestNameFilters( TestFormValidation ):
    ''' test model_name, model_name_plural & field_name '''

    def setUp( self ):
        #
        super( TestNameFilters, self ).setUp()
        #
        self.oCategory = Category.objects.get( id = self.iCategoryID )

    def test_model_name( self ):
        #
        self.assertEquals( model_name( self.oCategory ), 'Category' )

    def test_model_name_plural( self ):
        #
        self.assertEquals( model_name_plural( self.oCategory ), 'Categories' )

    def test_field_name( self ):
        #
        self.assertEquals( field_name( self.oCategory, 'cTitle' ),
                           'Category Description' )
