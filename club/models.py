from django.db import models
from django.urls import reverse
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TipoMiembro(models.Model):
    descripcion = models.CharField(max_length=100)


class ClaseMiembro(models.Model):
    descripcion = models.CharField(max_length=100)


class Miembro(models.Model):
    # CHOICES Sexo
    SEXO_M = 'M'
    SEXO_F = 'F'
    SEXO_CHOICES = (
        (SEXO_M, 'Masculino'),
        (SEXO_F, 'Femenino'),
    )

    # Datos de la persona
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(choices=SEXO_CHOICES, max_length=1)

    # Datos del club
    tipo_miembro = models.ForeignKey(
        TipoMiembro,
        on_delete=models.PROTECT)
    clase = models.ForeignKey(
        ClaseMiembro,
        on_delete=models.PROTECT)
    miembro_iglesia = models.BooleanField(default=True,
                                          verbose_name='¿Es miembro de la Iglesia Adventista del Séptimo Día?')

    class Meta:
        ordering = ['nombre', 'clase']
        verbose_name = 'miembro'
        verbose_name_plural = 'miembros'

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno} - {self.get_tipo_miembro_display()}'

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('miembro-detail', kwargs={'pk': self.id})

    def get_absolute_url_update(self):
        """Returns the url to access a detail record for this cliente."""
        return reverse('miembro-update', args=[int(self.id)])

    @property
    def edad(self):
        # delta = datetime.now().date() - self.fecha_nacimiento
        # return delta

        # print(datetime.now().date())
        # print(self.fecha_nacimiento)
        # # delta = relativedelta.relativedelta(
        # #     datetime.now().date(), self.fecha_nacimiento)
        # return delta.days

        return relativedelta(datetime.now().date(), self.fecha_nacimiento).years

    @property
    def edad_por_anio(self):
        return datetime.now().date().year - self.fecha_nacimiento.year


class Familia(models.Model):
    nombre_familia = models.CharField(max_length=200)
    miembro = models.ManyToManyField(
        Miembro,
        blank=True,
    )

    def __str__(self):
        return f'Familia {self.nombre_familia}'

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('familia-detail', kwargs={'pk': self.id})
