from django.test import TestCase, RequestFactory
from pagination import make_pagination_range, make_pagination  

class PaginationTestCase(TestCase):
    def setUp(self):
        """
        Configura os dados e as variáveis necessárias para os testes.
        """
        self.page_range = range(1, 11)  # Simula 10 páginas
        self.queryset = list(range(1, 21))  # Simula 20 itens no queryset
        self.factory = RequestFactory()  # Para criar requisições simuladas

    def test_make_pagination_range(self):
        """
        Testa o cálculo do intervalo de páginas.
        """
        # Caso 1: Intervalo básico no meio
        result = make_pagination_range(self.page_range, qty_pages=4, current_page=5)
        self.assertEqual(list(result['pagination']), [4, 5, 6, 7])  # Verifica o intervalo correto
        self.assertTrue(result['first_page_out_of_range'])  # Página atual > middle_range, deve ser True
        self.assertTrue(result['last_page_out_of_range'])  # Intervalo não excede o final

        # Caso 2: No início do intervalo
        result = make_pagination_range(self.page_range, qty_pages=4, current_page=1)
        self.assertEqual(list(result['pagination']), [1, 2, 3, 4])
        self.assertFalse(result['first_page_out_of_range'])  # No início, deve ser False
        self.assertTrue(result['last_page_out_of_range'])  # Há páginas após o intervalo

        # Caso 3: No final do intervalo
        result = make_pagination_range(self.page_range, qty_pages=4, current_page=10)
        self.assertEqual(list(result['pagination']), [7, 8, 9, 10])
        self.assertTrue(result['first_page_out_of_range'])  # Há páginas antes do intervalo
        self.assertFalse(result['last_page_out_of_range'])  # Última página, nada além

    def test_make_pagination(self):
        """
        Testa a integração da paginação completa com o Paginator do Django.
        """
        # Caso 1: Página válida no meio do intervalo
        request = self.factory.get('/?page=2')
        page_obj, paginator_range = make_pagination(request, self.queryset, per_page=5, qty_pages=4)

        self.assertEqual(list(page_obj.object_list), [6, 7, 8, 9, 10])  # Itens da página 2
        self.assertEqual(list(paginator_range['pagination']), [1, 2, 3, 4])  # Intervalo correto de páginas

        # Caso 2: Página inválida na URL
        request = self.factory.get('/?page=abc')
        page_obj, paginator_range = make_pagination(request, self.queryset, per_page=5, qty_pages=4)

        self.assertEqual(list(page_obj.object_list), [1, 2, 3, 4, 5])  # Página inicial como fallback
        self.assertEqual(list(paginator_range['pagination']), [1, 2, 3, 4])  # Intervalo correto para início

        # Caso 3: Página além do limite
        request = self.factory.get('/?page=10')
        page_obj, paginator_range = make_pagination(request, self.queryset, per_page=5, qty_pages=4)

        self.assertEqual(list(page_obj.object_list), [16, 17, 18, 19, 20])  # Última página
        self.assertEqual(list(paginator_range['pagination']), [1, 2, 3, 4])  # Intervalo ajustado para o final

        # Caso 4: Página inicial (sem parâmetro 'page')
        request = self.factory.get('/')
        page_obj, paginator_range = make_pagination(request, self.queryset, per_page=5, qty_pages=4)

        self.assertEqual(list(page_obj.object_list), [1, 2, 3, 4, 5])  # Página inicial
        self.assertEqual(list(paginator_range['pagination']), [1, 2, 3, 4])  # Intervalo inicial