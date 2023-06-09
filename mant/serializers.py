from rest_framework import exceptions, serializers, status
from mant.models import Epp, Riesgos, Sistemas, ModeloImplemento, Labores, Fallas

class EppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epp
        fields = '__all__'
        
class RiesgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riesgos
        fields = '__all__'
        managed = True
        verbose_name = ''
        verbose_name_plural = 'rgs'
        
class SistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sistemas
        fields = '__all__'
        managed = True
        verbose_name = ''
        verbose_name_plural = 'sis'
        
class ModImpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloImplemento
        fields = '__all__'
        managed = True
        verbose_name = ''
        verbose_name_plural = 'mi'

class LaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labores
        fields = '__all__'
        managed = True
        verbose_name = ''
        verbose_name_plural = 'la'

class FallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fallas
        fields = '__all__'
        managed = True
        verbose_name = ''
        verbose_name_plural = 'fa'