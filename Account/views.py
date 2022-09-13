from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
import re   



# --- load SignUp page - Default url ---
# Create your views here.
def loadSignUpPage(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        profile_image=request.FILES['profile_image']
        term = request.POST.get('term')
        state=State.objects.get(id=request.POST['state'])
        city = request.POST.get('city')

        password_pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")
        mobile_pattern= re.compile("[6-9][0-9]{9}")


        if User.objects.filter(username=email):
            messages.error(request, f"{email} is already taken.")
            return redirect('/sign-up')
        elif User.objects.filter(email=email):
            messages.error(request, f"{email} is already taken.")
            return redirect('/sign-up')
        elif UserProfile.objects.filter(phone_number=phone_number):
            messages.error(request, f"{phone_number} is already taken.")
            return redirect('/sign-up')
        else:
            if term != None:
                if mobile_pattern.match(phone_number):
                    if len(password)>8 and re.search(password_pattern,password):
                        userobj=User.objects.create_user(first_name=first_name, last_name=last_name,username=email, email=email, password=password)
                        usertypeobj=UserType.objects.create(user_id=userobj)
                        UserProfile.objects.create(usertype=usertypeobj,phone_number=phone_number,profile_image=profile_image,terms_conditions=True,state=state,city=city)
                        user_obj=authenticate(username=email,password=password)
                        if user_obj is not None:
                            login(request, user_obj)
                            return redirect('/home-screen')
                        else:
                            return redirect('/')
                    else:
                        messages.error(request, f"Password length must be more than 8 character long and must contatin atleat one number,one uppercare,one lowercase and one special symbol ")
                        return redirect('/sign-up')
                else:
                    messages.error(request, f"Mobile is incorrect please enter you valid mobile number")
                    return redirect('/sign-up')
            else:
                print("Please Select terms and condition")
                return redirect('/sign-up')
            
    else:
        state=State.objects.all()
        context={'state':state}
        return render(request, 'account/sign-up.html', context)

# --- load SignUp for Profession page ---
def loadSignUpForProfession(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        experience = request.POST.get('experience')
        profession=request.POST['profession']
        start_time= request.POST.get('start_time')
        close_time= request.POST.get('end_time')
        password = request.POST.get('password')
        shop_name= request.POST.get('shop_name')
        if request.POST.get('sunday')!=None:
            sunday = True
        else:
            sunday=False
        if request.POST.get('monday')!=None:
            monday = True
        else:
            monday=False
        if request.POST.get('tuesday')!=None:
            tuesday = True
        else:
            tuesday=False
        if request.POST.get('wednesday')!=None:
            wednesday = True
        else:
            wednesday=False
        if request.POST.get('thrusday')!=None:
            thrusday = True
        else:
            thrusday=False
        if request.POST.get('friday')!=None:
            friday = True
        else:
            friday=False
        if request.POST.get('saturday')!=None:
            saturday = True
        else:
            saturday=False

        profile_image=request.FILES['profile_image']
        address= request.POST.get('address')
        state= State.objects.get(id=request.POST['state'])
        city=request.POST['city']
        about=request.POST['about']
        if request.POST.get('term')!=None:
            term = True
        else:
            term=False

        print(sunday,monday,tuesday )

        if User.objects.filter(username=email):
            print('Email Already exists.')
            return redirect('/sign-up-community')
        elif User.objects.filter(email=email):
            print('Email Already exists.')
            return redirect('/sign-up-community')
        elif UserProfile.objects.filter(phone_number=phone_number):
            print('Phone Number Already Taken')
            return redirect('/sign-up-community')
        else:
            if term != None:
                userobj=User.objects.create_user(first_name=first_name, last_name=last_name,username=email, email=email, password=password)
                usertypeobj=UserType.objects.create(user_id=userobj,user_type='Proffe User')
                UserProfile.objects.create(
                                            year_of_experience=experience, 
                                            profession=profession,
                                            usertype=usertypeobj,
                                            phone_number=phone_number,
                                            profile_image=profile_image,
                                            terms_conditions=True,
                                            shop_name=shop_name,
                                            shop_start_time=start_time,
                                            shop_close_time=close_time,
                                            shop_address=address,
                                            shop_state=state,
                                            shop_city=city,
                                            shop_status_sunday=sunday,
                                            shop_status_monday=monday,
                                            shop_status_Tuesday=tuesday,
                                            shop_status_Wednesday=wednesday,
                                            shop_status_Thrusday=thrusday,
                                            shop_status_Friday=friday,
                                            shop_status_saturday=saturday,
                                            shop_description=about,
                                            )

                return redirect('/')
            else:
                print("Please Select terms and condition")
                return redirect('/sign-up-community')
    else:
        state=State.objects.all()
        context={'state':state}
        return render(request, 'account/sign-up-for-profession.html',context)


def load_city(request):
    state_id = request.GET.get('state')
    city = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'account/loadcity.html', {'city': city})

# --- load SignIn page ---
def loadSignInPage(request):
  if request.user.is_authenticated:
    return redirect('/profession-profile-screen')
  else:
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if User.objects.filter(email=username):
            user=User.objects.get(email=username)
            user=authenticate(username=user.username,password=password)

            if user is not None:
                login(request, user)
                print('Login Successfully')
                return redirect('/home-screen')
            else:
                messages.error(request, f"Wrong Credetials")
                return redirect('/')
        elif UserProfile.objects.filter(phone_number=username):
            user=UserProfile.objects.get(phone_number=username)
            user=authenticate(username=user.usertype.user_id.username,password=password)

            if user is not None:
                login(request, user)
                print('Login Successfully')
                return redirect('/home-screen')
            else:
                messages.error(request, f"Wrong Credetials")
                return redirect('/')
        else:
            messages.error(request, f"Wrong Credetials")
            return redirect('/')

    else:
        return render(request, 'account/sign-in.html')

# --- load Forgot Password Page ---
def loadForgotPasswordPage(request):
    return render(request, 'account/forgot-password.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def professional_or_community(request):
    return render(request, 'account/professional-or-community.html')

def new_professonal_user(request):
    try:
     if request.method == 'POST':   
        user=request.user
        usertype=UserType.objects.get(user_id=user)
        print(usertype)
        usertype.user_type='Professional User'
        usertype.save()
        return redirect('/home-screen')
     else:
        return redirect('/professional_or_community')
    except:
        return HttpResponse("<h1>404 Error</h1>")

def new_community_user(request):
    try:
     if request.method == 'POST':
        user=request.user
        usertype=UserType.objects.get(user_id=user)
        usertype.user_type='Professional User'
        usertype.save()
        return redirect('/home-screen')
     else:
        return redirect('/professional_or_community')
    except:
        return HttpResponse("<h1>404 Error</h1>")