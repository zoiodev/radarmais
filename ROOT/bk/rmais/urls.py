# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rmais import views



##############################################################
# REGRAS DE URLS
# PADRÃO ADMIN FRONT: dashboard/admin/...
#
#   => USUÁRIO
#       Listagem: 
#			URL: 	dashboard/admin/usuarios/listagem
#			Método:	usuarioListagem
#
#       Formulário de Adição: 
#			URL:	dashboard/admin/usuarios/add/
#			Método: usuarioAddForm
#
#       Post de Adição: 
#			URL:	dashboard/admin/usuarios/add/post
#			Método: usuarioAddPost
#
#       Formulário de Edição: 
#			URL:	dashboard/admin/usuarios/edit/x
#			Método: usuarioEditForm
#
#       Post de Edição: 
#			URL:	dashboard/admin/usuarios/edit/post/x
#			Método: usuarioEditPost
#
##############################################################


urlpatterns = patterns('',
	url(r'^$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'), 
	url(r'^dashboard/$', views.home, name='home'), 
	url(r'^dashboard/admin/clientes/add/$', views.clienteAddForm, name='clienteAddForm'),
	url(r'^dashboard/admin/clientes/add/post/$', views.clienteAddFormPost, name='clienteAddFormPost'),  
	url(r'^dashboard/admin/clientes/listagem/$', views.clientesListagem, name='clientesListagem'),  
	url(r'^dashboard/admin/clientes/clientesListagemPost/$', views.clientesListagemPost, name='clientesListagemPost'),  
	url(r'^dashboard/admin/clientes/edit/(?P<id>\d+)/$', views.clienteEditForm, name='clienteEditForm'),  
	url(r'^dashboard/admin/clientes/edit/post/(?P<id>[a-zA-Z0-9_.-]+)/$', views.clienteEditFormPost, name='clienteEditFormPost'),  
	url(r'^dashboard/admin/clientes/delete/(?P<id>[a-zA-Z0-9_.-]+)/$', views.clienteDelete, name='clienteDelete'),  
	url(r'^dashboard/admin/usuarios/listagem/$', views.usuarioListagem, name='usuarioListagem'),  
	url(r'^dashboard/admin/usuarios/add/$', views.usuarioAddForm, name='usuarioAddForm'),
	url(r'^dashboard/admin/usuarios/add/post/$', views.usuarioAddPost, name='usuarioAddPost'),    
	url(r'^dashboard/admin/usuarios/edit/(?P<id>\d+)/$', views.usuarioEditForm, name='usuarioEditForm'),  
	url(r'^dashboard/admin/usuarios/edit/post/(?P<id>[a-zA-Z0-9_.-]+)/$', views.usuarioEditPost, name='usuarioEditPost'),  
	url(r'^dashboard/admin/usuarios/delete/(?P<id>[a-zA-Z0-9_.-]+)/$', views.usuarioDelete, name='usuarioDelete'),  
	url(r'^dashboard/admin/usuarios/usuarioListagemPost/$', views.usuarioListagemPost, name='usuarioListagemPost'),  
	url(r'^dashboard/admin/noticias/add/$', views.noticiaAddForm, name='noticiaAddForm'), 
	url(r'^dashboard/admin/noticias/add/post/$', views.noticiaAddPost, name='noticiaAddPost'), 
	url(r'^dashboard/admin/noticias/edit/(?P<id>[a-zA-Z0-9_.-]+)/$', views.noticiaEditForm, name='noticiaEditForm'), 
	url(r'^dashboard/admin/noticias/edit/post/(?P<id>[a-zA-Z0-9_.-]+)/$', views.noticiaEditPost, name='noticiaEditPost'), 
	url(r'^dashboard/admin/noticias/verifica-slug/(?P<slug>[a-zA-Z0-9_.-]+)/$', views.verificaNoticiaSlug, name='verificaNoticiaSlug'), 
	url(r'^dashboard/admin/noticias/lista-de-categorias/post/$', views.listaDeCategoriasPost, name='listaDeCategoriasPost'), 
	url(r'^dashboard/admin/noticias/listagem/$', views.noticiaListagem, name='noticiaListagem'),  
	url(r'^dashboard/admin/noticias/delete/(?P<id>[a-zA-Z0-9_.-]+)/$', views.noticiaDelete, name='noticiaDelete'),  
	url(r'^dashboard/admin/usuarios/noticiaListagemPost/$', views.noticiaListagemPost, name='noticiaListagemPost'),
	url(r'^dashboard/admin/upload-files/$', views.uploadFile, name='uploadFile'),
	url(r'^dashboard/admin/delete-files/$', views.deleteFile, name='deleteFile'),
	url(r'^info/(?P<page>[a-zA-Z0-9_.-]+)/$', views.pagina, name="pagina"),
	url(r'^busca/(?P<buscar>[a-zA-Z0-9_.-]+)/$', views.rbusca, name='rbusca'), 
	url(r'^enviar-email/$', views.email, name='email'), 
	url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', views.listagem, name="listagem"),
	url(r'^(?P<categoria>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/$', views.noticia, name="noticia"),
)