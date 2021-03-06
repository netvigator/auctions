from django.utils           import timezone

from .base                  import TestCasePlus

from categories.models      import Category

from categories.tests.base  import TestCategoryFormValidation

from ..tags.core_tags       import (getDashForReturn,
                                    getLineBreakForReturn,
                                    getDashForReturnButDropLast,
                                    model_name,
                                    model_name_plural,
                                    field_name )

from pyPks.Time.Test        import isISOdatetime

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




class TestNameFilters( TestCategoryFormValidation ):
    ''' test model_name, model_name_plural & field_name '''

    def setUp( self ):
        #
        super().setUp()
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
                           'Category Name' )
