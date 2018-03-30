from django.core.exceptions import ValidationError
from django.test            import TestCase

from ..validators           import isPriorityValid


class TestIsPriorityValid( TestCase ):
    ''' test isPriorityValid() '''
    
    
    def test_valid_priorities( self ):
        #
        try:
            isPriorityValid( 'A1' )
            isPriorityValid( 'Z9' )
            isPriorityValid( 'AZ' )
        except ValidationError as e:
            self.fail("isPriorityValid() raised ValidationError unexpectedly!")


    def test_invalid_priorities( self ):
        #
        with self.assertRaises( ValidationError ):
            isPriorityValid( 'a1' )

        with self.assertRaises( ValidationError ):
            isPriorityValid( '9Z' )

        with self.assertRaises( ValidationError ):
            isPriorityValid( '!@' )

        with self.assertRaises( ValidationError ):
            isPriorityValid( '!' )

        with self.assertRaises( ValidationError ):
            isPriorityValid( '!@#' )

