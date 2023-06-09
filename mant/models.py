from django.db import models

# Create your models here.
'''
    CRUD principales
'''
class Epp(models.Model):
    descripcion = models.CharField(max_length=255)
    
class Riesgos(models.Model):
    descripcion = models.CharField(max_length=255)
    
class Sistemas(models.Model):
    nombre = models.CharField(max_length=255)
    
class ModeloImplemento(models.Model):
    descripcion =  models.CharField(max_length=255)

class Labores(models.Model):
    nombre = models.CharField(max_length=255)
    detalle = models.CharField(max_length=255)
    promedio_horas = models.DecimalField(max_digits=8)

class Fallas(models.Model):
    nombre = models.CharField(max_length=255)
    obs = models.TextField(max_length=255)

'''
    CRUD Mantenimiento
'''