from django.db import models

# Create your models here.
class Zone(models.Model):
    code = models.CharField(max_length=2, verbose_name="Código")
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return f'{self.name}'

class Line(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="Zona")
    code = models.CharField(max_length=2, verbose_name="Código", default="LN")
    
    def __str__(self):
        return f'{self.zone.code + self.code + self.pk}'

class Level(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, verbose_name="Línea")
    code = models.CharField(max_length=2, verbose_name="Código", default="NV")

    def __str__(self):
        return f'{self.line.__str__ + self.code + self.pk}'

class Location(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Nivel")
    code = models.CharField(max_length=2, verbose_name="Código", default="UB")
    
    def __str__(self):
        return f'{self.level.__str__ + self.code + self.pk}'

class Position(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Ubicación")
    code = models.CharField(max_length=2, verbose_name="Código", default="PO")
    description = models.TextField(verbose_name="Descripción", default="")
    
    def __str__(self):
        return f'{self.location.__str__ + self.code + self.pk}'