from django.urls import resolve
from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from django.shortcuts import render
import re
from lists.views import home_page
from lists.models import Item, List

# Create your tests here.


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list = List()
        list.save()

        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.list = list
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.list = list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(first_saved_item.list, list)
        self.assertEqual(second_saved_item.text, '두 번째 아이템')
        self.assertEqual(second_saved_item.list, list)


class HomePageTest(TestCase):
    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = self.remove_csrf(render_to_string('home.html', request=request))
        # 'home'과 {new_item_text } comparing
        response_decode = self.remove_csrf(response.content.decode())
        self.assertEqual(response_decode, expected_html)
        # html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        #   self.assertIn('<title>To-Do lists</title>', html)
        #   self.assertTrue(html.strip().endswith('</html>'))
        # self.assertTemplateUsed(response, 'home.html')

        # response = home_page(request)
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>',response.content)
        # self.assertTrue(response.content.strip().endswith(b'</html>'))


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response= self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
    #

    def test_displays_all_items(self):
        # Item.objects.create(text= 'itemey 1')
        # Item.objects.create(text= 'itemey 2')
        #
        # response = self.client.get('/lists/the-only-list-in-the-world/')
        #
        # self.assertContains(response, 'itemey 1')
        # self.assertContains(response, 'itemey 2')
        list = List.objects.create()
        Item.objects.create(text= 'itemey 1', list=list)
        Item.objects.create(text= 'itemey 2', list=list)


class NewListTest(TestCase):
    def test_home_page_can_save_a_POST_request(self):
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = '신규 작업 아이템'
        #
        # response = home_page(request)
        self.client.post('/lists/new',
                         data={'item_text': '신규 작업 아이템'}
                         )
        #self.assertIn('신규 작업 아이템', response.content.decode())
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        # same as objects.all(0)
        self.assertEqual(new_item.text, '신규 작업 아이템')
        # expecthtml = render_to_string(
        #     'home.html',
        #     {'new_item_text' : '신규 작업 아이템'}
        # )
        # expected_html = self.remove_csrf(expecthtml)
        # response_decode = self.remove_csrf(response.content.decode())
        #
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/')
        # 코드가 좀길어서 코드냄새가 난다
        # self.assertEqual(response.content.decode(), expected_html)
        # expected_html = self.remove_csrf(render_to_string('home.html', request=request))
        # # 'home'과 {new_item_text } comparing
        # response_decode = self.remove_csrf(response.content.decode())
        # self.assertEqual(response_decode, expected_html)
        # or just insert using render expected_response = render(request,'home.html)
        # self.assertTemplateUsed(response,'home.html')
        # expected_response = render(request,
        #                            'home.html',
        #                            {'new_item_text':'신규 작업 아이템'}
        #                            )
        # self.assertEqual(response_decode, expected_html)

    def test_home_page_redirects_after_POST(self):
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = '신규 작업 아이템'
        # response = home_page(request)
        response= self.client.post(
            '/lists/new',
            data={'item_text': '신규 작업 아이템'}
        )
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
        #
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


    # def test_home_page_displays_all_list_itmes(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #
    #     request = HttpRequest()
    #     response = home_page(request)
    #
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())