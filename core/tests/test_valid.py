from django.core.exceptions     import ValidationError
from django.test                import TestCase

from ..validators               import gotTextOutsideParens


class GotTextOutsideParensTests(TestCase):
    #
    ''' test the gotTextOutsideParens() validator '''
    #
    def setUp(self):
        self.s1 = 'abcde (efghijk)'
        self.s2 = 'abcde'
        self.s3 = ' (efghijk) '

    def test_OK_titles( self ):
        #
        try:
            gotTextOutsideParens( self.s1 )
            gotTextOutsideParens( self.s2 )
        except ValidationError:
            self.fail("gotTextOutsideParens() raised ValidationError unexpectedly!")
    #
    def test_bad_title( self ):
        #
        with self.assertRaises( ValidationError ):
            gotTextOutsideParens( self.s3 )

