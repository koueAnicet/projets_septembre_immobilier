
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from authentication import forms
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text



from immobilier import settings
from .tokens import generate_token
from authentication.forms import User


def logout_user_auth(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('home')


   
class  RegisterView(View):
    template_name = "authentication/pages/register.html" 
    class_form = forms.FormRegister 
    
    def get(self, request):
    
        form = self.class_form()
        messages.success(request, "Merci de bien vouloir vous inscris!")
        
        return render(request, self.template_name, locals())
    
    def post(self, request):
        form = self.class_form(request.POST)
        
        if form.is_valid():
            
            form.is_active = False
            print('##########')
            print(form.is_active)
            user = form.save()
            
            login(request, user)
            messages.success(request, "Votre compte a été créé avec success! Nous vous avons envoyez un email de confirmation,veuillez le confirmé")
            
            #Email de bienvenu
            
            subject = "Bienvenue sur GARO ESTATE!!"
            message = "Hello "+ user.first_name + "!!\n" + "Bienvenue à GARO ESTATE!!\n Merci pour la visite sur notre site web\n Nous t'avons envoyé un email de confirmation, s'il vous plait confirmez votre adresse email afin d'activer votre compte.\n\n Nous vous remercions\n GARO ESTATE TEAM\n"
            from_email = settings.EMAIL_HOST_USER
            to_list =[user.email]#on peu envoyer a plusier personne
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            
            #confirmation d'email
            
            current_site = get_current_site(request)
            email_subject = "Confirmation de l'email " + user.email + "GARO ESTATE - Django Login!!"
            message2 = render_to_string('authentication/pages/email_confirmation.html',{
                'name' : user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = False
            email.send()
            print('##########@') 
            print(email)
            
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, locals())
    
    
class  LoginView(View):
    template_name = "authentication/pages/login.html" 
    class_form = forms.LoginForm
    
    
    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, locals())
    
    #@method_decorator(login_required)
    def post(self, request):
        form = self.class_form(request.POST)
        
        if form.is_valid():
            #recuperation des infos
            user= authenticate(request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                if user.is_estate_agent and user.is_active != False:
                    
                    login(request, user)
                    fname = user.username
                    messages.success(request, "Bienvenue  d'être connecté.")
                    
                    return redirect('user-property')
                elif user and user.is_superuser:
                    login(request, user)
                    fname = user.get_full_name
                  
                    #messages.success(request, "f Bonjour {fname}! Merci d'avoir d'être connecté.")
                    return redirect('user-property')
                
                else:
                    messages.error(request, "Votre adresse email doit être confirmer avant de vous connecter, merci!")
                    
                    return render(request, self.template_name, locals())
        messages.error(request, "Utilisateur introuvable.")
        return render(request, self.template_name, context={'form': form})


class ContactView(View):
    template_name ="web/pages/contat.html"
    class_form = 'Contact'
    
    def get(self, request):
        
        return render(request, self.template_name , locals())


def user_profiles(request):
    return render(request, "authentication/pages/user-profile.html", locals())

@login_required
def submit_property(request):
   
    return render(request, "authentication/pages/submit-property.html", locals())


def user_property(request):
    template_name = "authentication/pages/user-properties.html"
    return render(request, 'authentication/pages/user-properties.html', locals())


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk=uid)
    except (TypeError,ValueError, OverflowError, User.DoesNotExist):
        user= None
        
    if user is not None and generate_token.check_token(user, token):
        user.is_active =True
        user.save()
        messages.success(request, "Votre a été activé , félicitaion!! connectez maintenant.")
        #login(request, user)
        return redirect('login')
    else:
        #messages.error(request, " Ooop, activation a échoué !!!!")
        return render(request, 'authentication/pages/activation_echoue.html', locals())