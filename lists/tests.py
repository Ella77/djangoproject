from django.urls import resolve
from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from django.shortcuts import render
import re
from lists.views import home_page
from lists.models import Item
class HomePageTest(TestCase):

    def remove_csrf(self,origin):
        csrf_regex =r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex,'',origin)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_returns_correct_html(self):

        request =HttpRequest()
        response =home_page(request)
        expected_html = self.remove_csrf(render_to_string('home.html', request=request))
        # 'home'과 {new_item_text } comparing
        response_decode = self.remove_csrf(response.content.decode())
        self.assertEqual(response_decode, expected_html)
       # html = response.content.decode('utf8')
     # self.assertTrue(html.startswith('<html>'))
     #   self.assertIn('<title>To-Do lists</title>', html)
     #   self.assertTrue(html.strip().endswith('</html>'))
       #self.assertTemplateUsed(response, 'home.html')

        #response = home_page(request)
       #self.assertTrue(response.content.startswith(b'<html>'))
        #self.assertIn(b'<title>To-Do lists</title>',response.content)
        #self.assertTrue(response.content.strip().endswith(b'</html>'))


    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response =  home_page(request)

        self.assertIn('신규 작업 아이템', response.content.decode())
        #self.assertTemplateUsed(response,'home.html')
# Create your tests here.

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text ='첫 번째 아이템'
        first_item.save()
        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items =Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item = saved_items[0]
        second_saved_item =saved_items[1]
        self.assertEqual(first_saved_item.text,'첫 번째 아이템')
        self.assertEqual(second_saved_item.text,'두 번째 아이템')