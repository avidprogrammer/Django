"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from contacts.models import Contact, Address
from django.test import TestCase

class ContactsTest(TestCase):
    def test_name(self):
        """
        Tests contact is created correctly
        """
        km = Contact(fname='abc', lname='xyz', email='abc_xyz@asti.com')
        self.assertEquals(str(km), 'abc xyz abc_xyz@asti.com')

    def test_address(self):
        """
        Tests addresses are created correctly
        """
        strt ='13058 Rose Petal Cir'
        cty = 'Herndon'
        zip = '20171'
        st = 'VA'
        add1 = Address(street=strt,
                       city=cty,
                       state=st,
                       zip=zip)
        self.assertEquals(str(add1), '\n'.join([strt, cty, st, zip]))                       
                    
