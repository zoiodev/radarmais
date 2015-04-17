var app = angular.module('app', ['ngSanitize']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

// Controller principal, já lê as empresas
app.controller('BuscaCtrl', function($scope, $http){

	$scope.pesquisar = function(pesquisa, token){

		// Se a pesquisa for vazia
		if (pesquisa == ""){

			// Retira o autocomplete
			$scope.completing = false;

			// console.log('pesquisa vazia')
		}else{
			

			if (pesquisa.length >= 3) {

				var urlBusca = webrootBusca.replace('0/', '');

				// console.log(urlBusca);

				// // Pesquisa no banco via AJAX
				// $http({
				// 		method: 'POST',
				// 		url: urlBusca,
				// 		headers: { 'Content-Type' : 'application/x-www-form-urlencoded', 'X-CSRFToken': token},
				// 		data: $.param({ "buscar" : pesquisa})
				// 	}).
				// 	success(function(data, status, headers, config) {
				// 		console.log(data);

				// 		// JSON retornado do banco
				// 		$scope.retornos = data.noticias;

				// 		// Coloca o autocomplemento
				// 		$scope.completing = true;	
						
				// 	})
				// 	.
				// 	error(function(data, status, headers, config) {
				// 		// Se deu algum erro, mostro no log do console
				// 		console.log(data);
				// 		console.log("Ocorreu um erro no banco de dados ao trazer auto-ajuda da home");
				// 	});	

				//+++> SYNC
				var xhr = new window.XMLHttpRequest();  
				xhr.open('POST', urlBusca, true);  
				xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
				xhr.onreadystatechange = function() {  
					if (xhr.readyState === 4) {
						if (xhr.status === 200) {
							// console.log('Success');
							// console.log(xhr.responseText);

							var data = xhr.responseText.replace(/(\r\n|\n|\r)/gm,"");
							// console.log("data: "+ data);
							var jsonResponse = JSON.parse(data);
							// console.log("jsonResponse: "+ jsonResponse);
							// console.log(jsonResponse["noticias"]);

							// var data = JSON.parse(xhr.responseText);
							// console.log(data)

							$scope.retornos = jsonResponse["noticias"];
							$scope.completing = true;	
						}
					}
				};
				xhr.send("buscar="+ pesquisa);

			}



		}
	};
});