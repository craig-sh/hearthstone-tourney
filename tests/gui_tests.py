import unittest
from selenium import webdriver


class IndexPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/index')

    def test_index_title_display(self):
        self.assertIn("Kai", self.driver.title)

    def test_table_display(self):
        elem = self.driver.find_element_by_name('city_info')
        assert elem.is_displayed()

    def test_valid_health(self):
        table = self.driver.find_element_by_name('city_info')
        # Go through all headers, find which one displays health of City
        for i, e in enumerate(table.find_elements_by_tag_name('th')):
            if e.text == 'Health':
                health_column = i
                break

        # for each row check if health is valid
        for i, row in enumerate(table.find_elements_by_css_selector('tr')):
            if i == 0:
                # skip the first row, its the header, not sure why tr selects it
                continue
            col = row.find_elements_by_css_selector('td')[health_column]
            health = int(col.text)
            assert 0 < health <= 30

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    # ignore warnings because of ResourceWarning when running with chrome
    # https://stackoverflow.com/questions/20885561/warning-from-warnings-module-resourcewarning-unclosed-socket-socket-object
    unittest.main(warnings='ignore')
