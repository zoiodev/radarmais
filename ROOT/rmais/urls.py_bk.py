# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rmais import views

##############################################################
# REGRAS DE URLS
# PADRÃO ADMIN FRONT: dashboard/admin/...
#
#   => USUÁRIO
#       Listagem: 
#           URL:    dashboard/admin/usuarios/listagem
#           Método: usuarioListagem
#
#       Formulário de Adição: 
#           URL:    dashboard/admin/usuarios/add/
#           Método: usuarioAddForm
#
#       Post de Adição: 
#           URL:    dashboard/admin/usuarios/add/post
#           Método: usuarioAddPost
#
#       Formulário de Edição: 
#           URL:    dashboard/admin/usuarios/edit/x
#           Método: usuarioEditForm
#
#       Post de Edição: 
#           URL:    dashboard/admin/usuarios/edit/post/x
#           Método: usuarioEditPost
#
##############################################################

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'), 
    url(r'^dashboard/$', views.home, name='home'), 
    url(r'^adicionar-novo-usuario/$', views.usuarioFormulario, name='usuarioFormulario'),  
    url(r'^lista-de-usuarios/$', views.usuarioList, name='usuarioList'),  
    url(r'^dashboard/adicionar-usuario/add/$', views.usuarioAdd, name='usuarioAdd'),  
    url(r'^dashboard/adicionar-usuario/edit/(?P<id>\d+)/$', views.usuarioEdit, name='usuarioEdit'),  
    url(r'^dashboard/usuario/edit/(?P<id>[a-zA-Z0-9_.-]+)/$', views.edit, name='edit'),  
    url(r'^dashboard/usuario/del/(?P<id>[a-zA-Z0-9_.-]+)/$', views.delete, name='delete'),  
    url(r'^listagem/(?P<slug>[a-zA-Z0-9_.-]+)/$', views.listagem, name="listagem"),
    url(r'^adicionar-noticia/$', views.noticiaForm, name='noticiaForm'), 
    url(r'^(?P<categoria>[a-zA-Z0-9_.-]+)/noticia/(?P<slug>[a-zA-Z0-9_.-]+)/$', views.noticia, name="noticia"),
    url(r'^(?P<page>[a-zA-Z0-9_.-]+)/$', views.pagina, name="pagina"),
    url(r'^dashboard/busca/(?P<buscar>[a-zA-Z0-9_.-]+)/$', views.rbusca, name='rbusca'), 
    url(r'^dashboard/enviar-email/$', views.email, name='email'), 
)