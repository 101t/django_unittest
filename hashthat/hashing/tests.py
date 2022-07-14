import imp
from attr import has
from django.test import TestCase
from django.core.exceptions import ValidationError
from selenium import webdriver
from .forms import HashForm
import hashlib
import time

from .models import Hash


class FunctionalTestCase(TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
    
    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        # assert self.browser.page_source.find('install')
        self.assertIn('Enter hash here:', self.browser.page_source)
    
    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element('id', 'id_text')
        text.send_keys('hello')
        self.browser.find_element('name', 'submit').click()
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)
    
    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element('id', 'id_text')
        text.send_keys('hello')
        time.sleep(2)  # wait for AJAX
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

        

    def tearDown(self) -> None:
        self.browser.quit()


class UnitTestCase(TestCase):

    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm(data={'text': 'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', text_hash)
    
    def saveHash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        hash.save()
        return hash

    def test_hash_object(self):
        hash = self.saveHash()
        pulled_hash = Hash.objects.get(hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        hash = self.saveHash()
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertContains(response, 'hello')
    
    def test_bad_data(self):
        def badHash():
            hash = Hash()
            hash.hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824gggggggggggggggggggg'
            hash.full_clean()
        self.assertRaises(ValidationError, badHash)
