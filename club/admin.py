from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Miembro, Familia, TipoMiembro, ClaseMiembro


@admin.register(TipoMiembro)
class TipoMiembroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = TipoMiembro


@admin.register(ClaseMiembro)
class ClaseMiembroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = ClaseMiembro
    # list_display = ('descripcion', 'hexcolor', 'colored_name')


@admin.register(Miembro)
class MiembroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido_paterno', 'apellido_materno',
                    'fecha_nacimiento', 'sexo', 'tipo_miembro', 'clase', 'miembro_iglesia']
    list_filter = ["tipo_miembro", "sexo", "clase"]
    search_fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'sexo',
                     'tipo_miembro', 'clase', 'miembro_iglesia']
    # fields = ['miembro', 'fecha_pago',
    #           'concepto', 'importe', 'notas']


class MiembroInline(admin.StackedInline):
    model = Miembro


@admin.register(Familia)
class FamiliaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Familia
    # autocomplete_fields = ["miembro"]
    inlines = [MiembroInline]
