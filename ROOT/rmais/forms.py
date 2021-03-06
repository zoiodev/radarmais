# -*- coding: utf-8 -*-
from django import forms
from ROOT.rmais.models import Empresa, Cidade, Usuario, Noticia, Categoria, Estado
from django.forms.widgets import CheckboxSelectMultiple 

# login e senha
class  UsuarioForm(forms.Form):
	usuario = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Login', 'type': 'email'}))
	senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))


class SenhaForm(forms.Form):
	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'e-mail de cadastro', 'class': 'email_enviar_senha'}))




class AddUsuarioForm(forms.ModelForm):

	class Meta:
		model = Usuario
		fields = '__all__'

	empresa = forms.ModelChoiceField(
									queryset=Empresa.objects.all(), 
									widget=forms.Select(attrs={'id':'cliente', 'name': 'cliente'}),
									# widget=forms.Select(attrs={'id':'cliente', 'name': 'cliente', 'ng-model': 'formData.cliente_id'}),
									required=False
									)
	types = (
			    (0, 'usuário'),
			    (1, 'máquina'),
			)
	tipo_de_usuario = forms.ChoiceField(
									widget = forms.Select(), 
     								choices = (types), 
     								required = False,
     								)

	nome_do_usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome Completo', 'id': 'right-label'}), required=False)

	cidade_de_preferencia = forms.ModelChoiceField(label="Cidade de Preferencia", 
													empty_label=" -- Selecione a Cidade --", 
													queryset=Cidade.objects.all(), 
													widget=forms.Select(attrs={'class':'select-cidades'}),
													required=False
													)

	email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'E-mail'}), required=False)

	options = (
				(0 , 'Inativo'),
				(1 , 'Ativo'),
				(2 , 'Temporario'),
			)
	status = forms.ChoiceField(widget = forms.Select(attrs={'ng-init':"formData.status='0'"}), 
 								choices = (options), 
 								required = False,
         						)
	
	temp_day = (
        (0, 'Ilimitada'),
        (1, '7 Dias'),
        (2, '15 Dias'),
        (3, '30 Dias'),
        (4, '90 Dias'),
    )
	dias_liberado = forms.ChoiceField(
									widget = forms.Select(attrs={'ng-init':"formData.dias_liberado='0'"}), 
     								choices = (temp_day), 
     								required = False,
     								)


class UsuarioFiltroForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = '__all__'

	# >>> filtro pra busca
	empresaFilter = forms.ModelChoiceField(empty_label='todos os clientes',
									queryset=Empresa.objects.all(), 
									widget=forms.Select(attrs={'name': 'cliente_id', 'id': 'cliente_id', 'ng-model': 'formData.cliente_id'}),
									required=False
									)

	campobusca = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'palavra chave', 'id': 'campobusca', 'ng-model': 'formData.campobusca', 'class': 'ng-pristine ng-valid'}), required=False)
	# >>> filtro pra busca




class NoticiaForm(forms.ModelForm):

	class Meta:
		model = Noticia
		field = ("empresa")
	

	data_criacao= forms.CharField(required=False)
	embed_video= forms.CharField(required=False)
	imagem_principal= forms.CharField(required=False)
	fonte 		= forms.CharField(required=False)
	link_fonte	= forms.CharField(required=False)
	slug	= forms.CharField(required=False)
	cliente = forms.ModelChoiceField(
										queryset=Empresa.objects.all(), 
										widget=forms.CheckboxSelectMultiple(attrs={'id':'cliente', 'name': 'cliente'}),
										required=False,
									)
	categoria   			= forms.CharField(widget=forms.TextInput(attrs={'id': 'categoria', 'name': 'categoria', 'type': 'hidden'}), required=False)
	data 					= forms.CharField(widget=forms.TextInput(attrs={'id': 'data', 'name': 'data', 'type': 'hidden'}), required=False)
	data_da_noticia 		= forms.CharField(widget=forms.TextInput(attrs={'id': 'data_da_noticia', 'name': 'data_da_noticia', 'type': 'hidden'}), required=False)
	titulo 					= forms.CharField(widget=forms.TextInput(attrs={'id': 'titulo', 'name': 'titulo', 'type': 'hidden'}), required=False)
	chamada 				= forms.CharField(widget=forms.TextInput(attrs={'id': 'chamada', 'name': 'chamada', 'type': 'hidden'}), required=False)
	texto 					= forms.CharField(widget=forms.TextInput(attrs={'id': 'texto', 'name': 'texto', 'type': 'hidden'}), required=False)
	fonte 					= forms.CharField(widget=forms.TextInput(attrs={'id': 'fonte', 'name': 'fonte', 'type': 'hidden'}), required=False)
	# destino 				= forms.CharField(widget=forms.TextInput(attrs={'id': 'destino', 'name': 'destino', 'type': 'hidden'}), required=False)
	ativo 					= forms.CharField(widget=forms.TextInput(attrs={'id': 'ativo', 'name': 'ativo', 'type': 'checkbox', 'checked': 'checked', 'value': 1}), required=False)
	data_de_publicacao 		=  forms.CharField(widget=forms.TextInput(attrs={'id': 'data_publicacao', 'name': 'data_publicacao', 'class': 'datetimepicker text-center'}), required=False)
	
	options = (
	        (0, '- sem status -'),
	        (1, 'Alarmante'),
	        (2, 'Normal'),
	        (3, 'Atenção'),
	    )
	status = forms.ChoiceField(widget = forms.Select(), 
	 								choices = (options), 
	 								required = False
	 							)



class EmpresasForm(forms.ModelForm):

	class Meta:
		model = Empresa
		fields = '__all__'

	nome_da_empresa 	= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome da empresa', 'id': 'right-label'}), required=False)
	nome_do_contato 	= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome do Contato da empresa', 'id': 'right-label'}), required=False)
	email_do_contato 	= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'E-mail de Contato da empresa', 'id': 'right-label'}), required=False)
	endereco	 		= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Endereço da Empresa', 'id': 'right-label'}), required=False)
	ativo 				= forms.CharField(widget=forms.TextInput(attrs={'id': 'ativo', 'name': 'ativo', 'type': 'checkbox', 'checked': 'checked', 'value': 1}), required=False)
	