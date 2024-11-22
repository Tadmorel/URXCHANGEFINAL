from django.shortcuts import render

# Create your views here.


# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.forms import SetPasswordForm
import google.generativeai as genai
import json
from django.utils import timezone
from django.shortcuts import redirect
from .forms import ProfileForm





import time

def model_configai ():
    genai.configure(api_key="AIzaSyCPeU450l8GdHiDNT30YOJ3HQzpN_cjY4E", )

    generation_config = {

        "temperature":0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1000,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=generation_config)
    return model

def llm_prompt_engineering(model,response):
    chat = model.start_chat(
        history = [

            {"role":"user",
            "parts":'''Vas a tomar la funcion de un analista de texto, 
             tu objetivo es analizar el sentimiento de la oracion que te voy a dar,
             el formato como me lo vas a responder es de la siguiente forma:
                "{"sentiment":"result"}"
            donde result sera la emocion y tiene 3 categorias, Buena, Mala y Regular segun sea el caso. En
            caso de que el texto no sea entendible, imprimir "No Aplica"'''  
             
             }
        ]
    )

    response = chat.send_message(response)
    return response.text


model = model_configai()




def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada. Puedes iniciar sesión ahora.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'main/login.html')

@login_required
def dashboard(request):
    user=request.user
    post_form = UniversityCreateForm ()
    rol = user.user_type
    data_context = {'user': request.user,'post_form':post_form}
    print(rol)
    if rol == 'collaborator':
        data_context['collab'] = True
        if request.method == 'POST':
           post_form = UniversityCreateForm(request.POST,request.FILES)
           if post_form.is_valid():
               post = post_form.save(commit=False)
               post.user = user
               post.save()
    universities= University.objects.all()
    data_context["universities"] = universities
            
    return render(request, 'main/dashboard.html',data_context)


def user_logout(request):
    logout(request)
    return redirect('login')
    

def university(request, university_id):
    user = request.user
    university = University.objects.filter(pk=university_id).first()
    post_form = PostForm()
    comment_form = CreateComment()
    rol = user.user_type
    #Solo posts activos
    posts = Posts.objects.filter(university=university_id, is_active = True)  
    university_posts = []
    #Filtro de valuaciones
    #filter_valuation = request.GET.get('filter', 'all')

    # Itera a través de los posts y sus comentarios

        # Contadores para valuaciones
    #total_buenas = Comments.objects.filter(post__university=university, valuation='Buena', is_active=True).count()
    #total_malas = Comments.objects.filter(post__university=university, valuation='Mala', is_active=True).count()
    #total_regulares = Comments.objects.filter(post__university=university, valuation='Regular', is_active=True).count()
    #posts = Posts.objects.filter(university=university_id, is_active=True)
    #university_posts = []
    for each_post in posts:
        comments_posts = Comments.objects.filter(post=each_post)
        university_posts.append(
            {'post': each_post, 'comments': comments_posts}
        )  
    data_context = {"university": university, "post_form": post_form, "posts": university_posts, "comment_form": comment_form}
    print(rol)
    if rol == 'collaborator':
        data_context['collab'] = True

    if request.method == 'POST':
        form_type = request.POST.get("validator")
        if form_type == "post" and rol == 'collaborator':
            data_context['collab'] = True
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                #redirect('university')
                post.user = user
                post.university = university
                post.save()
                return redirect('university', university_id=university_id)
                #redirect('university')
        elif form_type == "comment":
            comment_form = CreateComment(request.POST)
            post_id = request.POST.get("post_id")
            post = Posts.objects.get(pk=post_id)
            if comment_form.is_valid():
                content = request.POST.get("comment")
                print("aqui en el prompt")
                result = llm_prompt_engineering(model, content)
                print("sali del prompt")
                json_data = json.loads(result)
                sentiment = json_data["sentiment"]
 
                comment = comment_form.save(commit=False)
                comment.valuation = sentiment
                comment.post = post
                comment.usuario = request.user
                comment.save()
            else:
                print(comment_form.errors)
    return render(request, 'la_salle.html', data_context)


#Editar post

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)  # Obtener la publicación por su ID o lanzar 404 si no existe
    data_context = {'post': post}

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Pre-rellenar el formulario con los datos actuales
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            messages.success(request, 'Publicación actualizada con éxito.')
            return redirect('university', university_id=post.university.id)  # Redirigir a la página de la universidad
    else:
        form = PostForm(instance=post)  # Mostrar el formulario con los datos existentes

    data_context['form'] = form
    return render(request, 'edit_post.html', data_context)



#Eliminar post

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)  # Obtiene el post por su ID
    data_context = {'post': post}

    if request.method == "POST":
        if 'yes' in request.POST:
            post.is_active = False  # Desactiva el post sin eliminarlo
            post.save()
            messages.success(request, 'La publicación ha sido eliminada con éxito.')
            return redirect('university', university_id=post.university.id)  # Redirige a la universidad
        elif 'no' in request.POST:
            return redirect('university', university_id=post.university.id)  # Redirige sin desactivar

    return render(request, 'delete_post.html', data_context) 







#Recuperar contraseña

def password_recovery(request):
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            answer = form.cleaned_data['security_answer']
            
            try:
                user = CustomUser.objects.get(username=username)
                if user.security_answer == answer:
                    request.session['recovery_user_id'] = user.id
                    return redirect('reset_password')
                else:
                    messages.error(request, 'Respuesta de seguridad incorrecta.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
    else:
        form = PasswordRecoveryForm()

    return render(request, 'main/password_recovery.html', {'form': form})

def reset_password(request):
    user_id = request.session.get('recovery_user_id')
    if not user_id:
        return redirect('password_recovery')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña actualizada con éxito.')
            return redirect('login')
    else:
        form = SetPasswordForm(user)

    return render(request, 'main/reset_password.html', {'form': form})



#Delete Universisty
@login_required
def delete_university(request, university_id):
    university = University.objects.get(pk=university_id)
    data_context = {'university': university}
    
    if request.method == "POST":
        if 'yes' in request.POST:
            university.active = False  # Desactivar universidad
            university.deleted_date = timezone.now()  # Guardar la fecha de desactivación
            university.save()
            messages.success(request, 'Universidad desactivada con éxito.')
            return redirect('dashboard')  # Redirigir al dashboard u otra página
        elif 'no' in request.POST:
            return redirect('university', university_id=university_id)  # Regresar a la página de la universidad
    
    return render(request, 'delete_university.html', data_context)


#Editar Universidad
@login_required
def edit_university(request, university_id):
    university = get_object_or_404(University, pk=university_id)
    if request.method == 'POST':
        form = UniversityCreateForm(request.POST, request.FILES, instance=university)
        if form.is_valid():
            form.save()
            messages.success(request, 'Universidad actualizada con éxito.')
            return redirect('university', university_id=university.id)
    else:
        form = UniversityCreateForm(instance=university)
    
    return render(request, 'edit_university.html', {'form': form, 'university': university})



#Eliminar valuación
@login_required
def delete_valuation(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)  # Obtener el comentario por su ID
    user = request.user  # Obtener el usuario actual

    # Verificar si el usuario es colaborador
    if user.user_type != 'collaborator':
        messages.error(request, 'No tienes permiso para eliminar valuaciones.')
        return redirect('university', university_id=comment.post.university.id)

    if request.method == "POST":
        if 'yes' in request.POST:  # Si se confirma la acción
            comment.is_active = False  # Desactiva el comentario
            comment.save()
            messages.success(request, 'La valuación ha sido eliminada con éxito.')
            return redirect('university', university_id=comment.post.university.id)  # Redirige a la universidad
        elif 'no' in request.POST:
            return redirect('university', university_id=comment.post.university.id)  # Redirige sin desactivar

    return render(request, 'delete_valuation.html', {'comment': comment})



@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'main/profile.html', {'form': form})






def your_view(request):
    context = {
        'range_20': range(1, 21),  # Genera un rango del 1 al 20
        # otros contextos...
    }
    return render(request, 'tu_template.html', context)
