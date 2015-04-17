# -*- coding: utf-8 -*-
import json
import os
from django.conf import settings # mail
from django.core.mail import send_mail
from datetime import date
import datetime
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, HttpResponse, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UsuarioForm, UsuarioFiltroForm, SenhaForm, AddUsuarioForm, NoticiaForm, EmpresasForm
from ROOT.rmais.models import Categoria, Noticia, Pagina, Usuario, Empresa, Leitura
from functools import reduce
from operator import __or__ as OR
from django.views.decorators.csrf import csrf_exempt

## EMAIL ##
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from ROOT.rmais.sort_headers import SortHeaders


import random
import string

from django.db.models import Q

from django.db import connection

# envio de email
# from django.core.mail import EmailMessage



# front
def login(request, logError=None):
	form = UsuarioForm(request.POST)
	formSenha = SenhaForm(request.POST or None)

	logError = ''

	if request.method == 'POST':
		if form.is_valid:
			login = request.POST.get('usuario')
			senha = request.POST.get('senha')

			usuario = Usuario.objects.filter(email=login).first()
			
				

			if usuario:
				if usuario.senha != senha:
					request.session['logado_error'] = 'log-passInvalid'
					logError = request.session['logado_error']

					return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha, 'logError': logError})

				else:
					if usuario.status == 0:
						request.session['logado_error'] = 'log-inativo'
						logError = request.session['logado_error']

						return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha, 'logError': logError})

					elif usuario.status == 2:
						datetime_agora 	= datetime.datetime.now().replace(microsecond=0)
						tempo_acesso 	= usuario.dias_liberado
						data_criacao 	= usuario.data_criacao
						data_expiracao 	= data_criacao

						if tempo_acesso == 1:
							data_expiracao = data_criacao + datetime.timedelta(days = 7)

						elif tempo_acesso == 2:
							data_expiracao = data_criacao + datetime.timedelta(days = 15)

						elif tempo_acesso == 3:
							data_expiracao = data_criacao + datetime.timedelta(days = 30)

						elif tempo_acesso == 4:
							data_expiracao = data_criacao + datetime.timedelta(days = 90)
						

						# print "datetime_agora: %s" % datetime_agora
						# print "data_expiracao: %s" % data_expiracao
						# print datetime_agora <= data_expiracao
						print 'data de agora %s'%datetime_agora
						print 'data de expiracao %s' %data_expiracao
						print 'data de criacao: %s'%data_criacao

						if datetime_agora <= data_expiracao:
							request.session['logado'] = 1
							request.session['usuario_id'] = usuario.id
							request.session['empresa_id'] = usuario.empresa.id
							request.session['tipo_usuario'] = usuario.empresa.tipo_de_usuario
							request.session['data_expiracao'] = json.dumps(data_expiracao, default=date_handler)# serialize date

							if usuario.primeiro_acesso:
								usuario.primeiro_acesso = 0
								usuario.save()
								return redirect("configuracoes")
							else:
								return redirect("home")

						else:
							request.session['logado_error'] = 'log-expirou'
							logError = request.session['logado_error']
							return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha, 'logError': logError, 'data_expiracao': data_expiracao})
							# return HttpResponseRedirect("")

					


					else:
						request.session['logado'] = 1
						request.session['usuario_id'] = usuario.id
						request.session['empresa_id'] = usuario.empresa.id
						request.session['tipo_usuario'] = usuario.empresa.tipo_de_usuario

						if usuario.primeiro_acesso:
							usuario.primeiro_acesso = 0
							usuario.save()
							return redirect("configuracoes")
						else:
							return redirect("home")
							
			else:
				request.session['logado_error'] = 'log-error'
				logError = request.session['logado_error']
				
				return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha, 'logError': logError})
				

	return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha})


# >>> serialize date
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
# <<< serialize date


def email(request):
	formSenha = SenhaForm(request.POST)

	if formSenha.is_valid:
		email = request.GET['email']

		# print email
		usuario = Usuario.objects.filter(email=email).values('id', 'nome_do_usuario', 'email', 'senha').first()
		
		# print usuario['email']
		
		if usuario:
			# # teste
			assunto = '[Radar+] Dados de acesso'
			from_addr = settings.EMAIL_HOST_USER
			replay_to_addr = settings.EMAIL_REPLAY_TO
			usuarioEmail = [usuario['email']] 

			## HTML
			h = get_template('rmais/email/sua_senha.html')

			## TXT
			t = get_template('rmais/email/sua_senha.txt')

			c = Context({
				'nome': usuario['nome_do_usuario'],
				'login': usuario['email'],
				'senha': usuario['senha'],
			})

			html_content = h.render(c)
			text_content = t.render(c)

			# send_mail(assunto, t.render(c), from_addr, usuarioEmail, fail_silently=True)
			msg = EmailMultiAlternatives(assunto, text_content, from_addr, usuarioEmail, headers = {'Reply-To': replay_to_addr})
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			
			return HttpResponse('true')
			
		else:
			return HttpResponse('false')
			

def logout(request):
	if 'logado' in request.session:
		del request.session['logado']
		del request.session['usuario_id']
		del request.session['empresa_id']
		del request.session['tipo_usuario']

	if 'data_expiracao' in request.session:
		del request.session['data_expiracao']

	return redirect('login')

def home(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
		
		cursor = connection.cursor()
		

		query = '''
					Select * from (
							Select distinct
								Noticia.id,
								Categoria.nome_da_categoria,
								Categoria.id as categoria_id,
								Categoria.logo,
								Categoria.slug as categoria_slug,
								Categoria.ordem,
								Noticia.titulo,
								Noticia.slug as noticia_slug,
								Noticia.data_da_noticia,
								Noticia.status,
								(
									Select 
										(count(NoticiaT.id) - count(Leitura.id)) as total_nao_lidas
									from
										rmais_noticia as NoticiaT
										left join rmais_leitura as Leitura on (NoticiaT.id = Leitura.noticia_id and Leitura.usuario_id = %s)
										inner join rmais_noticia_empresa as NE on (NoticiaT.id = NE.noticia_id)
									where
										NoticiaT.categoria_id = Categoria.id
										AND NoticiaT.ativo = 1
										AND NoticiaT.delete = 0
										AND NE.empresa_id = %s
								) as total_nao_lidas
							From
								rmais_categoria as Categoria
								left join rmais_noticia as Noticia on (Noticia.categoria_id = Categoria.id)
								inner join rmais_noticia_empresa as NE on (Noticia.id = NE.noticia_id)

							Where
								Categoria.ativo = 1
								AND Categoria.delete = 0
								AND Noticia.ativo = 1
								AND Noticia.delete = 0
								AND Noticia.data_de_publicacao <= now()
								AND NE.empresa_id = %s

							Group by
								Categoria.nome_da_categoria,
								Noticia.titulo

							Order By
								Categoria.ordem,
								Noticia.data_de_publicacao DESC
						) as Teste
						Group By 
							nome_da_categoria

						Order by 
							ordem
			'''
													
		params = (request.session.get('usuario_id'), request.session.get('empresa_id'), request.session.get('empresa_id'))

		categoriaNoticia = Noticia.objects.raw(query, params)


		datetime_agora = datetime.datetime.now().replace(microsecond=0)
		
		pagina = Pagina.objects.filter(slug='home').order_by('-id').first()


		noticias_lidas = Noticia.objects.filter(leitura__usuario_id=request.session['usuario_id']).values_list('id', flat=True).distinct()
		total_lidas_por_categoria = Noticia.objects.filter(pk__in=noticias_lidas, ativo=1).values_list('categoria_id').annotate(total=Count('id'))


		return render(request, 'rmais/home.html', {'menu': menu, 'pagina': pagina, 'total_lidas_por_categoria': total_lidas_por_categoria, 'categoriaNoticia': categoriaNoticia})


def listagem(request, slug=None):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
		
		if request.session.get('tipo_usuario') == 1:
			categoria = Categoria.objects.filter(slug=slug).order_by('-id').first()
		else:
			categoria = Categoria.objects.filter(slug=slug, noticia__delete=0, noticia__empresa=request.session.get('empresa_id')).order_by('-id').first()
		

		if categoria:
			datetime_agora = datetime.datetime.now().replace(microsecond=0)

			
			noticia_list  = Noticia.objects.filter(categoria_id=categoria, ativo=1, delete=0, data_de_publicacao__lt=datetime_agora, empresa__id=request.session['empresa_id'])

			paginacao = Paginator(noticia_list, 5)# mostra apenas X noticias

			page = request.GET.get('page')
			try:
				noticias = paginacao.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				noticias = paginacao.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				noticias = paginacao.page(paginacao.num_pages)
			# <<< paginacao
			leituras = Noticia.objects.filter(leitura__usuario_id=request.session['usuario_id']).values_list('id', flat=True).distinct()
			
			context = {
						'noticias': noticias, 
						'categoria': categoria, 
						'menu': menu, 
						'leituras': leituras, 
						'total_pages_paginator': paginacao.num_pages
					}
			return render(request, 'rmais/listagem.html', context)
		else:
			return redirect('home')

@csrf_exempt
def noticia_listagem_paginacao_infinita_json(request, categoria_slug=None, pagina=None):
	if request.session.get('tipo_usuario') == 1:
		categoria = Categoria.objects.filter(slug=categoria_slug).order_by('-id').first()
	else:
		categoria = Categoria.objects.filter(slug=categoria_slug, noticia__delete=0, noticia__empresa=request.session.get('empresa_id')).order_by('-id').first()


	if categoria:
		datetime_agora = datetime.datetime.now().replace(microsecond=0)

		# >>> paginacao
		noticia_list  = Noticia.objects.filter(categoria_id=categoria, ativo=1, delete=0, data_de_publicacao__lt=datetime_agora, empresa__id=request.session['empresa_id'])

		paginacao = Paginator(noticia_list, 5)# mostra apenas X noticias

		page = pagina

		try:
			noticias = paginacao.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			noticias = paginacao.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			noticias = paginacao.page(paginacao.num_pages)
		# <<< paginacao

		print noticias
		leituras = Noticia.objects.filter(leitura__usuario_id=request.session['usuario_id']).values_list('id', flat=True).distinct()
		

		context = {
				'noticias': noticias, 
				'categoria': categoria,
				'leituras': leituras,
				'total_pages_paginator': paginacao.num_pages,
				'empresa': request.session['empresa_id']
				}
		return render(request, 'rmais/noticia_listagem_paginacao_infinita.json', context)
	else:
		return redirect('home')



def noticia(request, categoria=None, id=None, slug=None):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
		datetime_agora = datetime.datetime.now().replace(microsecond=0)

		# noticia  = Noticia.objects.filter(id=id, slug=slug, ativo=1, data_de_publicacao__lt=datetime_agora).order_by('-id').first()
		noticia  = Noticia.objects.filter(id=id, ativo=1, delete=0, data_de_publicacao__lt=datetime_agora).first()

		if not noticia:
			return redirect('listagem', categoria)
		

		# print "noticia: %s" % noticia
		# print "id: %s" % id
		# print "slug: %s" % slug
		# print "tipo_usuario: %s" % request.session.get('tipo_usuario')

		if request.session.get('tipo_usuario') == 1:
			categoria = Categoria.objects.filter(id=noticia.categoria.id)
		else:
			categoria = Categoria.objects.filter(id=noticia.categoria.id, noticia__empresa=request.session.get('empresa_id'))

		print categoria

		if categoria:
			if not noticia:
				return redirect('listagem', categoria)

			categoria = Categoria.objects.filter(id=noticia.categoria_id).order_by('-id').first()
			
			# gravando a leitura do usuário
			leitura = Leitura(noticia_id = noticia.id, usuario_id = request.session['usuario_id'])
			leitura.save()
			
			return render(request, 'rmais/noticia.html', {'noticia': noticia, 'categoria': categoria, 'menu': menu})
		else:
			return redirect('home')

def pagina(request, page=None):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
		pagina = Pagina.objects.filter(slug=page).order_by('-id').first()
		
		return render(request, 'rmais/pagina.html', {'pagina': pagina, 'menu': menu})

@csrf_exempt
def rbusca(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		# print request
		print 'xgo no metodo rbusca'

		buscar = request.POST.get('buscar')
		# print request
		# print buscar

		if buscar:
			resultBusca = Noticia.objects.filter(Q(titulo__icontains=buscar) | Q(chamada__icontains=buscar) | Q(texto__icontains=buscar), delete=0, ativo=1, empresa=request.session.get('empresa_id')).values('id', 'titulo', 'chamada', 'slug', 'categoria__slug')
			# print resultBusca

			if resultBusca:
				context = {'resultBusca': resultBusca}
				return render(request, 'rmais/rbusca.json', context)
			else:
				return render(request, 'rmais/rbusca.json')
				
		else:
			return render(request, 'rmais/rbusca.json')


@csrf_exempt
def rbusca_export(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		resultBusca = Noticia.objects.all().values('id', 'titulo', 'chamada', 'slug', 'texto', 'categoria__slug', 'empresa__id')

		noticias = []
		for noticia in resultBusca:

			noticias.append({
				'id', noticia['id'], 
				'titulo', removetags(noticia['titulo'], 'p b span strong br h1 h2 h3 h4 h5 h6'), 
				'chamada', removetags(noticia['chamada'], 'p b span strong br h1 h2 h3 h4 h5 h6'), 
				'slug', noticia['slug'], 
				'texto', removetags(noticia['texto'], 'p b span strong br h1 h2 h3 h4 h5 h6'), 
				'categoria__slug', noticia['categoria__slug'], 
				'empresa__id', noticia['empresa__id'], 
			})

		# file = open('ROOT/static/busca/noticias.json', "w")
		# file.write(serialize("json", Noticia.objects.all()))

		with open("ROOT/static/busca/noticias.json", "w") as out:
			# json.dump(noticias, out)
			json_serializer = serializers.get_serializer('json')()
			json_serializer.serialize(Noticia.objects.all(), stream=out)

	return True



# / front








# admin
def verificaNoticiaSlug(request, slug=None):
	resultBusca = Noticia.objects.filter(slug=slug)
	
	if resultBusca:
		noticia = Noticia.objects.filter(slug=slug)[:1]
		context = {'existe': True, 'id': noticia[0].id}
	else:
		context = {'existe': False, 'id': 0}
		

	return HttpResponse(json.dumps(context), content_type="application/json")

def noticiaAddForm(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			form = NoticiaForm(request.POST)
			#pagina = Pagina.objects.filter(slug='adicionar-noticia').first()
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')

			empresas = Empresa.objects.filter(ativo=1)
			

			context = { 'form': form, 
						'pagina': pagina, 
						'menu': menu, 
						'empresas': empresas,
					}


			template = 'rmais/noticiaAddForm.html'
			return render(request,template, context);


def noticiaAddPost(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			if request.method == 'POST':
				form = NoticiaForm(request.POST or None)
				if form.is_valid:
					categoria = request.POST.get('categoria')
					data_da_noticia = request.POST.get('data_da_noticia')
					titulo_format = request.POST.get('titulo')
					titulo = titulo_format
					slug = request.POST.get('slug')
					chamada = request.POST.get('chamada')
					texto = request.POST.get('texto')
					empresasarray = request.POST.get('clientearray')
					data_de_publicacao = request.POST.get('data_de_publicacao')
					ativo = request.POST.get('ativo')
					status = request.POST.get('status')
					fonte = request.POST.get('fonte')

					if ativo is None:
						ativo = 0

					empresas = Empresa.objects.filter(id__in=empresasarray.split(","))
				


					news = Noticia.objects.create(
									# empresa= empresas,
									categoria_id= categoria,
									titulo=titulo,
									slug=slug,
									chamada=chamada,
									texto=texto,
									data_da_noticia=data_da_noticia,
									data_de_publicacao=data_de_publicacao,
									ativo=ativo,
									status=status,
									fonte=fonte
								)

					news.save()

					news.empresa = empresas
					news.save()

		return HttpResponse("ok|%s" % news.pk)

def noticiaEditForm(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			if id:
				noticia = get_object_or_404(Noticia, pk=id)
			else:
				return HttpResponseRedirect('noticia')


			form = NoticiaForm(instance=noticia)
			#pagina = Pagina.objects.filter(slug='adicionar-noticia').first()
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			empresas = Empresa.objects.filter(ativo=1)

			context = { 'form': form, 
						'pagina': pagina, 
						'menu': menu, 
						'empresas': empresas,
						'noticia': noticia,
					}


			template = 'rmais/noticiaEditForm.html'
			return render(request,template, context);

def noticiaEditPost(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			if request.method == 'POST':
				if id:
					noticia = get_object_or_404(Noticia, pk=id)
				else:
					return HttpResponseRedirect('noticia')

				form = NoticiaForm(request.POST or None)
				if form.is_valid:
					categoria = request.POST.get('categoria')
					data_da_noticia = request.POST.get('data_da_noticia')
					titulo = request.POST.get('titulo')
					slug = request.POST.get('slug')
					chamada = request.POST.get('chamada')
					texto = request.POST.get('texto')
					empresasarray = request.POST.get('clientearray')
					data_de_publicacao = request.POST.get('data_de_publicacao')
					ativo = request.POST.get('ativo')
					status = request.POST.get('status')
					fonte = request.POST.get('fonte')

					if ativo is None:
						ativo = 0


					empresas = Empresa.objects.filter(id__in=empresasarray.split(","))
			
					noticia.categoria_id= categoria
					noticia.titulo=titulo
					noticia.slug=slug
					noticia.chamada=chamada
					noticia.texto=texto
					noticia.data_de_publicacao=data_de_publicacao
					noticia.data_da_noticia=data_da_noticia
					noticia.ativo=ativo
					noticia.status=status
					noticia.fonte=fonte
								
					noticia.save()

					noticia.empresa = empresas
					noticia.save()
					return HttpResponse("ok|%s" % noticia.pk)

		return HttpResponse("error")
			
def noticiaListagem(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			#pagina = Pagina.objects.filter(slug='lista-de-usuarios').first()

			empresas = Empresa.objects.filter(ativo=1, delete=0)
			categorias = Categoria.objects.filter(ativo=1, delete=0)



			# >>> teste
			LIST_HEADERS = (
				('ID', 'id'),
				('TÍTULO', 'titulo'),
				('CATEGORIA', 'categoria'),
				('DATA', 'data_de_publicacao'),
				('ON?', 'ativo'),
			)
			sort_headers = SortHeaders(request, LIST_HEADERS)

			noticia_list = Noticia.objects.filter(delete=0).order_by(sort_headers.get_order_by())
		


			# >>> paginacao
			# noticia_list = Noticia.objects.all()
			paginacao = Paginator(noticia_list, 50)# mostra apenas X noticias

			page = request.GET.get('page')
			try:
				noticias = paginacao.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				noticias = paginacao.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				noticias = paginacao.page(paginacao.num_pages)
			# <<< paginacao


			context = {'menu': menu, 
						'pagina': pagina, 
						'noticias': noticias, 
						'empresas': empresas, 
						'categorias': categorias, 
						'headers': list(sort_headers.headers()),
						'url_pagination_params': "&sort=%s&dir=%s" % (request.GET.get('sort'), request.GET.get('dir'))
					}
			template = 'rmais/noticiaListagem.html'

			return render(request, template, context)	
	


		
def noticiaListagemPost(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			if request.method == 'POST':

				fieldCampoBusca 	= request.POST.get('campobusca')
				fieldCampoCliente 	= request.POST.get('cliente_id')
				fieldCampoCategoria = request.POST.get('categoria_id')
				fieldCampoUrl 		= request.POST.get('url')


				list_search = []

				if fieldCampoBusca:
					list_search.append(Q(titulo__icontains=fieldCampoBusca))
					list_search.append(Q(texto__icontains=fieldCampoBusca))
					list_search.append(Q(chamada__icontains=fieldCampoBusca))

				if fieldCampoCategoria:
					list_search.append(Q(categoria_id=fieldCampoCategoria))

				if fieldCampoCliente:
					list_search.append(Q(empresa=fieldCampoCliente))



				if list_search:
					resultBusca = Noticia.objects.filter(reduce(OR, list_search), delete=0)

					context = {'resultBusca': resultBusca, 'urlEdit': fieldCampoUrl.replace('0/', '')}
					return render(request, 'rmais/noticiaListagemPost.json', context)
			
			return render(request, 'rmais/noticiaListagemPost.json')
				
def noticiaDelete(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			noticia = Noticia.objects.get(pk=id)
			if noticia:
				noticia.delete=1
				noticia.save()
				# noticia.delete()
				if noticia.save:
					template = 'noticiaListagem'
					return HttpResponse('true')
				else:
					template = 'noticiaListagem'
					return HttpResponse('false') 
			else:
				template = 'usuarioListagem'
				return HttpResponse('noticia-inexistente')

def duplicar_noticia(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			noticia = Noticia.objects.get(pk=id)

			if noticia:
				# >>> criar noticia
				criar_noticia = Noticia.objects.create(
									categoria= noticia.categoria,
									titulo=noticia.titulo,
									slug=noticia.slug,
									chamada=noticia.chamada,
									texto=noticia.texto,
									data_de_publicacao=noticia.data_de_publicacao,
									data_da_noticia=noticia.data_da_noticia,
									ativo=0,
									status=noticia.status,
									fonte=noticia.fonte,
									# empresa=noticia.empresa
								)
				# # <<< criar noticia

				empresas_all = noticia.empresa.all()
				
				empresasarray = []
				for emp in empresas_all:
					empresasarray.append(emp.id)

				empresas = Empresa.objects.filter(id__in=empresasarray)
				

			
				criar_noticia.empresa = empresas
				criar_noticia.save()

				
				return redirect('noticiaEditForm', criar_noticia.id)

		return HttpResponse('...')

@csrf_exempt
def uploadFile(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
	# 	resultado = handle_uploaded_file(request.FILES['file'])

	# 	if resultado:
	# 		context = {'upload': True}
	# 	else:
	# 		context = {'upload': False}
			
	# 	return HttpResponse(json.dumps(context), content_type="application/json")

		print request.FILES
		# print request.FILES['files[]']
		# print 'files[]' in request.FILES

		saved_images = handle_uploads(request, ['files[]'])
		print saved_images[0][1]

		# print saved_images
		# return HttpResponse(saved_images[0][1])

		return HttpResponse(json.dumps({
											'files': {
												'url': "/%s" % saved_images[0][1]
											}
										}), content_type="application/json")

@csrf_exempt
def deleteFile(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		#### POR SEGURANÇA, NÃO IREMOS APAGAR AS IMAGENS......................
		url_da_imagem = request.POST['file']
		# print url_da_imagem

		a_url = url_da_imagem.split('/')
		nome_da_imagem = a_url[-1]

		# print nome_da_imagem

		url_imagem_local = "/%s%s" % (settings.UPLOAD_PATH, nome_da_imagem)

		# print url_imagem_local




		# delete = os.remove(url_imagem_local)
		# print delete

		return HttpResponse(json.dumps({
											'files': "True"
										}), content_type="application/json")

		




def handle_uploads(request, keys):
	saved = []
    
	upload_dir = date.today().strftime(settings.UPLOAD_PATH)
	upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)

	print upload_dir
	print upload_full_path
	print "teste 1"

	if not os.path.exists(upload_full_path):
		os.makedirs(upload_full_path)

	print "teste 2"
	# print keys

	for key in keys:
		# print key

		# print key in request.FILES

		if key in request.FILES:

			print "teste 4"

			upload = request.FILES[key]

			print upload

			print os.path.join(upload_full_path, upload.name)


			while os.path.exists(os.path.join(upload_full_path, upload.name)):
				print "teste 5"
				upload.name = '_' + upload.name
				print upload

			dest = open(os.path.join(upload_full_path, upload.name), 'wb')
			print "dest: %s" % dest
			print "upload.chunks(): %s" % upload.chunks()
			for chunk in upload.chunks():
				retorno = dest.write(chunk)
				print "retorno: %s" % retorno
			close = dest.close()
			print "close: %s" % close

			print "e agora:"
			saved.append((key, os.path.join(upload_dir, upload.name)))
	# returns [(key1, path1), (key2, path2), ...]
			# print saved
	return saved

# def handle_uploads_unique(request, keys):
# 	saved = []
    
# 	upload_dir = date.today().strftime(settings.UPLOAD_PATH)
# 	upload_full_path = os.path.join(settings.MEDIA_ROOT, upload_dir)

# 	print upload_dir
# 	print upload_full_path
# 	print "teste 1"

# 	if not os.path.exists(upload_full_path):
# 		os.makedirs(upload_full_path)

# 	print "teste 2"

# 	for key in keys:
# 		print "teste 3"
# 		if key in request.FILES:

# 			print "teste 4"
# 			print equest.FILES

# 			upload = request.FILES[key]
# 			while os.path.exists(os.path.join(upload_full_path, upload.name)):
# 				upload.name = '_' + upload.name
# 			dest = open(os.path.join(upload_full_path, upload.name), 'wb')
# 			for chunk in upload.chunks():
# 				dest.write(chunk)
# 			dest.close()
# 			saved.append((key, os.path.join(upload_dir, upload.name)))
# 	# returns [(key1, path1), (key2, path2), ...]
# 	return saved


def listaDeCategoriasPost(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		listCategorias = Categoria.objects.filter(ativo=1)

		return render(request, 'rmais/categorias.json', {'listCategorias': listCategorias})
		# return HttpResponse('okkkk');








def usuarioListagem(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			#pagina = Pagina.objects.filter(slug='lista-de-usuarios').first()





			# >>> teste
			LIST_HEADERS = (
				('ID', 'id'),
				('NOME', 'nome_do_usuario'),
				('E-MAIL', 'email'),
				('CLIENTE', 'empresa'),
				('TIPO', 'id'),
			)
			sort_headers = SortHeaders(request, LIST_HEADERS)


			usuarios_list = Usuario.objects.filter(delete=0).order_by(sort_headers.get_order_by())
			

			paginacao = Paginator(usuarios_list, 50)# mostra apenas X usuarios

			page = request.GET.get('page')

			try:
				# print list(sort_headers.headers())
				usuarios = paginacao.page(page)
				print sort_headers.get_order_by()
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				usuarios = paginacao.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				usuarios = paginacao.page(paginacao.num_pages)
				# print 'page.num_pages'
			# <<< paginacao

			formFiltro = UsuarioFiltroForm(request.POST or None)

			context = {
						'menu': menu, 
						'pagina': pagina, 
						'usuarios': usuarios, 
						'formFiltro': formFiltro,
						'headers': list(sort_headers.headers())
						}
			template = 'rmais/usuarioListagem.html'

			


			return render(request, template, context)

def usuarioListagemPost(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if request.method == 'POST':
			fieldCampoBusca = request.POST.get('campobusca')
			fieldCampoCliente = request.POST.get('cliente_id')
			fieldCampoUrl = request.POST.get('url')

			print "fieldCampoBusca: %s | fieldCampoCliente: %s | fieldCampoUrl: %s" % (fieldCampoBusca, fieldCampoCliente, fieldCampoUrl)

			if fieldCampoCliente:
				empresa = Empresa.objects.get(pk=fieldCampoCliente, delete=0)
				print "empresa: %s" % empresa

				if fieldCampoBusca:
					resultBusca = empresa.usuario_set.filter(
															Q(nome_do_usuario__icontains=fieldCampoBusca) | 
															Q(email__icontains=fieldCampoBusca),
															Q(delete=0)
															)
				else:
					resultBusca = empresa.usuario_set.all
			else:
				if fieldCampoBusca:
					resultBusca = Usuario.objects.filter(
															Q(nome_do_usuario__icontains=fieldCampoBusca) | 
															Q(email__icontains=fieldCampoBusca),
															Q(delete=0)
															)
				else:
					resultBusca = ''
			

			print "resultBusca: %s" % resultBusca

			if resultBusca:
				context = {'resultBusca': resultBusca, 'urlEdit': fieldCampoUrl.replace('0/', '')}
				return render(request, 'rmais/usuarioListagemPost.json', context)
			else:
				return render(request, 'rmais/usuarioListagemPost.json')

def usuarioAddForm(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			form = AddUsuarioForm(request.POST)
			#pagina = Pagina.objects.filter(slug='adicionar-novo-usuario').first()
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')

			context = {'form': form, 'pagina': pagina, 'menu': menu}
			template = 'rmais/usuarioAddForm.html'
			return render(request,template, context);		

def usuarioAddPost(request, status=None, qtd_dias=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if request.method == 'POST':
			form = AddUsuarioForm(request.POST or None)

			if form.is_valid:
				nome = request.POST.get('nome_do_usuario')
				email = request.POST.get('email')
				empresa = request.POST.get('empresa')
				status = status
				dias_liberado = qtd_dias
				senha = id_generator()
				verificaEmail = Usuario.objects.filter(email=email).first()

				# print status

				if verificaEmail:
					return HttpResponse('email-ja-existente')
				else:
					# save
					newUsuario = Usuario(
											nome_do_usuario=nome, 
											email=email, 
											senha=senha, 
											status=status, 
											empresa_id=empresa, 
											dias_liberado=dias_liberado,
										)
					newUsuario.save()

					if newUsuario.save:
						localizarUser = Usuario.objects.last()
						return render(request, 'rmais/usuarioLastAdd.json', {'localizarUser': localizarUser})
					else:
						return HttpResponse('false')
		return render(request, 'rmais/usuarioLastAdd.json', {'localizarUser': localizarUser})
		

	 
def usuarioEditForm(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			#pagina = Pagina.objects.filter(slug='lista-de-usuarios').first()
			usuario = get_object_or_404(Usuario, pk=id)

			if usuario:
			   form = AddUsuarioForm(initial = {
												'nome_do_usuario': usuario.nome_do_usuario,
												'email': usuario.email,
												'empresa': usuario.empresa,
												'status': usuario.status,
												'dias_liberado': usuario.dias_liberado,
												})

			   

			context = {
						'menu': menu, 
						'pagina': pagina, 
						'form': form, 
						'usuario': usuario
						}
			template = 'rmais/usuarioEditForm.html'
			return render(request, template, context)

def usuarioEditPost(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if request.method == 'POST':
			usuario = Usuario.objects.get(pk=id)

			if usuario:
				email = request.POST.get('email')
				usuarios = Usuario.objects.filter(email=email)

				if usuarios:
					if usuarios[0].id != usuario.id:
						return HttpResponse('email-ja-existe')
					else:
						# o email deste usuario ainda é o mesmo	
						form = AddUsuarioForm(request.POST or None)
						if form.is_valid:
							usuario.nome_do_usuario = request.POST.get('nome_do_usuario')
							usuario.email = email
							usuario.empresa_id = request.POST.get('empresa')
							usuario.status = request.POST.get('status')
							usuario.dias_liberado = request.POST.get('dias_liberado')

							fields = ['nome_do_usuario', 'email','status', 'empresa_id', 'dias_liberado']
							usuario.save(update_fields=fields)
							
							if usuario.save:
								return HttpResponse('true')
							else:
								return HttpResponse('false')

				else:
					# ele não achou nenhum usuario com este email 
					# então, o mesmo sera alterado
					form = AddUsuarioForm(request.POST or None)
					if form.is_valid:
						usuario.nome_do_usuario = request.POST.get('nome_do_usuario')
						usuario.email = email
						usuario.status = request.POST.get('empresa')
						usuario.empresa_id = request.POST.get('status')
						usuario.dias_liberado = request.POST.get('dias_liberado')

						fields = ['nome_do_usuario', 'email','status', 'empresa_id', 'dias_liberado']
						usuario.save(update_fields=fields)

						if usuario.save:
							return HttpResponse('true')
						else:
							return HttpResponse('false')

def usuarioDelete(request, id=None):	
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		usuario = Usuario.objects.get(pk=id)
		if usuario:
			usuario.delete=1
			usuario.save()
			if usuario.save:
				template = 'usuarioListagem'
				return HttpResponse('true')
			else:
				template = 'usuarioListagem'
				return HttpResponse('false') 
		else:
			template = 'usuarioListagem'
			return HttpResponse('usuario-inexistente')









def clientesListagem(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			

			LIST_HEADERS = (
			    ('ID', 'id'),
			    ('NOME EMPRESA', 'nome_da_empresa'),
			    ('CONTATO', 'nome_do_contato'),
			    ('ATIVO', 'ativo'),
			    ('TIPO DE USUARIO', 'tipo_de_usuario'),
			)
			sort_headers = SortHeaders(request, LIST_HEADERS)


			empresas_list = Empresa.objects.filter(delete=0).order_by(sort_headers.get_order_by())
			

			paginacao = Paginator(empresas_list, 50)# mostra apenas X usuarios

			page = request.GET.get('page')

			try:
				# print list(sort_headers.headers())
				empresas = paginacao.page(page)
				print sort_headers.get_order_by()
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				empresas = paginacao.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				empresas = paginacao.page(paginacao.num_pages)
				# print 'page.num_pages'
			# <<< paginacao


			context = {
						'menu': menu, 
						'empresas': empresas, 
						'headers': list(sort_headers.headers()),
						'url_pagination_params': "&sort=%s&dir=%s" % (request.GET.get('sort'), request.GET.get('dir'))
						}
			template = 'rmais/clientesListagem.html'

			


			return render(request, template, context)
		
def clientesListagemPost(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		if request.method == 'POST':
			fieldCampoBusca = request.POST.get('campobusca')
			fieldCampoUrlEdit = request.POST.get('urlEdit')
			fieldCampoUrlDelete = request.POST.get('urlDel')

			if fieldCampoBusca:
				resultBusca = Empresa.objects.filter(
												Q(nome_da_empresa__icontains=fieldCampoBusca) | 
												Q(nome_do_contato__icontains=fieldCampoBusca) |
												Q(email_do_contato__icontains=fieldCampoBusca) |
												Q(tipo_de_usuario__icontains=fieldCampoBusca),
												delete=0
												)

				if resultBusca:
					context = {
								'resultBusca': resultBusca,
								'fieldCampoUrlEdit': fieldCampoUrlEdit.replace('0/', ''),
								'fieldCampoUrlDelete': fieldCampoUrlDelete.replace('0/', ''),
							}
					template = 'rmais/clientesListagemPost.json'
					return render(request, template, context)
				else:
					
					context = {
								'resultBusca': resultBusca,
								'fieldCampoUrlEdit': fieldCampoUrlEdit.replace('0/', ''),
								'fieldCampoUrlDelete': fieldCampoUrlDelete.replace('0/', ''),
							}
					template = 'rmais/clientesListagemPost.json'
					return render(request, template, context)

def clienteAddForm(request):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			form = EmpresasForm(request.POST)
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')

			context = {'form': form, 'pagina': pagina, 'menu': menu}
			template = 'rmais/clienteAddForm.html'
			return render(request,template, context);		

def clienteAddFormPost(request):
	print 'xgou no metodo'
	if request.method == 'POST':
		print 'deu post'

		form = EmpresasForm(request.POST or None)

		if form.is_valid:
			nome_da_empresa = request.POST.get('nome_da_empresa')
			endereco = request.POST.get('endereco')
			nome_do_contato = request.POST.get('nome_do_contato')
			email_do_contato = request.POST.get('email_do_contato')
			tipo_de_usuario = 0
			if request.POST.get('ativo'):
				ativo = request.POST.get('ativo')
			else:
				ativo = 0
			
			# save
			newCliente = Empresa(
									nome_da_empresa=nome_da_empresa, 
									endereco=endereco, 
									nome_do_contato=nome_do_contato, 
									email_do_contato=email_do_contato, 
									tipo_de_usuario=tipo_de_usuario, 
									ativo=ativo,
								)


			newCliente.save()

			
			
			if newCliente.save:
				print 'o cliente foi salvo com sucesso'
				localizarUser = Empresa.objects.last()
				return render(request, 'rmais/clienteLastAdd.json', {'localizarUser': localizarUser})
			else:
				return HttpResponse('false')
	# return			

def clienteEditForm(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			empresa = get_object_or_404(Empresa, pk=id)
			if empresa:
			   	form = EmpresasForm(initial = {
												# 'estado': empresa.estado,
												# 'cidade': empresa.cidade,
												'nome_da_empresa': empresa.nome_da_empresa,
												'endereco': empresa.endereco,
												'nome_do_contato': empresa.nome_do_contato,
												'email_do_contato': empresa.email_do_contato,
												'tipo_de_usuario': empresa.tipo_de_usuario,
												'ativo': empresa.ativo,
												})

		
			
			context = {'menu': menu, 'pagina': pagina, 'empresa': empresa, 'form': form}
			template = 'rmais/clienteEditForm.html'
			return render(request, template, context)

def clienteEditFormPost(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:
		if 'logado' not in request.session:
			return redirect('login')
		else: 
			menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
			empresa = get_object_or_404(Empresa, pk=id)
			
			if empresa:
			   	empresa.nome_da_empresa = request.POST.get('nome_da_empresa')
				empresa.endereco = request.POST.get('endereco')
				empresa.nome_do_contato = request.POST.get('nome_do_contato')
				empresa.email_do_contato = request.POST.get('email_do_contato')
				# empresa.tipo_de_usuario = request.POST.get('tipo_de_usuario')
				if request.POST.get('ativo'):
					empresa.ativo = request.POST.get('ativo')
				else:
					empresa.ativo = 0

				fields = [
						'nome_da_empresa', 
						'endereco',
						'nome_do_contato', 
						'email_do_contato', 
						'tipo_de_usuario', 
						'ativo'
						]
				empresa.save(update_fields=fields)

				if empresa.save:
					return HttpResponse('true')
				else:
					return HttpResponse('false')

def clienteDelete(request, id=None):
	if request.session.get('tipo_usuario') != 1:
		return redirect('home')
	else:	
		empresa = Empresa.objects.get(pk=id)
		if empresa:
			empresa.delete=1
			empresa.save()
			if empresa.save:
				template = 'empresaListagem'
				return HttpResponse('true')
			else:
				template = 'empresaListagem'
				return HttpResponse('false') 
		else:
			template = 'empresaListagem'
			return HttpResponse('empresa-inexistente')







def configuracoes(request):
	if 'logado' not in request.session:
		return redirect('login')
	else: 
		menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).values('id', 'titulo', 'slug').order_by('ordem')
		template = 'rmais/configuracoes.html'

		return render(request, template, {'menu': menu})

def configuracoesPost(request):
	if request.method == 'POST':
		usuario = Usuario.objects.get(pk=request.session.get('usuario_id'))
		senha_atual = request.POST.get('senha_atual')
		nova_senha = request.POST.get('senha_nova')

		qtd_caracter_senha = len(nova_senha)

		if usuario.senha == senha_atual:
			if qtd_caracter_senha >= 3:
				usuario.senha = nova_senha
				fields = [ 
						'senha',
						]
				usuario.save(update_fields=fields)
				if usuario.save:
					return HttpResponse('true')
				else:
					return HttpResponse('false')
			else:
				return HttpResponse('min-caracter_senha')

		else: 
			return HttpResponse('senha-error')
	return HttpResponse('ok')

	

# gerador de chave randomica      
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))






