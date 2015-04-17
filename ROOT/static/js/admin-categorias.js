var app = angular.module('app', []);
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

// Controller principal, já lê as empresas
app.controller('CategoriasCtrl', function($scope, $http){

	var locationAction = webroot+'admin/noticias/lista-de-categorias/post';
	
	// Pesquisa no banco via AJAX
	$http.get(locationAction).
	success(function(data) {

		// console.log(data);

		// Coloca o autocomplemento
		$scope.completing = true;	

		// JSON retornado do banco
		$scope.retornos = data.categorias;

		// console.log(data);

		$scope.ativarCategoria = function(categoriaId) {

			// console.log(nomeRepresa);
			angular.forEach(data.categorias, function(item){   
				// console.log(item);
				if(item.id == categoriaId) {
					$scope.categoriaId = item.id;
					$scope.categoriaNome = item.nome;
					$scope.categoriaLogo = item.logo;
					$scope.categoriaBg = item.bg;
					$scope.categoriaSlug = item.slug;
					return false;
				}
			});
		}

		if ($scope.categoriabanco) {
			$scope.ativarCategoria($scope.categoriabanco);
		} else {
			$scope.categoriaId 		= data.categorias[0].id;
			$scope.categoriaNome 	= data.categorias[0].nome;
			$scope.categoriaLogo 	= data.categorias[0].logo;
			$scope.categoriaBg 		= data.categorias[0].bg;
			$scope.categoriaSlug	= data.categorias[0].slug;
		}

	})
	.
	error(function(data) {
		// Se deu algum erro, mostro no log do console
		console.log("Ocorreu um erro no banco de dados ao trazer auto-ajuda da home");
	});		
});