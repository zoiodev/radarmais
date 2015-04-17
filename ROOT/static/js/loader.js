function loader(btn){
	var txt = btn.html();
	var tamBtn = btn.css('width');
			
	btn.addClass('hide');
	btn.after('<img src="/static/img/admin/loader.gif" id="img_loader""> ');
	btn.parent().width(tamBtn);
	btn.parent().attr("disabled",true);	
}
function remove_loader(btn){
	$('#img_loader').remove();
	btn.removeClass('hide');
	btn.parent().removeAttr("disabled");	
}
function loader_submit(btn){
	var txt = btn.html();
	var tamBtn = btn.css('width');
			
	btn.addClass('hide');
	btn.after('<a class="button expand secondary tiny radius save" id="img_loader"><img src="/static/img/admin/loader.gif" "> </a>');
	btn.parent().attr("disabled",true);	
}
function loader_esqueci_minha_senha(btn){
	var txt = btn.html();
	var tamBtn = btn.outerWidth();
	// console.log(tamBtn);
			
	btn.addClass('hide');
	btn.after('<a class="button expand enviar-email" style="width:'+ (tamBtn) +'px;" id="img_loader"><img src="/static/img/admin/loader.gif" "> </a>');
	btn.parent().attr("disabled",true);	
}
function remove_loader_submit(btn){
	$('#img_loader').remove();

	btn.removeClass('hide');
	btn.parent().removeAttr("disabled");	
		
}