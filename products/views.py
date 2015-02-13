from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from utils import get_query
from models import Product
from products.forms import ProductForm

class JSONResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        super(JSONResponse, self).__init__(args, kwargs)
        self.status_code = 200
        self['Content-Type'] = 'application/json'

#Home page with product creation form
def index(request):
	return render_to_response("home.html", RequestContext(request, {'form': ProductForm()}))

#returns json of all the products
def get_list(request):
	products = Product.objects.all()
	results = [obj.as_json() for obj in products]
	return JSONResponse(json.dumps(results, cls=DjangoJSONEncoder))

#creates a product
@require_http_methods(["POST"])
def create(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()
	return HttpResponseRedirect(reverse('index'),)

#returns json response for single product
@require_http_methods(["GET"])
def read(request, pk):
	try:
		product = Product.objects.get(id=pk)
		response = {"id": product.id, "name": product.name, "price":product.price, "category": product.category }
	except Product.DoesNotExist:
		response = {"status": False, "Description": "Product Not Found"}
	return JSONResponse(json.dumps(response, cls=DjangoJSONEncoder))

#updates single product
@csrf_exempt
@require_http_methods(["POST"])
def update(request):
	#data = urlencode(json.loads(request.body))
	#request.POST = QueryDict(data)
	if request.method == "POST":
		form_data = json.loads(request.body)
		pk = form_data.get('id')
		try:
			product = Product.objects.get(id=pk)
			product.name = form_data.get('name')
			product.price = form_data.get('price')
			product.category = form_data.get('category')
			product.save()
			response = {"status": True}
		except Exception, e:
			print e
			response = {"status": False, "Description": "Problem Updating Product"}
		return JSONResponse(json.dumps(response, cls=DjangoJSONEncoder))

#deletes a product and returns json
@require_http_methods(["GET"])
def delete(request, pk):
	products = Product.objects.filter(id=pk)
	for product in products: product.delete()
	if products:
		response = {"status": True}
	else:
		response = {"status": False, "Description": "Product Not Found"}
	return JSONResponse(json.dumps(response, cls=DjangoJSONEncoder))

#uses search functionality from utils.py and returns json
def search(request):
	found_entries = []
	if ('q' in request.GET) and request.GET['q'].strip():
		#get_query function performs search on two fields (name and category)
		entry_query = get_query(request.GET['q'], ['name', 'category',])
		found_entries = Product.objects.filter(entry_query)
	found_entries = serializers.serialize("json", found_entries)
	#print JSONResponse(found_entries)
	return JSONResponse(found_entries)
