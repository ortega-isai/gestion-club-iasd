from django.urls import reverse
from django.db import models
from club.models import Miembro
from django.db.models import Sum
import uuid


class CuentaContable(models.Model):
    cuenta = models.CharField(max_length=25)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f'{self.cuenta }'


class Concepto(models.Model):
    concepto = models.CharField(max_length=25)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f'{self.concepto}'


class Entrada(models.Model):
    folio = models.CharField(max_length=8, blank=True)
    fecha_pago = models.DateField()
    de = models.ForeignKey(
        Miembro,
        on_delete=models.PROTECT,
    )
    notas = models.TextField(blank=True)

    # class Meta:
    #     ordering = ['fecha_pago', 'id']

    def __str__(self):
        return f'{self.id} - {self.de} por: ${self.total_importe}'

    def get_absolute_url(self):
        return reverse('entrada-detail', kwargs={'pk': self.pk})

    @property
    def mes_pago(self):
        return self.fecha_pago.month

    @property
    def anio_pago(self):
        return self.fecha_pago.year

    @property
    def total_importe(self):
        return ConceptoEntrada.objects.filter(entrada=self).aggregate(Sum('importe'))['importe__sum']

    @property
    def conceptos(self):
        return ', '.join(ConceptoEntrada.objects.filter(entrada=self).values_list('concepto__concepto', flat=True))

    @property
    def cuentacontables(self):
        return ', '.join(ConceptoEntrada.objects.filter(entrada=self).values_list('cuenta_contable__cuenta', flat=True))


class ConceptoEntrada(models.Model):
    entrada = models.ForeignKey(
        Entrada,
        on_delete=models.CASCADE,
    )
    miembro = models.ForeignKey(
        Miembro,
        on_delete=models.PROTECT
    )
    concepto = models.ForeignKey(
        Concepto,
        on_delete=models.PROTECT,
    )
    cuenta_contable = models.ForeignKey(
        CuentaContable,
        on_delete=models.CASCADE,
    )
    importe = models.FloatField()

    def __str__(self):
        return f'pago para {self.miembro} por {self.concepto} por {self.importe}'


class Salida(models.Model):
    folio = models.CharField(max_length=30, blank=True)
    fecha_pago = models.DateField()
    de = models.ForeignKey(
        Miembro,
        on_delete=models.PROTECT,
    )
    proveedor = models.CharField(
        max_length=100
    )
    notas = models.TextField(blank=True)

    # class Meta:
    #     ordering = ['fecha_pago', 'proveedor']

    def get_absolute_url(self):
        return reverse('salida-detail', kwargs={'pk': self.pk})

    @property
    def mes_pago(self):
        return self.fecha_pago.month

    @property
    def anio_pago(self):
        return self.fecha_pago.year

    @property
    def total_importe(self):
        return ConceptoSalida.objects.filter(salida=self).aggregate(Sum('importe'))['importe__sum']

    @property
    def conceptos(self):
        return ', '.join(ConceptoSalida.objects.filter(salida=self).values_list('concepto', flat=True))

    @property
    def cuentacontables(self):
        return ', '.join(ConceptoSalida.objects.filter(salida=self).values_list('cuenta_contable__cuenta', flat=True))


class ConceptoSalida(models.Model):
    salida = models.ForeignKey(
        Salida,
        on_delete=models.PROTECT,
    )
    concepto = models.CharField(max_length=100)
    cuenta_contable = models.ForeignKey(
        CuentaContable,
        on_delete=models.CASCADE,
    )
    importe = models.FloatField()

    def __str__(self):
        return f'{self.concepto} ${self.importe}'
