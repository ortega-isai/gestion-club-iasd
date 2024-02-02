from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import CuentaContable, Salida, ConceptoSalida, Concepto, Entrada, ConceptoEntrada


@admin.register(CuentaContable)
class CuentaContableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = CuentaContable


@admin.register(Concepto)
class ConceptoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Concepto


class ConceptoEntradaTabularInline(admin.TabularInline):
    model = ConceptoEntrada
    autocomplete_fields = ["miembro"]


@admin.register(Entrada)
class EntradaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Entrada
    list_filter = ["fecha_pago",
                   "conceptoentrada__concepto", "conceptoentrada__cuenta_contable", "de"]
    list_display = ['id', 'folio', 'fecha_pago',
                    'de', 'conceptos', 'total_importe']
    search_fields = ['id', "fecha_pago", "de__nombre", "de__apellido_paterno",
                     "de__apellido_materno"]
    inlines = [ConceptoEntradaTabularInline]
    autocomplete_fields = ["de"]


class ConceptoSalidaTabularInline(admin.TabularInline):
    model = ConceptoSalida
    # autocomplete_fields = ["miembro"]


@admin.register(Salida)
class SalidaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Salida
    list_filter = ["fecha_pago", "conceptosalida__cuenta_contable", "de"]
    list_display = ['id', 'folio', 'fecha_pago',
                    'de', 'conceptos', 'total_importe']
    search_fields = ['id', "fecha_pago", "de__nombre", "de__apellido_paterno",
                     "de__apellido_materno"]
    inlines = [ConceptoSalidaTabularInline]
    autocomplete_fields = ["de"]
