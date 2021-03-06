$( document ).ready(function() {
	// >>> inteligencia dos selects
	var status = $('#id_status');
	var qtdDias = $('#id_dias_liberado');
	qtdDias.prop('disabled', 'disabled');

	if(status.val() == 2){
		qtdDias.removeAttr("disabled");
	}

	status.change(function() {
		if(status.val() == 2){
			qtdDias.val(1);
			// $('#id_dias_liberado option:eq(1)').prop('selected', true);
			qtdDias.removeAttr("disabled");
		}else{
			qtdDias.val(0);
			// $('#id_dias_liberado option:eq(0)').prop('selected', true);
			qtdDias.prop('disabled', 'disabled');
		}
	});

	qtdDias.change(function() {
		if(qtdDias.val() == 0){
			status.val(1);
			// $('#id_status option:eq(1)').prop('selected', true);
			qtdDias.prop('disabled', 'disabled');
		}

	});
	// <<< inteligencia dos selects




	$(".usuarioEdit").click(function() {
		
		usuarioId = $('#usuario_id').val();
		token = $('#token').val();
		var localAction = $('#url').val();
		
		loader($(this));

		$.ajax({
			type: 'POST',
			url: localAction,
			headers: { 'Content-Type' : 'application/x-www-form-urlencoded', 'X-CSRFToken': token},
			data: $( "#editUsuario" ).serialize(),
			// SUCESSO
			success: function(data){
				if(data == 'true'){
					alert('Usuário alterado com sucesso.');
					window.location = $('#url-listagem').val(); 
				}if(data == 'email-ja-existe'){
					printarAlertaAdmin('Este e-mail já foi cadastrado, tente novamente.', 'alert', $('form#editUsuario'));
					remove_loader($(".usuarioEdit"));
				}if(data == 'false'){					
					console.log('Erro ao Editar usuario');
				}

				remove_loader($('.usuarioEdit'));
			},
			// ERRO
			error: function (data) {
				// Se deu algum erro, mostro no log do console
				console.log(data);
				console.log('deu erro');
			}
		});
	});




	$( "a.deleteUsuario" ).click(function() {
		deletarUsuarios($(this));
		// console.log('metodo');
		// var usuarioId = $(this).parent().attr('id');
		// var localAction = $(this).attr('rel');
		
		// var txt = 'Deseja excluir este usuario?';

		// if(confirm(txt) === true){
		// 	console.log('retorno true');
		// 	$.get( localAction, function( data ) {
		// 		if (data == 'true') {
		// 			location.reload();
		// 		}else{
		// 			alert('erro ao deletar usuario.');
		// 		}
		// 	});
		// }
		
	});

});


function deletarUsuarios(elemento) {
	var usuarioId = $(elemento).parent().attr('id');
	var localAction = $(elemento).attr('rel');
	// console.log(localAction);
	
	var txt = 'Deseja excluir este usuario?';

	if(confirm(txt) === true){
		// console.log('retorno true');
		$.get( localAction, function( data ) {
			if (data == 'true') {
				location.reload();
			}else{
				alert('erro ao deletar usuario.');
			}
		});
	}
	

}

