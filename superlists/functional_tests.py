from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.common.exceptions import StaleElementReferenceException

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    def stale_aware_for_action(self, action):
        while(True):
            try:
                action()
                break
            except StaleElementReferenceException:
                continue
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        def insert_second_item_to_inputbox():
         inputbox = self.browser.find_element_by_id('id_new_item')
            self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

            inputbox.send_keys('공작 깃털 사기')
            inputbox.send_keys(Keys.ENTER)
            self.stale_aware_for_action(insert_second_item_to_inputbox)

        #
       # import time
        #time.sleep(6)

            table = self.browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
        #self.assertTrue(
            #any(row.text == '1: 공작 깃털 사기' for row in rows),
           #             "신규 작업이 테이블에 표시되지 않는다 -- 해당 텍스트 :\n%s" % (
          #                  table.text,
         #   )
        #)
            self.assertIn('1: 공작 깃털 사기', [row.text for row in rows])

            self.fail('Finish the Test!')
        def check_for_first_item():
            self.check_for_row_in_list_table('1: 공작 깃털 사기')
        def check_for_second_item():
            self.check_for_row_in_list_table('2: 깃털 모아서 날기')\
        self.stale_aware_for_action(check_for_first_item)
        self.stale_aware_for_action(check_for_second_item)
    # if __name__ == '__main__':
    #     unittest.main(warnings='ignore')
#
# browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
# browser.get('http://localhost:8000')
# assert 'To-Do' in browser.title
# executable_path='/Users/soojin/Downloads/geckodriver