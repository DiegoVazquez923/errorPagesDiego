from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
#Falta importar el modelo
from .models import CustomUser
#Falta importar el serializador
from .serializers import CustomUserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

#Importaciones de envio de form a React
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#Importaciones para enviar correo y recuperación de contraseña
import secrets
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

#USER API
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    renderer_classes = [JSONRenderer]

    #Como le pongo seguridad?
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    #Sobreescribir el metodo para la obtención de permisos
    def get_permissions(self):
        if self.request.method in ['POST','PUT', 'DELETE']:
            # Checar si tenemos sesión 
            return [IsAuthenticated()]
        #Dar acceso a todo lo demas sin estar logueado
        return []

#Envio del Token (inicio de sesion) al Front
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#Envio del form de registro al Front
class CustomUserFormAPI(APIView):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        fields = {
            field: {
            'label': form[field].label,
            'input':form[field].field.widget.attrs,
            'type': form[field].field.widget.input_type,
            }
                for field in form.fields
        }
        return Response(fields)
    
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.data)
        
        if form.is_valid():
            user_data = form.cleaned_data
            print(user_data['control_number'])
            User = get_user_model()
            user = User.objects.create_user(
            email=user_data['email'],
            password=user_data['password1'],
            name=user_data['name'],
            surname=user_data['surname'],
            control_number=user_data['control_number'],
            age=user_data['age'],
            tel=user_data['tel'],
            )
            return Response({'message': 'Usuario creado con éxito'},status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Vista para generar el token y enviar correo con token
@csrf_exempt
def send_reset_email(request):
    if request.method == "POST":
        #LLega del request de React información del email del usuario que quiere restablecer la contraseña
        email = request.POST.get("email")
        #Busquemos al usuario porque puede ser que no exista en el sistema
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Generar un token aleatorio de 20 caracteres
            token = secrets.token_urlsafe(20)

            # Las siguientes 2 lineas guarda el token en la BD
            user.token = token
            user.save()

            # Queremos que desde el correo electronica exista un link que incluya el token para que desde gmail (u otro) el usuario pueda regresar al sistema
            # y cambie su conraseña (debemos revisar que el token sea igual al que esta la BD para ello)
            # Construir el enlace de recuperación, en este caso lo dejamos en localhost pero deberia cambiar en producción
            reset_link = f"http://localhost:5173/reset-password/{token}"

            #Envio de correo
            send_mail(
                subject="🔐 Recuperación de contraseña",
                message=f"Hola, usa este enlace para restablecer tu contraseña: {reset_link}",  # Texto plano (fallback)
                from_email="no-reply@errorpages.com",
                recipient_list=[email],
                fail_silently=False,
                html_message=f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #0066cc;">Recuperación de contraseña</h2>
                    <p>Hola,</p>
                    <p>Has solicitado restablecer tu contraseña. Para continuar, haz clic en el siguiente botón:</p>
                    <p>
                        <a href="{reset_link}" 
                        style="display: inline-block; padding: 10px 20px; background-color: #0066cc; color: #ffffff; 
                                text-decoration: none; font-weight: bold; border-radius: 5px;">
                            Restablecer contraseña
                        </a>
                    </p>
                    <p>O copia y pega este enlace en tu navegador:</p>
                    <p><a href="{reset_link}" style="color: #0066cc;">{reset_link}</a></p>
                    <p>Si no solicitaste este cambio, ignora este mensaje.</p>
                    <p>Saludos,<br>El equipo de ErrorPages</p>
                </body>
                </html>
                """
            )
            #Regresamos mensaje de exito a React
            return JsonResponse({"message": "Correo de recuperación enviado."}, status=200)
        #Regresamos mensaje de error a React
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


#Vista que verificara que el token del usuario sea correcto y realiza el cambio de contraseña
@csrf_exempt
def reset_password(request):
    #Llega información desde el front con react
    if request.method == "POST":
        token = request.POST.get("token")
        new_password = request.POST.get("password")
        #Buscamos al usuario por token (ya que deberia ser unico y debe ser correcto, si no nos estan hackeando 0_0)
        user = CustomUser.objects.filter(token=token).first()

        if user:
            user.password = make_password(new_password)  # Encripta la nueva contraseña
            user.token = None  # Eliminar el token después de usarlo
            user.save()

            #Envio de correo
            send_mail(
                subject="🔐 Recuperación de contraseña",
                message=f"Tu contraseña fue cambiada con exito!",  # Texto plano (fallback)
                from_email="no-reply@errorpages.com",
                recipient_list=[user.email],
                fail_silently=False,
                html_message=f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #0066cc;">¡Tu contraseña fue cambiada con exito!</h2>
                    <p>Hola,</p>
                    <p>Tu contraseña ha cambiado recientemente, haz clic en el siguiente botón para iniciar sesión:</p>
                    <p>
                        <a href="http://localhost:5173/login/" 
                        style="display: inline-block; padding: 10px 20px; background-color: #0066cc; color: #ffffff; 
                                text-decoration: none; font-weight: bold; border-radius: 5px;">
                            Iniciar sesión
                        </a>
                    </p>
                    <p>Si no solicitaste este cambio, Tu cuenta esta en peligro, ponte en contacto con admin@errorpages.com.</p>
                    <p>Saludos,<br>El equipo de ErrorPages</p>
                </body>
                </html>
                """
            )

            return JsonResponse({"message": "Contraseña restablecida exitosamente."})
        return JsonResponse({"error": "Token inválido"}, status=400)
