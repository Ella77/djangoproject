from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.common.exceptions import StaleElementReferenceException
import sys
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
        # self.browser.implicitly_wait(10)

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)


        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    # @classmethod
    # def setUpClass(cls):
    #     for arg in sys.argv :
    #         if 'liveserver' in arg:
    #             cls.server_url = 'http://' + arg.split('=')[1]
    #             cls.live_server_url = ''
    #             return
    #     super().setUpClass()
    #     cls.server_url = cls.live_server_url
    #
    # def tearDown(self):
    #     self.browser.quit()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     if cls.server_url == cls.live_server_url:
    #         super().tearDownClass()

    def stale_aware_for_action(self, action):
        while(True):
            try:
                action()
                break
            except StaleElementReferenceException:
                continue

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    #목록 저장하고 있는지 궁금


    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        # self.assertIn('To-Do', self.browser.title)
        # header_text = self.browser.find_element_by_tag_name('h1').text
        # self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )
        inputbox.send_keys('공작 깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        with self.wait_for_page_load(timeout=1):
            self.check_for_row_in_list_table('1: 공작 깃털 사기')
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('깃털 모아서 날기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        with self.wait_for_page_load(timeout=1):
            self.check_for_row_in_list_table('1: 공작 깃털 사기')
            self.check_for_row_in_list_table('2: 깃털 모아서 날기')

        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작 깃털 사기', page_text)
        self.assertNotIn('깃털 모아서 날기', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작 깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)
        # def check_for_first_item():
        #         # def check_for_second_item():
        #         #     def check_for_row_in_list_table(self, row_text):
        #         #         table = self.browser.find_element_by_id('id_list_table')
        #         #         rows = table.find_elements_by_tag_name('tr')
        #         #         self.assertIn(row_text, [row.text for row in rows])
        #         #
        #         #     with self.wait_for_page_load(timeout=10):
        #         #         self.check_for_row_in_list_table('2: 깃털 모아서 날기')
        #         #
        #         # def insert_second_item_to_inputbox():
        #         #     inputbox2 = self.browser.find_element_by_id('id_new_item')
        #         #     self.assertEqual(
        #         #         inputbox2.get_attribute('placeholder'),
        #         #         '작업 아이템 입력'
        #         #     )
        #         #     inputbox2.send_keys('깃털 모아서 날기')
        #         #     inputbox2.send_keys(Keys.ENTER)

        #
        # self.stale_aware_for_action(check_for_first_item)
        #
        # self.stale_aware_for_action(insert_second_item_to_inputbox)
        #
        # self.stale_aware_for_action(check_for_second_item)
        # self.stale_aware_for_action(check_for_first_item)




        self.fail('Finish the Test!')




        #
       # import time
        #time.sleep(6)

        #self.assertTrue(
            #any(row.text == '1: 공작 깃털 사기' for row in rows),
           #             "신규 작업이 테이블에 표시되지 않는다 -- 해당 텍스트 :\n%s" % (
          #                  table.text,
         #   )
        #)



    # if __name__ == '__main__':
    #     unittest.main(warnings='ignore')
#
# browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
# browser.get('http://localhost:8000')
# assert 'To-Do' in browser.title
# executable_path='/Users/soojin/Downloads/geckodriver