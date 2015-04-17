from django.contrib import admin
from rmais.models import Categoria, Empresa, Usuario, Estado, Cidade, Represa, NivelDaAgua, Pagina, GaleriaImagen, Noticia, Leitura


# >>> categoria
class CategoriaAdmin(admin.ModelAdmin):
	# mostrar campos list
	list_display = ('nome_da_categoria', 'ativo')

	#campos a serem inseridos
	fieldsets = [
		('Categoria', 	{'fields': ['nome_da_categoria']}),
		(None, 	{'fields': ['slug']}),
        (None,  {'fields': ['logo']}),
		(None, 	{'fields': ['banner']}),
		(None, 	{'fields': ['ordem']}),
		(None, 	{'fields': ['ativo']}),
	]
	# url amigavel
	prepopulated_fields = {"slug": ("nome_da_categoria",)}
# <<< categoria


# >>> empresa
class EmpresaAdmin(admin.ModelAdmin):
	# mostrar campos list	
	list_display = ('nome_da_empresa', 'ativo')
	# busca
	search_fields = ['nome_da_empresa', 'email_do_contato']
# <<< empresa

# >>> usuarios
class UsuarioAdmin(admin.ModelAdmin):
	# busca
	serach_fields = ['nome_do_usuario', 'email', 'cidade_de_preferencia']
	# relacionamento
# <<< usuarios

# >>> galeriaImagen
class GaleriaImagenAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['legenda', ]
    list_display = ('legenda', 'ativo')
# <<< galeriaImagen


# >>> Estado
class EstadoAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['sigla', 'nome']
# <<< Estado

# >>> Cidade
class CidadeAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['nome',]
# <<< Cidade

# >>> noticias
class NoticiaAdmin(admin.ModelAdmin):
    search_fields = ['titulo', 'chamada', 'texto', 'fonte']
    prepopulated_fields = {"slug": ("titulo",)}
    list_display = ('titulo', 'ativo')
# <<< noticias

# >>> Represa
class RepresaAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['nome_da_represa',]
# <<< Represa

# >>> NivelDaAgua
class NivelDaAguaAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['nivel_da_agua',]
# <<< NivelDaAgua

# >>> Pagina
class PaginaAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['titulo', 'texto']
    prepopulated_fields = {"slug": ("titulo",)}
    list_display = ('titulo', 'ativo')
# <<< Pagina

# >>> Cidade
class LeituraAdmin(admin.ModelAdmin):
    # busca
    search_fields = ['campo_teste',]
# <<< Cidade




# >>> registros do admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Usuario)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(GaleriaImagen, GaleriaImagenAdmin)
admin.site.register(Represa, RepresaAdmin)
admin.site.register(NivelDaAgua, NivelDaAguaAdmin)
admin.site.register(Pagina, PaginaAdmin)
admin.site.register(Leitura, LeituraAdmin)




