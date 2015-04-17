$( document ).ready(function() {
	$(".clienteEdit").click(function() {
		
		clienteId = $('#cliente_id').val();
		token = $('#token').val();

		var localAction = $('#url').val();
		
		$.ajax({
			type: 'POST',
			url: localAction,
			data: $( "#editCliente" ).serialize(),
			// SUCESSO
			success: function(data){
				console.log(data);
				console.log('xgo');
				if(data == 'true'){
					window.location = $('#url-listagem').val(); 
				}else{
					alert('Erro ao Editar usuario');
				}
			},
			// ERRO
			error: function (data) {
				// Se deu algum erro, mostro no log do console
				// console.log(data);
				console.log('deu erro');
			}
		});
	});




	$( "a#deleteCliente" ).click(function() {
		var clienteId = $(this).parent().attr('id');
		var localAction = $(this).attr('rel');
		
		var txt = 'Deseja excluir este Cliente?';

		if(confirm(txt) === true){
			console.log(localAction);
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

