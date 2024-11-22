# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from . import models
from .models import Posts
from django.contrib.auth import get_user_model


class UserRegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('student', 'Estudiante'),
        ('collaborator', 'Colaborador'),
    )
#Pregunta de seguridad
    SECURITY_QUESTIONS = (
        ('birth_city', '¿En qué ciudad naciste?'),
        ('pet_name', '¿Cuál fue el nombre de tu primera mascota?'),
        ('school_name', '¿Cómo se llamaba tu escuela primaria?'),
    )

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Email')
    country = forms.CharField(max_length=100, required=False, label='País')
    university = forms.CharField(max_length=200, required=False, label='Universidad')

 # Pregunta y respuesta de seguridad
    security_question = forms.ChoiceField(choices=SECURITY_QUESTIONS, label="Pregunta de seguridad", required=True)
    security_answer = forms.CharField(max_length=200, label="Respuesta de seguridad", required=True)



    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'country', 'university', 'security_question','security_answer', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'student':
            if not cleaned_data.get('country'):
                self.add_error('country', 'Este campo es requerido para estudiantes.')
            if not cleaned_data.get('university'):
                self.add_error('university', 'Este campo es requerido para estudiantes.')
        elif user_type == 'collaborator':
            # Para colaboradores, solo se requiere la universidad
            if not cleaned_data.get('university'):
                self.add_error('university', 'Este campo es requerido para colaboradores.')
        return cleaned_data
    

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Posts
        fields=['title','type','description','direccion','precio','cuartos','banos','descripcion','foto']


    



class UniversityCreateForm(forms.ModelForm):
    class Meta:
        model = models.University
        fields = ['nombre_uni','direccion','contacto','tipo','logo']


class PasswordRecoveryForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    security_answer = forms.CharField(max_length=200, label="Respuesta de seguridad", widget=forms.PasswordInput)


class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comments
        fields = ['comment',"post","usuario","valuation"]


    

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']  # Excluye el correo electrónico
        help_texts = {
            'username':None,
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username