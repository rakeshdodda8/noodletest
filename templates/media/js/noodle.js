var home = angular.module('App', []);
           
          home.config(function($interpolateProvider) {
            $interpolateProvider.startSymbol('{//');
            $interpolateProvider.endSymbol('//}');
          });	
		
		home.controller("productDetails", function ($scope, $http){
			$scope.list_all_products = function(){
				$http.get('get_list', {}).success(function (data) {
				  $scope.products = data;
				}).error(function (data) {
				});
			}

			$scope.list_all_products();

			$scope.delete_product = function(prod_id){
		       $http.get('delete/'+prod_id, {}).success(function (data) {
		        	$scope.list_all_products();
		        }).error(function (data) {});
			}

			$scope.status = false;
			$scope.show_update_product = function(prod_id){
			$scope.status = true;
				$http.get('read/'+prod_id, {}).success(function (data) {
					$scope.id = data.id;
					$scope.name = data.name;
					$scope.price = data.price;
					$scope.category = data.category;
				}).error(function (data) {});
			}

			$scope.update_product = function(){
				data = { 'id' : $scope.id, 'name': $scope.name, 'price': $scope.price, 'category': $scope.category}
			 	$http.post('/update', data).success(function (data) {
				    $scope.list_all_products();
				    $scope.status = false;
			    }).error(function (data) {
			        });
			}

			$scope.search_status = false;
			$scope.get_search_results = function(){
				query_string = $scope.q;
				$http.get('search?q='+query_string, {}).success(function (data) {
				if(data.length > 0)
				{
					$scope.search_status = true;
					$scope.search_result = false;
					$scope.search_results = data;
				}
				else
				{
					$scope.search_status = false;
					$scope.search_result = true;
				}
				}).error(function (data) {});
			}
	});