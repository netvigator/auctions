# separate file for these avoids circular import issue

from django_webtest         import WebTest
from test_plus.test         import TestCase, CBVTestCase


class TestCasePlus( TestCase ):
    """subclass of test_plus.test TestCase
    allows implementation of project specific helper methods"""
    #
    pass



class TestViewPlus( CBVTestCase ):
    """subclass of test_plus.CBVTestCase
    allows implementation of project specific helper methods"""
    #
    pass




class WebTestCase( WebTest ):
    """subclass of test_plus.test TestCase
    allows implementation of project specific helper methods"""
    #
    pass

