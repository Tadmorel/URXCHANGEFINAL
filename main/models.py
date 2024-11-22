from django.db import models

# Create your models here.


# main/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Estudiante'),
        ('collaborator', 'Colaborador'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Campos adicionales para Estudiantes
    country = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=200, blank=True, null=True)

     # Pregunta y respuesta de seguridad
    security_question = models.CharField(max_length=200, blank=True, null=True)
    security_answer = models.CharField(max_length=200, blank=True, null=True)

    
    def __str__(self):
        return self.username

class University(models.Model):
    nombre_uni = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=50)
    tipo = models.CharField(max_length=4 ,choices=[("pub","publica"),("priv","privada")])
    logo = models.ImageField(upload_to="")
    active = models.BooleanField(default=True)  # Campo para desactivar la universidad
    deleted_date = models.DateTimeField(null=True, blank=True)  # Campo para guardar la fecha de desactivación



class Posts(models.Model):
    type_choices = [("bancos","bancos"),("seguridad","seguridad"),("comida","comida"),("consejos","consejos"),("alojamiento","alojamiento"),("otros","otros")]
    title = models.CharField(max_length=50) #Buscar tipos de campos que hay y sus caracteristicas
    type = models.CharField(max_length=15, choices=type_choices, default="bancos")
    description = models.TextField(max_length=500) #Buscar lo que quiero de este dato
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100, blank=True, null=True) 
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cuartos = models.IntegerField(blank=True, null=True)
    banos = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    foto = models.ImageField(upload_to="alojamientos",blank=True, null=True)
    is_active = models.BooleanField(default=True) #Eliminar publicacion



    def __str__(self):
        return self.title
    


class Comments(models.Model):

    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)
    valuation = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Campo para "apagar" la valuación





    








