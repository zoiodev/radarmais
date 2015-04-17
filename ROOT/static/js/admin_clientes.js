$( document ).ready(function() {
	$( "a.deleteCliente" ).click(function() {
		var clienteId = $(this).parent().attr('id');
		var localAction = $(this).attr('rel');
		
		var txt = 'Deseja excluir este Cliente?';

		// console.log(localAction);

		if(confirm(txt) === true){
			// console.log(localAction);
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

