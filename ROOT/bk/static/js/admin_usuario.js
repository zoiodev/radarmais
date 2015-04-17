$( document ).ready(function() {
	// $( "a.cadastroUsuario" ).click(function() {
	// 	var localAction = webroot+'adicionar-usuario/add/';
	// 	$.ajax({
	// 		type: 'POST',
	// 		url: localAction,
	// 		data: $( "#addUsuario" ).serialize(),
	// 		// SUCESSO
	// 		success: function(data){
	// 			if(data == 'email-ja-existente'){
	// 				alert('usuario ja existe');
	// 			}else{
	// 				if(data == 'true'){
	// 					alert('usuario salvo com sucesso.');
	// 					// window.location = "../../../../lista-de-usuarios/";
	// 				}else{
	// 					alert('erro ao salvar ususario');
	// 				}
	// 			}
				
	// 		},
	// 		// ERRO
	// 		error: function (data) {
	// 			// Se deu algum erro, mostro no log do console
	// 			console.log(data);
	// 		}
	// 	});
	// });


	$(".usuarioEdit").click(function() {
		
		usuarioId = $('#usuario_id').val();
		token = $('#token').val();
		var localAction = $('#url').val();
		console.log(localAction);
		$.ajax({
			type: 'POST',
			url: localAction,
			headers: { 'Content-Type' : 'application/x-www-form-urlencoded', 'X-CSRFToken': token},
			data: $( "#editUsuario" ).serialize(),
			// SUCESSO
			success: function(data){
				console.log(data);
				if(data == 'true'){
					window.location = $('#url-listagem').val(); 
				}else{
					alert('Erro ao Editar usuario');
				}
			},
			// ERRO
			error: function (data) {
				// Se deu algum erro, mostro no log do console
				console.log(data);
				console.log('deu erro');
			}
		});
	});




	$( "a#deleteUsuario" ).click(function() {
		var usuarioId = $(this).parent().attr('id');
		var localAction = $(this).attr('rel');
		
		var txt = 'Deseja excluir este usuario?';

		if(confirm(txt) === true){
			$.get( localAction, function( data ) {
				if (data == 'true') {
					location.reload();
				}else{
					alert('erro ao deletar usuario.');
				}
			});
		}
		
	});





});

