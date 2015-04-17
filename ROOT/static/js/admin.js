function printarAlertaAdmin(frase, tipo, onde) {
	
	if ($('div[data-alert]').length) {
		$('div[data-alert]').slideUp('fast');
		setTimeout(function(){ 
			$('div[data-alert]').remove();

			var html = '<div data-alert class="alert-box '+ tipo +' round" style="display:none;">'+ frase +'<a href="javascript:void(0)" onClick="fecharAlertaAdmin();" class="close">&times;</a></div>';

			$(onde).before(html);
			$('div[data-alert]').slideDown();
		}, 300);
		


	} else {
		var html = '<div data-alert class="alert-box '+ tipo +' round" style="display:none;">'+ frase +'<a href="javascript:void(0)" onClick="fecharAlertaAdmin();" class="close">&times;</a></div>';

		$(onde).before(html);
		$('div[data-alert]').slideDown();

	}

	setTimeout(function(){
		fecharAlertaAdmin();
	}, 10000);
	
}

function fecharAlertaAdmin() {
	$('div[data-alert]').slideUp();
	setTimeout(function(){ 
		$('div[data-alert]').remove();
	}, 1000);
}