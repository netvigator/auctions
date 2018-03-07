from django.test        import TestCase

from ..utils_testing    import BaseUserTestCase



class getFindersTest(BaseUserTestCase):
    
    ''' test getFinders for Brands, Categories & Models '''
    
    def setUp(self):
        #
        super( getFindersTest, self ).setUp()
        #
        self.client.login(username ='username1', password='mypassword')
        #
        self.oBrand = Brand(
            cTitle      = "Cadillac",
            cLookFor    = "Caddy",
            cExcludeIf  = 'golf',
            iStars      = 5,
            iUser = self.user1 )
        #
        self.oBrand.save()
        #
        self.oCategory = Category(
            cTitle      = "Widgets",
            iStars      = 5,
            iUser       = self.user1 )
        self.oCategory.save()
        self.CategoryID = self.oCategory.id
        #
        oModel = Model(
            cTitle      = "Fleetwood",
            cLookFor    = "Woodie",
            iStars      = 5,
            iBrand      = self.oBrand,
            iCategory   = self.oCategory,
            iUser       = self.user1 )
        oModel.save()

