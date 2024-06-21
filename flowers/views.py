from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from wtforms import ValidationError
from .models import FlowerProducts

# Create your views here.
def home(request):
    products = FlowerProducts.objects.all()
    return render(request, 'flowers/flowersweb.html', {
        'products': products
    })

def cart(request):
    return render(request, 'flowers/cart.html', {})

@csrf_exempt
def signup_api(request):  
    if request.method == 'POST':
        try:
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['pass1']
            confirm_pass = request.POST['pass2']
                         
            if User.objects.filter(username = username).exists():
                return JsonResponse({'error': "This UserName is already exists."}, status=400)
            
            if len(username) > 30:
                return JsonResponse({'error': "this UserName mustbe below 30 charecters."}, status=400)
            
            required_fields = ['username','firstname', 'lastname', 'email', 'pass1', 'pass2']
            for field in required_fields:
                if len(request.POST[field]) == 0 :
                    return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
                         
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Enter a valid Email Address'}, status=400)

            users_with_email = User.objects.filter(email=email)
            if users_with_email.exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            if (len(password)< 6 or len(password)> 16) :
                return JsonResponse({'error': 'Password need min 6 charecters and max 16 charecters.'}, status=400)
            else:
                pass

            if not password == confirm_pass:
                return JsonResponse({'error': 'Password and Confirm passwords are not same'}, status = 400)

            newUser = User.objects.create_user(username, email, password)
            newUser.first_name = firstname
            newUser.last_name = lastname
            newUser.save()
            
            JsonResponse({"Success": "Your Account has been Successfully Created."}, status = 201)
            return redirect('login')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400)
    return render(request, 'flowers/signup.html')
    
@csrf_exempt    
def login_api(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        try:
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request, user)
                firstname = user.first_name
                return render(request, 'flowers/home.html', {'fname': firstname})   
            else:
                return JsonResponse({"error": "Username or password is not valid"}, status=400)
        except Exception as e:
                return JsonResponse({"error": str(e)}, status = 400)

    return render(request, 'flowers/login.html')

def signout_api(request):
    logout(request)
    return redirect('home')

