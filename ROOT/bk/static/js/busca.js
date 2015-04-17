var app = angular.module('app', ['ngSanitize']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

// Controller principal, já lê as empresas
app.controller('BuscaCtrl', function($scope, $http){

	$scope.pesquisar = function(pesquisa){

		// Se a pesquisa for vazia
		if (pesquisa == ""){

			// Retira o autocomplete
			$scope.completing = false;

			console.log('pesquisa vazia')
		}else{
			
			var urlBusca = webrootBusca.replace('0/', '');

			// // Pesquisa no banco via AJAX
			$http.get(urlBusca+pesquisa, { "buscar" : pesquisa}).
			success(function(data) {
				// Coloca o autocomplemento
				$scope.completing = true;	

				// JSON retornado do banco
				$scope.retornos = data.noticias;     
				
			})
			.
			error(function(data) {
				// Se deu algum erro, mostro no log do console
				console.log(data);
				console.log("Ocorreu um erro no banco de dados ao trazer auto-ajuda da home");
			});		



		}
	};
});