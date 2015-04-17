
///////  EDITOR ///////////////
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
var editor = new MediumEditor('.editable', {
	anchorTarget: true,
	buttons: ['bold', 'italic', 'underline', 'strikethrough', 'quote', 'anchor', 'justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull', 'superscript', 'subscript', 'orderedlist', 'unorderedlist', 'outdent', 'indent', 'header1', 'header2'],
	buttonLabels: 'fontawesome',
	firstHeader: 'h2',
	secondHeader: 'h3',
	// staticToolbar: true,
	// stickyToolbar: false,
	cleanPastedHTML: true
});

var editorNoReturn = new MediumEditor('.editableNoReturn', {
	anchorTarget: true,
	buttons: ['bold', 'italic', 'underline', 'strikethrough', 'quote', 'anchor', 'justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull', 'superscript', 'subscript', 'orderedlist', 'unorderedlist', 'outdent', 'indent', 'header1', 'header2'],
	buttonLabels: 'fontawesome',
	firstHeader: 'h2',
	secondHeader: 'h3',
	disableReturn: true,
	// staticToolbar: true,
	// stickyToolbar: false,
	cleanPastedHTML: true
});
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////


$(document).ready(function(){

	//// FORMULÁRIO
	/////////////////////////////////////////
	$("form#formnoticia input[type=submit]").click(function() {
		$('form#formnoticia input[name="destino"]').val($(this).attr('id'));
		// console.log($('form#formnoticia input[name="destino"]').val());
		// fecharAlerta();
	});
	$('form#formnoticia').submit(function(){
		// console.log('submit');
		// debugger;

		////===> PASSANDO VALORES DOS ELEMENTOS DIV PARA O FORMULÁRIO
		$('[data-form-input]').each(function(index, value){
			// debugger;
			nome_do_campo 			= $(value).attr('data-form-input');
			place_holder_do_campo 	= $(value).attr('data-placeholder');
			valor_do_campo			= $(value).html();

			$('form#formnoticia').find('input[name="'+ nome_do_campo +'"]').val(valor_do_campo).attr('placeholder', place_holder_do_campo);

		});



		////===> VARIÁVEIS
		var categoria 		= $(this).find('input[name="categoria"]');
		var categoria_value	= $(categoria).val();

		var data 			= $(this).find('input[name="data"]');
		var data_value		= $(data).val();
		
		var titulo 			= $(this).find('input[name="titulo"]');
		var titulo_value	= $(titulo).val();
		
		var chamada 		= $(this).find('input[name="chamada"]');
		var chamada_value	= $(chamada).val();
		
		var texto 			= $(this).find('input[name="texto"]');
		var texto_value		= $(texto).val();

		var fonte 			= $(this).find('input[name="fonte"]');
		var fonte_value		= $(fonte).val();
		
		var clientes 		= $(this).find('input[name="cliente[]"]:checked');
		var clientes_value	= $(clientes).serialize()
		// console.log(clientes_value);
		// debugger;

		var data_publicacao = $(this).find('input[name="data_publicacao"]');
		var data_publicacao_value	= $(data_publicacao).val();
		
		var ativo 			= $(this).find('input[name="ativo"]');
		var ativo_value		= "0";
		if (ativo.is(':checked')) {
			ativo_value = "1";
		}

		var status 			= $(this).find('select[name="status"]');
		var status_value	= $(status).find('select[name="status"] option:selected').val();

		var destino 		= $(this).find('input[name="destino"]');
		var destino_value	= $(destino).val();

		
		////===> PASSAR VALORES DO EDITOR PARA OS CAMPOS
		/*
		ERRO DE REDUNDÂNCIA:  esta ação foi melhorada e colocada no início da função

		$(data).val($('#dataDeCadastro span').html());
		$(titulo).val($('#tituloDaMateria').html());
		$(chamada).val($('#chamadaDaMateria').html());
		$(texto).val($('#textoDaMateria').html());
		$(fonte).val($('#fonteDaMateria').html());
		*/


		// console.log("categoria_value: "+ categoria_value);
		// console.log("data: "+ $(data).val());
		// console.log("titulo: "+ $(titulo).val());
		// console.log("titulo_value: "+ titulo_value);
		// console.log("chamada: "+ $(chamada).val());
		// console.log("texto: "+ $(texto).val());
		// console.log("fonte: "+ $(fonte).val());
		// console.log("clientes: "+ clientes_value);
		// console.log("data_publicacao: "+ $(data_publicacao).val());
		// console.log("ativo: "+ ativo_value);
		// console.log("status: "+ $(status).val());
		// console.log("destino: "+ $(destino).val());
		// console.log("destino_value: "+ destino_value);


		////===> VALIDAÇÃO
		// debugger;
		/*
		TITULO */
		if (titulo_value) {
			if (titulo_value.replace(' ', '') == '') {
				avisarErro('Favor inserir um título');
				return false;
			}
			
			if (titulo_value.trim() == $(titulo).attr('placeholder').trim()) {
				avisarErro('Favor inserir um título');
				return false;
			}
		} else {
			avisarErro('Favor inserir um título');
			return false;
		}

		/*
		CHAMADA
		OBS.: não tem validação, apenas limpeza do campo */
		if (chamada_value) {
			if (chamada_value.trim() == $(chamada).attr('placeholder').trim()) {
				$(chamada).val('');
			}
		}

		/*
		TEXTO */
		if (texto_value){
			if (texto_value.replace(' ', '') == '') {
				avisarErro('Favor inserir um texto');
				return false;
			}

			if (texto_value.trim() == $(texto).attr('placeholder').trim()) {
				avisarErro('Favor inserir um texto');
				return false;
			}
		} else {
			avisarErro('Favor inserir um texto');
			return false;
		}

		/*
		CLIENTES */
		if (clientes_value) {
			if (clientes_value == '') {
				avisarErro('Você precisa escolher os clientes que podem visualizar esta notícia');
				return false;
			} else {
				var clientes_value = new Array();
				$.each($(clientes), function() {
					clientes_value.push($(this).val());
				});
				clientes_value = clientes_value.toString();
				$(this).find('input[name="clientearray"]').val(clientes_value);
				// console.log(clientes_value);
			}
		} else {
			avisarErro('Você precisa escolher os clientes que podem visualizar esta notícia');
			return false;
		}

		/*
		DATA DE PUBLICAÇÃO
		OBS.: não tem validação, apenas limpeza do campo */
		// debugger;
		if (data_publicacao_value) {
			if (data_publicacao_value == '__/__/____ __:__') {
				$(data_publicacao).val('');
			} else {
				var dataPub = $(data_publicacao).val();

				var dataPubXP = dataPub.split(' ');
				var dataPubDat = dataPubXP[0];
				var dataPubHou = dataPubXP[1];

				var dateXP = dataPubDat.split('/');
				var dia = dateXP[0];
				var mes = dateXP[1];
				var ano = dateXP[2];

				var dataCompleta = ano+'-'+mes+'-'+dia+' '+ dataPubHou;

				$(this).find('input[name="data_de_publicacao"]').val(dataCompleta)
				// console.log(dataCompleta);
				// debugger;

			}
		}




		// console.log($(this).serialize());


		/*
		.
		.
		.
		.
		.
		.
		.
		.
		.
		.
		REALIZA O AJAX PARA CADASTRAR NOTÍCIA
		*/
		var noticia_id = "";
		noticia_id = 2;


		// console.log($( "#formnoticia" ).serialize());


		var localAction = webroot+'admin/noticias/add/post/';
		
		$.ajax({
			type: 'POST',
			url: localAction,
			data: $( "#formnoticia" ).serialize(),
			headers: { 'X-CSRFToken': $('#token').val()},
                
			// data: $( "#formnoticia" ).serialize(),
			// headers: { 'X-CSRFToken': $('#token').val()},
			// SUCESSO
			success: function(data){
				console.log(data);


				///=> REDIRECIONA
				var destino_url = "";

				if (destino_value == 1) {
					destino_url = "listagem";
				}
				if (destino_value == 2) {
					destino_url = webroot+"admin/noticias/add";
				}
				if (destino_value == 3) {
					destino_url = "edit/"+ noticia_id;
				}



				if (destino_url != "") {
					// window.location = destino_url; 
				}


				
			},
			// ERRO
			error: function (data) {
				// Se deu algum erro, mostro no log do console
				console.log(data.responseText);
			}
		});

		/*
		.............................................
		*/






	});
	/////////////////////////////////////////



	//// HELP
	/////////////////////////////////////////
	$('#infoForm').click(function(){
		$(document).foundation('joyride', 'start');
	});
	/////////////////////////////////////////




	

	
	//// CHECK BOX DOS CLIENTES
	/////////////////////////////////////////

	$('#todos').change(function(){
		if ($(this).is(":checked")) {
			$('.clientes-list input[type="checkbox"]').prop('checked', true);

		} else {
			$('.clientes-list input[type="checkbox"]').prop('checked', false);
		}
	});

	$('.clientes-list input[type="checkbox"]').change(function(){
		if (!$(this).is(":checked")) {
			if ($("#todos").prop('checked', true)) {
				$("#todos").prop('checked', false);
			}
		}
	});
	/////////////////////////////////////////







	//// CALENDÁRIO PERSONALIZADO
	/////////////////////////////////////////
	$('.datetimepicker').datetimepicker({
		lang:'pt-BR',
		i18n:{
			de:{
				months:[
					'Janeiro','Fevereiro','Março','Abril',
					'Maio','Junho','Julho','Agosto',
					'Setembro','Outubro','Novembro','Dezembro',
				],
				dayOfWeek:[
					"Dom", "Seg", "Ter", "Qua", 
					"Qui", "Sex", "Sab",
				]
			}
		},
		timepicker:true,
		format:'d/m/Y H:i',
		mask:true,
		closeOnDateSelect: true
	});

	$('.datetimepickerNoTime').datetimepicker({
		lang:'pt-BR',
		i18n:{
			de:{
				months:[
					'Janeiro','Fevereiro','Março','Abril',
					'Maio','Junho','Julho','Agosto',
					'Setembro','Outubro','Novembro','Dezembro',
				],
				dayOfWeek:[
					"Dom", "Seg", "Ter", "Qua", 
					"Qui", "Sex", "Sab",
				]
			}
		},
		onSelectDate:function(ct,$i){
			$('.datetimepickerNoTime').html(ct.dateFormat('d.m.Y'))
		},
		timepicker:false,
		format:'d.m.Y',
		mask:true,
		closeOnDateSelect: true
	});
	/////////////////////////////////////////
});



/// FUNCÕES DE APOIO PARA A VALIDAÇÃO
/////////////////////////////////////////
function avisarErro(frase) {
	
	if ($('div[data-alert]').length) {
		$('div[data-alert]').slideUp('fast');
		setTimeout(function(){ 
			$('div[data-alert]').remove();

			var html = '<div data-alert class="alert-box alert round" style="display:none;">'+ frase +'<a href="javascript:void(0)" onClick="fecharAlerta();" class="close">&times;</a></div>';

			$('#acoesParaSalvar').before(html);
			$('div[data-alert]').slideDown();
		}, 300);
		


	} else {
		var html = '<div data-alert class="alert-box alert round" style="display:none;">'+ frase +'<a href="javascript:void(0)" onClick="fecharAlerta();" class="close">&times;</a></div>';

		$('#acoesParaSalvar').before(html);
		$('div[data-alert]').slideDown();

	}
	
}
function fecharAlerta() {
	$('div[data-alert]').slideUp();
	setTimeout(function(){ 
		$('div[data-alert]').remove();
	}, 1000);
}
function zerarCampo(element) {
	// $(element).val('');
	// $(element).reset();
}
/////////////////////////////////////////









