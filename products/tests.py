from django.test import TestCase
from models import Product
import json
# Create your tests here.


class ProductTests(TestCase):
    def setUp(self):
        Product.objects.create(name="test product 1",
                               price=100,
                               category="test 1")
        Product.objects.create(name="test product 2",
                               price=1000,
                               category="test 2")

    def test_getList(self):
        product_list = Product.objects.all()
        self.assertEqual(product_list.count(), 2)
        self.assertEqual(product_list[0].id, 1)
        self.assertEqual(product_list[1].id, 2)

    def test_search(self):
    	data = [{"fields": {"category": "test 1", "price": 100, "name": "test product 1"}, "model": "products.product", "pk": 1}]
        resp = self.client.get('/search?q=1')
        self.assertEqual(resp.status_code, 200)
        resp.content  = json.loads(resp.content)[0]['fields']['name']
        self.assertEqual(resp.content, data[0]['fields']['name'])

    def test_delete(self):
        resp = self.client.get('/delete/1/')
        resp_content = json.loads(resp.content)
        self.assertEqual(resp_content['status'], True)
        product_list = Product.objects.all()
        self.assertEqual(product_list.count(), 1)

    def test_read(self):
        resp = self.client.get('/read/2/')
        resp_content = json.loads(resp.content)
        self.assertEqual(resp_content['name'], "test product 2")