from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        inputbox = self.햣browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        inputbox.send_keys('공작 깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: 공작 깃털 사기' for row in rows),
                        "신규 작업이 테이블에 표시되지 않는다"
        )

        self.fail('Finish the Test!')

    # if __name__ == '__main__':
    #     unittest.main(warnings='ignore')
#
# browser = webdriver.Firefox(executable_path='/Users/soojin/Downloads/geckodriver')
# browser.get('http://localhost:8000')
# assert 'To-Do' in browser.title
# executable_path='/Users/soojin/Downloads/geckodriver