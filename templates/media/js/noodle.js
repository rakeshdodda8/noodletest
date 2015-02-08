$(document).ready(function(){
	$.getJSON('get_list',function(data) {
				list_json(data);
	});
});
function get_search_results(){
	query_string = document.getElementById("q").value;
	$.getJSON('search?q='+query_string,function(data) {
			if(data.length > 0)
			{
				  var htmlStr = "<table><tr><th>Name</th><th>Price</th><th>Category</th></tr>";
			      $.each(data, function(key, val) {
					htmlStr = htmlStr + "<tr><td>"+val.fields.name+"</td><td>"+val.fields.price+"</td><td>"+val.fields.category+"</td><tr>";
					});
			      htmlStr = htmlStr + "</table>";
			      $("#search_results").html(htmlStr);
			}
			else
				$("#search_results").html("<br/>Not Results Found...");
		});
}
function list_json(data)
{
	if(data.length > 0)
	{
		  var htmlStr = "<table><tr><th>Name</th><th>Price</th><th>Category</th></tr>";
	      $.each(data, function(key, val) {
			htmlStr = htmlStr + "<tr><td>"+val.name+"</td><td>"+val.price+"</td><td>"+val.category+"</td><td><a href='#' onclick='delete_product("+val.id+")'>delete</a></td><td><a href='#' onclick='show_update_product("+val.id+")'>update</a></td></tr>";
			});
	      htmlStr = htmlStr + "</table>";
	      $("#list_results").html(htmlStr);
	}
	else
		$("#list_results").html("<br/>Not Products Found...");
}
function delete_product(prod_id)
{
	$.getJSON('delete/'+prod_id,function(data) {
		$.getJSON('get_list',function(data) {
				list_json(data);
		});
	});
}
function show_update_product(prod_id){
$.getJSON('read/'+prod_id,function(data) {
		
		$('#id').val(data.id);
		$('#name').val(data.name);
		$('#price').val(data.price);
		$('#category').val(data.category);
		$('#update_div').show();
});
}
function update_product(){
data = { id : $("#id").val(), name: $("#name").val(), price: $("#price").val(), category: $("#category").val(), csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() }
$.post("/update",
        data,
        function(data,status){
            $.getJSON('get_list',function(data) {
				list_json(data);
		}); 
        });
}
