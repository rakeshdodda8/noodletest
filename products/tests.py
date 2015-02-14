from django.test import TestCase
from models import Product
import json
from django.http import HttpRequest
# Create your tests here.


class ProductTests(TestCase):
    def setUp(self):
        self.body_attr = "body"
        Product.objects.create(name="test product 1",
                               price=100,
                               category="test 1")
        Product.objects.create(name="test product 2",
                               price=1000,
                               category="test 2")

    def test_getList(self):
        resp = self.client.get('/get_list')
        obj = json.loads(resp.content.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(obj[0]['name'], "test product 1")
        self.assertEqual(obj[1]['name'], "test product 2")

    def test_search(self):
    	resp = self.client.get('/search?q=1')
        obj  = json.loads(resp.content)[0]['fields']
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(obj['name'], "test product 1")

    def test_delete(self):
        resp = self.client.get('/delete/1/')
        resp_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_content['status'], True)
        

    def test_read(self):
        resp = self.client.get('/read/2/')
        resp_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_content['name'], "test product 2")

    def test_update(self):
        request = HttpRequest()
        post_data = '{"id": 1, "name": "test product updated", "price": 423, "category": "test"}'
        setattr(request, "_" + self.body_attr, post_data)
        resp = self.client.post('/update',data=post_data, content_type='application/json')
        obj = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(obj['status'], "true")
        #import pdb
        #pdb.set_trace()
