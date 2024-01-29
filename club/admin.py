from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Miembro, Familia, TipoMiembro, ClaseMiembro


@admin.register(TipoMiembro)
class TipoMiembroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = TipoMiembro


@admin.register(ClaseMiembro)
class ClaseMiembroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = ClaseMiembro


@admin.register(Miembro)
class MiembroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido_paterno', 'apellido_materno',
                    'fecha_nacimiento', 'sexo', 'tipo_miembro', 'clase', 'miembro_iglesia']
    list_filter = ["tipo_miembro", "sexo", "clase"]
    search_fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'sexo',
                     'tipo_miembro', 'clase', 'miembro_iglesia']
    # fields = ['miembro', 'fecha_pago',
    #           'concepto', 'importe', 'notas']


@admin.register(Familia)
class FamiliaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    autocomplete_fields = ["miembro"]
