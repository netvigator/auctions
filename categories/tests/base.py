
from core.tests.base import BaseUserWebTestCase

from ..models        import Category


class TestCategoryFormValidation( BaseUserWebTestCase ):

    ''' Category Form Tests '''
    # helpful:
    # https://stackoverflow.com/questions/2257958/django-unit-testing-for-form-edit

    def setUp(self):
        #
        super().setUp()
        #
        oCategory = Category(
                cTitle  = "Gadget",
                cLookFor= "thingamajig",
                iUser   = self.user1 )
        #
        oCategory.save()
        #
        self.iCategoryID = oCategory.id
        #
        self.loginWebTest()

