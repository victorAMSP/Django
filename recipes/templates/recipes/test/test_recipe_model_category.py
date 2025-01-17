from django.core.exceptions import ValidationError
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase
from django.urls import reverse

class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_category_model_string_representarion_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )