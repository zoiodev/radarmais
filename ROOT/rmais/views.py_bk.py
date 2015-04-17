# -*- coding: utf-8 -*-
from django.conf import settings # mail
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import UsuarioForm, SenhaForm, AddUsuarioForm, NoticiaForm
from rmais.models import Categoria, Noticia, Pagina, Usuario, Empresa


import random
import string



# like conditions sensitive with OR example: titulo=buscar OR chamada=buscar or texto=buscar
from django.db.models import Q

# envio de email
from django.core.mail import send_mail, mail_admins, EmailMessage
# from django.core.mail import EmailMessage




def login(request):
    if 'logado' in request.session:
        return redirect('home')
    else:
        form = UsuarioForm(request.POST)
        formSenha = SenhaForm(request.POST)

        if request.method == 'POST':
            if form.is_valid:
                login = request.POST.get('usuario')
                senha = request.POST.get('senha')

                usuario = Usuario.objects.filter(email=login, senha=senha).first()

                if usuario:
                    request.session['logado'] = 1
                    request.session['empresa_id'] = usuario.empresa.id

                    return redirect('home')
                else:
                    request.session['logado_error'] = 'log-error'
        
        return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha})


def logout(request):
    del request.session['logado']
        
    return redirect('login')


def home(request):
    # print request.session.keys()

    # print request.session['logado']
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
        categorias  = Categoria.objects.filter(ativo=1).order_by('ordem')[:4]
        pagina = Pagina.objects.filter(slug='home').order_by('-id').first()
        noticias = Categoria.objects.first()

        return render(request, 'rmais/home.html', {'categorias': categorias, 'noticias': noticias, 'menu': menu, 'pagina': pagina})


def listagem(request, slug=None):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
        categoria = Categoria.objects.filter(slug=slug).order_by('-id').first()
        noticias  = Noticia.objects.filter(ativo=1, categoria_id=categoria).order_by('data_criacao')

        return render(request, 'rmais/listagem.html', {'noticias': noticias, 'categoria': categoria, 'menu': menu})


def noticia(request, categoria=None, slug=None):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
        noticia  = Noticia.objects.filter(slug=slug).order_by('-id').first()
        categoria = Categoria.objects.filter(id=noticia.categoria_id).order_by('-id').first()
        
        return render(request, 'rmais/noticia.html', {'noticia': noticia, 'categoria': categoria, 'menu': menu})


def noticiaForm(request):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        form = NoticiaForm(request.POST)
        pagina = Pagina.objects.filter(slug='adicionar-noticia').first()
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')


        context = {'form': form, 'pagina': pagina, 'menu': menu}
        template = 'rmais/noticiaForm.html'
        return render(request,template, context);

def pagina(request, page=None):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
        pagina = Pagina.objects.filter(slug=page).order_by('-id').first()
        
        return render(request, 'rmais/pagina.html', {'pagina': pagina, 'menu': menu})


def rbusca(request, buscar=None):
    resultBusca = Noticia.objects.filter(Q(titulo__icontains=buscar) | Q(chamada__icontains=buscar) | Q(texto__icontains=buscar))
    if resultBusca:
        context = {'resultBusca': resultBusca}
    else:
        return render(request, 'rmais/rbusca.json')
        
    return render(request, 'rmais/rbusca.json', context)


def email(request):
    formSenha = SenhaForm(request.POST)

    if formSenha.is_valid:
        email = request.GET['email']

        usuario = Usuario.objects.filter(email=email).first()
        
        if usuario:
            # # teste
            assunto = 'Login e Senha Radar+'
            message = 'Sua senha: %s'%usuario.senha 
            from_addr = settings.EMAIL_HOST_USER  
            usuarioEmail = [usuario.email] 

            send_mail("New comment added", message, from_addr, usuarioEmail, fail_silently=True)
            # mail_admins("subject", 'some text', fail_silently=True)
            # EmailMessage('Subject', 'Body', to=recipient_list)
            
            # /teste
            
            return HttpResponse('true')
            
        else:
            return HttpResponse('false')


def usuarioFormulario(request):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        form = AddUsuarioForm(request.POST)
        pagina = Pagina.objects.filter(slug='adicionar-novo-usuario').first()
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')

        context = {'form': form, 'pagina': pagina, 'menu': menu}
        template = 'rmais/usuarioAdd.html'
        return render(request,template, context);


        

def usuarioAdd(request):
    if request.method == 'POST':
        form = AddUsuarioForm(request.POST or None)

        if form.is_valid:
            nome = request.POST.get('nome_do_usuario')
            email = request.POST.get('email')
            empresa = request.POST.get('empresa')
            status = request.POST.get('status')
            dias_liberado = request.POST.get('dias_liberado')
            senha = id_generator()

            # form.save()
            

            verificaEmail = Usuario.objects.filter(email=email).first()
            if verificaEmail:
                return HttpResponse('email-ja-existente')
            else:
                # save
                newUsuario = Usuario(nome_do_usuario=nome, email=email, senha=senha, status=status, empresa_id=empresa, dias_liberado=dias_liberado)
                newUsuario.save()

                if newUsuario.save:
                    localizarUser = Usuario.objects.last()
                    return HttpResponse('true', {'localizarUser': localizarUser})
                else:
                    return HttpResponse('false')
        
def usuarioList(request):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
        pagina = Pagina.objects.filter(slug='lista-de-usuarios').first()
        # >>> paginacao
        usuarios_list = Usuario.objects.all()
        paginacao = Paginator(usuarios_list, 5)# mostra apenas X usuarios

        page = request.GET.get('page')
        try:
            usuarios = paginacao.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            usuarios = paginacao.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            usuarios = paginacao.page(paginacao.num_pages)
        # <<< paginacao


        context = {'menu': menu, 'pagina': pagina, 'usuarios': usuarios}
        template = 'rmais/usuarioList.html'

        return render(request, template, context)
      
def usuarioEdit(request, id=None):
    if 'logado' not in request.session:
        return redirect('login')
    else: 
        menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
        pagina = Pagina.objects.filter(slug='lista-de-usuarios').first()
        usuario = get_object_or_404(Usuario, pk=id)
        if usuario:
           # form = AddUsuarioForm(request.POST or None)
           form = AddUsuarioForm(initial = {
                                            'nome_do_usuario': usuario.nome_do_usuario,
                                            'email': usuario.email,
                                            'empresa': usuario.empresa,
                                            'status': usuario.status,
                                            'dias_liberado': usuario.dias_liberado,
                                            })

    
        
        context = {'menu': menu, 'pagina': pagina, 'form': form, 'usuario': usuario}
        template = 'rmais/usuarioEdit.html'
        return render(request, template, context)

def edit(request, id=None):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, pk=id)
        if usuario:
            form = AddUsuarioForm(request.POST or None)
            if form.is_valid:
                nome = request.POST.get('nome_do_usuario')
                email = request.POST.get('email')
                empresa = request.POST.get('empresa')
                status = request.POST.get('status')
                dias_liberado = request.POST.get('dias_liberado')
          

                usuario.nome_do_usuario = nome
                usuario.email = email
                usuario.status = status
                usuario.empresa_id = empresa
                usuario.dias_liberado = dias_liberado

                fields = ['nome_do_usuario', 'email','status', 'empresa_id', 'dias_liberado']
                usuario.save(update_fields=fields)

                if usuario.save:
                    return HttpResponse('true')
                else:
                    return HttpResponse('false')


def delete(request, id=None):
    usuario = Usuario.objects.get(pk=id)
    if usuario:
        usuario.delete()
        if usuario.delete:
            template = 'usuarioList'
            return HttpResponse('true')
        else:
            template = 'usuarioList'
            return HttpResponse('false') 
    else:
        template = 'usuarioList'
        return HttpResponse('usuario-inexistente')

    

# gerador de chave randomica      
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))















# # bk
# # -*- coding: utf-8 -*-
# from django.conf import settings # mail
# from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, HttpResponse, redirect
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .forms import UsuarioForm, SenhaForm, AddUsuarioForm
# from rmais.models import Categoria, Noticia, Pagina, Usuario, Empresa


# import random
# import string



# # like conditions sensitive with OR example: titulo=buscar OR chamada=buscar or texto=buscar
# from django.db.models import Q

# # envio de email
# from django.core.mail import send_mail, mail_admins, EmailMessage
# # from django.core.mail import EmailMessage



# def login(request):
#     if 'logado' in request.session:
#         return redirect('home')
#     else:
#         form = UsuarioForm(request.POST)
#         formSenha = SenhaForm(request.POST)

#         if request.method == 'POST':
#             if form.is_valid:
#                 login = request.POST.get('usuario')
#                 senha = request.POST.get('senha')

#                 usuario = Usuario.objects.filter(email=login, senha=senha).first()

#                 if usuario:
#                     request.session['logado'] = 1
#                     request.session['empresa_id'] = usuario.empresa.id

#                     return redirect('home')
#                 else:
#                     request.session['logado_error'] = 'log-error'
        
#         return render(request, 'rmais/login.html', {'form': form, 'formSenha': formSenha})


# def logout(request):
#     del request.session['logado']
        
#     return redirect('login')


# def home(request):
#     # print request.session.keys()

#     # print request.session['logado']
#     if 'logado' not in request.session:
#         return redirect('login')
#     else: 
        
#         menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
#         categorias  = Categoria.objects.filter(ativo=1).order_by('ordem')[:4]
#         pagina = Pagina.objects.filter(slug='home').order_by('-id').first()
#         noticias = Categoria.objects.first()

#         return render(request, 'rmais/home.html', {'categorias': categorias, 'noticias': noticias, 'menu': menu, 'pagina': pagina})


# def listagem(request, slug=None):
#     if 'logado' not in request.session:
#         return redirect('login')
#     else: 
#         menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
#         categoria = Categoria.objects.filter(slug=slug).order_by('-id').first()
#         noticias  = Noticia.objects.filter(ativo=1, categoria_id=categoria).order_by('data_criacao')

#         return render(request, 'rmais/listagem.html', {'noticias': noticias, 'categoria': categoria, 'menu': menu})


# def noticia(request, categoria=None, slug=None):
#     if 'logado' not in request.session:
#         return redirect('login')
#     else: 
#         menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
#         noticia  = Noticia.objects.filter(slug=slug).order_by('-id').first()
#         categoria = Categoria.objects.filter(id=noticia.categoria_id).order_by('-id').first()
        
#         return render(request, 'rmais/noticia.html', {'noticia': noticia, 'categoria': categoria, 'menu': menu})


# def pagina(request, page=None):
#     if 'logado' not in request.session:
#         return redirect('login')
#     else: 
#         menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
#         pagina = Pagina.objects.filter(slug=page).order_by('-id').first()
        
#         return render(request, 'rmais/pagina.html', {'pagina': pagina, 'menu': menu})


# def rbusca(request, buscar=None):
#     resultBusca = Noticia.objects.filter(Q(titulo__icontains=buscar) | Q(chamada__icontains=buscar) | Q(texto__icontains=buscar))
#     if resultBusca:
#         context = {'resultBusca': resultBusca}
#     else:
#         return render(request, 'rmais/rbusca.json')
        
#     return render(request, 'rmais/rbusca.json', context)


# def email(request):
#     formSenha = SenhaForm(request.POST)

#     if formSenha.is_valid:
#         email = request.GET['email']

#         usuario = Usuario.objects.filter(email=email).first()
        
#         if usuario:
#             # # teste
#             assunto = 'Login e Senha Radar+'
#             message = 'Sua senha: %s'%usuario.senha 
#             from_addr = settings.EMAIL_HOST_USER  
#             usuarioEmail = [usuario.email] 

#             send_mail("New comment added", message, from_addr, usuarioEmail, fail_silently=True)
#             # mail_admins("subject", 'some text', fail_silently=True)
#             # EmailMessage('Subject', 'Body', to=recipient_list)
            
#             # /teste
            
#             return HttpResponse('true')
            
#         else:
#             return HttpResponse('false')


# def usuarioFormulario(request):
#     if 'logado' not in request.session:
#         return redirect('login')
#     else: 
#         form = AddUsuarioForm(request.POST)
#         pagina = Pagina.objects.filter(slug='adicionar-novo-usuario').first()
#         menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')

#         context = {'form': form, 'pagina': pagina, 'menu': menu}
#         template = 'rmais/usuarioAdd.html'
#         return render(request,template, context);
        

# def usuarioAdd(request):
#     if request.method == 'POST':
#         form = AddUsuarioForm(request.POST or None)

#         if form.is_valid:
#             nome = request.POST.get('nome_do_usuario')
#             email = request.POST.get('email')
#             empresa = request.POST.get('empresa')
#             status = request.POST.get('status')
#             dias_liberado = request.POST.get('dias_liberado')
#             senha = id_generator()

#             # form.save()
            

#             verificaEmail = Usuario.objects.filter(email=email).first()
#             if verificaEmail:
#                 return HttpResponse('email-ja-existente')
#             else:
#                 # save
#                 newUsuario = Usuario(nome_do_usuario=nome, email=email, senha=senha, status=status, empresa_id=empresa, dias_liberado=dias_liberado)
#                 newUsuario.save()

#                 if newUsuario.save:
#                     return HttpResponse('true')
#                 else:
#                     return HttpResponse('false')
        
# def usuarioList(request):
#     if 'logado' not in request.session:
#         return redirect('login')
#     else: 
#         menu = Pagina.objects.filter(ativo=1, aparecer_no_menu=1).order_by('ordem')
#         pagina = Pagina.objects.filter(slug='lista-de-usuarios').first()
#         usuarios_list = Usuario.objects.all()
#         paginacao = Paginator(usuarios_list, 5)# mostra apenas X usuarios

#         page = request.GET.get('page')
#         try:
#             usuarios = paginacao.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             usuarios = paginacao.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results.
#             usuarios = paginacao.page(paginacao.num_pages)


#         context = {'menu': menu, 'pagina': pagina, 'usuarios': usuarios}
#         template = 'rmais/usuarioList.html'

#         return render(request, template, context)
        

# # gerador de chave randomica      
# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))
