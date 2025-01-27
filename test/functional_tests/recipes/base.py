from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from utils.browser import make_chrome_browser
from recipes.templates.recipes.test.test_recipe_base import RecipeMixin

class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, seconds=5):
        time.sleep(seconds)