from django.test import TestCase
from django.contrib.auth import get_user_model
from django_webtest import WebTest

from forms import CommentForm
from models import Entry, Comment

class BaseTestCase(WebTest):
    def setUp(self):
        self.user = get_user_model().objects.create(username='tester')
        self.entry = Entry.objects.create(title='1-title', body='1-body',\
                                          author=self.user)

class ProjectTest(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class EntryModelTest(TestCase):
    def test_unicode_repr(self):
        entry = Entry(title="testEntry")
        self.assertEqual(unicode(entry), entry.title)

    def test_name_pluralization(self):
        self.assertEqual(unicode(Entry._meta.verbose_name_plural), "entries")

    def test_get_absoulte_url(self):
        user = get_user_model().objects.create(username='tester')
        entry = Entry.objects.create(title='1-title', author=user)
        self.assertIsNotNone(entry.get_absolute_url())

class CommentModelTest(TestCase):
    def test_unicode_repr(self):
        comment = Comment(name='tester')
        self.assertEqual(unicode(comment), comment.name)

class HomePageTests(BaseTestCase):
    """ Test whether the blog entries show up on the homepage """

    def test_one_entry(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_entries(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        Entry.objects.create(title='2-title', body='2-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-title')
        self.assertContains(response, '2-body')

    def test_zero_entries(self):
        self.entry.delete()
        response = self.client.get('/')
        self.assertContains(response, 'Mice ate my blog :(')
    
class EntryViewTest(BaseTestCase):
    
    def test_basic_view(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_title_present(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.title)

    def test_body_present(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.body)

    def test_view_page(self):
        page = self.app.get(self.entry.get_absolute_url())
        self.assertEqual(len(page.forms), 1)

class CommentFormTest(BaseTestCase):
    unicode_err_str = [unicode('This field is required.')]

    def test_init(self):
        CommentForm(entry=self.entry)
   
    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()
    
    def test_valid_data(self):
        form = CommentForm({
                'name': 'foo boo',
                'email': 'yogi@yellowstone.com',
                'body': 'Nice Blog!',
                }, entry = self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, 'foo boo')
        self.assertEqual(comment.email, 'yogi@yellowstone.com')
        self.assertEqual(comment.body, 'Nice Blog!')
        self.assertEqual(comment.entry, self.entry)

    def test_blank_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name' : self.unicode_err_str, 
            'email': self.unicode_err_str, 
            'body' : self.unicode_err_str,
        })

    def test_form_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required")

    def test_form_success(self):
        page = self.app.get(self.entry.get_absolute_url())
        page.form['name'] = 'God'
        page.form['email'] = 'g@foo.com'
        page.form['body'] = 'Omniscence'
        page = page.form.submit()
        self.assertRedirects(page, self.entry.get_absolute_url())
    
