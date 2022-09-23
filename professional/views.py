from operator import add
from django.shortcuts import render, redirect
from Account.models import *
from community_profession.models import *
from.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
import re
from geopy.geocoders import ArcGIS

def userprofileobj(request):
    user=request.user
    try:
        Usertype=UserType.objects.get(user_id=user)
    except:
        usertypeobj=UserType.objects.create(user_id=user)
        UserProfile.objects.create(usertype=usertypeobj)

    Usertype=UserType.objects.get(user_id=user)
    Userprofile=UserProfile.objects.get(usertype=Usertype)
    joincommunityobj=Join_Community.objects.filter(User_profile=Userprofile)
    My_Community=Community.objects.all()
    obj = My_Community
    if len(joincommunityobj) > 0:
        for i in joincommunityobj:
            print(i)
            obj = obj.exclude(id=i.Commnunity_id.id)
    else:
        obj = None
    return Userprofile,joincommunityobj,obj,My_Community

# Create your views here.
def is_user_is_professional_user(request):
    user=request.user
    usertype=UserType.objects.get(user_id=user)
    if usertype.user_type=='Professional User':
        return True
    else:
        return False

@login_required(login_url='/')
def loadProfessionProfileScreen(request,id=None):
    # try:
        userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
        if id==None:
            profession=Profession.objects.filter(UserProfile=userprofile)
            state=State.objects.all()
            print(profession)
            if obj is not None:
                context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'profession':profession,"state":state,'loginuser':userprofile}
            else:
                context={'My_community':My_Community,'userprofile':userprofile,'profession':profession,"state":state,'loginuser':userprofile}
            return render(request, 'professional/profile-screen-for-profession.html',context)
        else:
            userobj=User.objects.get(id=id)
            usertypeobj=UserType.objects.get(user_id=userobj)
            userprofile1 = UserProfile.objects.get(usertype=usertypeobj)
            profession=Profession.objects.filter(UserProfile=userprofile1)

            if obj is not None:
                context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile1':userprofile1,'profession':profession,'userprofile':userprofile,}
            else:
                context={'My_community':My_Community,'userprofile1':userprofile1,'profession':profession,'userprofile':userprofile,}
            return render(request, 'professional/profile-screen-for-profession.html',context)
    # except:
    #     return HttpResponse("<h1>404 Data Not Found<h1>")

@login_required(login_url='/')
def update_details(request):
    # try:
        userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
        obj=request.user
        if request.method == "POST":
            obj.first_name=request.POST.get("first_name")
            obj.last_name=request.POST.get("last_name")
            
            mobile_pattern= re.compile("[6-9][0-9]{9}")
            if mobile_pattern.match(request.POST.get("phone_number")):
                userprofile.phone_number=request.POST.get("phone_number")
                print('yes')
            else:
                print("no")
            
            userprofile.state= State.objects.get(id=request.POST.get('state')).name
            print(State.objects.get(id=request.POST.get('state')))
            userprofile.city=request.POST.get("city")
            print()
            obj.save()
            userprofile.save()
            return redirect('/profession-profile-screen')
        else:
            return redirect('/profession-profile-screen')
    # except:
    #     return HttpResponse("<h1>404 Data Not Found<h1>")

@login_required(login_url='/')
def update_profile_image(request):
    # try:
        userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
        if request.method == "POST":
            profile_image=request.FILES['profile_image']
            userprofile.profile_image=profile_image
            userprofile.save()
            return redirect('/profession-profile-screen')
        else:
            return redirect('/profession-profile-screen')
    # except:
    #     return HttpResponse("<h1>404 Data Not Found<h1>")

def add_profession(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    
   

    if request.method == 'POST':
        experience = request.POST.get('experience')
        profession=request.POST['profession']
        Profession_obj=Admin_Profession.objects.get(id=profession)
        start_time= request.POST.get('start_time')
        close_time= request.POST.get('end_time')
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

        profession_image=request.FILES['profession_image']
        address= request.POST.get('address')
        state= State.objects.get(id=request.POST['state'])
        city=request.POST['city']
        about=request.POST['about']

        
        nom=ArcGIS()
        Location=address+' '+city+' '+state.name
        
       
        latitude=nom.geocode(Location).latitude
        long=nom.geocode(Location).longitude

        print(latitude,long)

        Profession.objects.create(          UserProfile=userprofile,
                                            year_of_experience=experience, 
                                            profession=Profession_obj,
                                            profession_image=profession_image,
                                            
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
                                            profession_longitude=long,
                                            profession_latitude=latitude
                                            )
        return redirect('/profession-profile-screen')
    
    else:
        Profession_obj=Admin_Profession.objects.all()
        # My_Community=Community.objects.all()
        state=State.objects.all()
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'profession':Profession_obj,'state':state}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,'profession':Profession_obj,'state':state}
            # context={'state':state}
        return render(request, 'professional/add-profession.html',context)
    
def profession_details(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    profession=Profession.objects.get(id=id)
    services=ProfessionServices.objects.filter(Profession=profession)
    profession_image=Professionimage.objects.filter(profession=profession)[:4]
    profession_video=Professionvideo.objects.filter(profession=profession)[:2]
    profession_review=ProfessionReview.objects.filter(Profession=profession)
    profession_review_count=ProfessionReview.objects.filter(Profession=profession).count()

    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'profession':profession,'services':services,'profession_image':profession_image,"profession_video":profession_video,"profession_review":profession_review,"profession_review_count":profession_review_count}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,'profession':profession,'services':services,'profession_image':profession_image,"profession_video":profession_video,"profession_review":profession_review,"profession_review_count":profession_review_count}
    # context={'profession' : profession,'services':services,'profession_image':profession_image,"My_community":My_Community}
    return render(request, 'professional/profession-details.html', context)


def add_services(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method == 'POST':
        service_name= request.POST.get('service_name')
        price= request.POST.get('price')
        prof_id=request.POST.get('profession_id')
        profession_obj= Profession.objects.get(id=prof_id)
        ProfessionServices.objects.create(Profession=profession_obj,service_name=service_name,service_price=price)
        return redirect(f'/profession_details/{prof_id}')
    else:
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile}
        else:
            context={'My_community':My_Community,'userprofile':userprofile}
        return redirect('/profession-profile-screen',context)
        
def update_profession_details(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=='POST':
        name=request.POST.get('name')
        address=request.POST.get('address')
        experience= request.POST.get('experiance')
        about = request.POST['about']

        profession_obj=Profession.objects.get(id=id)
        profession_obj.shop_name=name
        profession_obj.shop_address=address
        profession_obj.year_of_experience=experience
        profession_obj.shop_description=about

        profession_obj.save()

        return redirect(f'/profession_details/{id}')
    else:
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile}
        else:
            context={'My_community':My_Community,'userprofile':userprofile}
        return redirect('/profession-profile-screen',context)

def Days_details(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    profession=Profession.objects.get(id=id)
    print(profession)
    if request.method=="POST":
        
        
        if request.POST.get('start_time')  != '':
            profession.shop_start_time = request.POST.get('start_time')
        else:
            pass
        if request.POST.get('end_time')  != '':
            profession.shop_close_time = request.POST.get('end_time')
        else:
            pass
        
       
        if request.POST.get('sunday')!=None:
            profession.shop_status_sunday = True
        else:
            profession.shop_status_sunday = False
        if request.POST.get('monday')!=None:
            profession.shop_status_monday = True
        else:
            profession.shop_status_monday = False
        if request.POST.get('tuesday')!=None:
            profession.shop_status_Tuesday = True
        else:
            profession.shop_status_Tuesday = False
        if request.POST.get('wednesday')!=None:
            profession.shop_status_Wednesday = True
        else:
            profession.shop_status_Wednesday = False
        if request.POST.get('thrusday')!=None:
            profession.shop_status_Thrusday = True
        else:
            profession.shop_status_Thrusday = False
        if request.POST.get('friday')!=None:
            profession.shop_status_Friday = True
        else:
            profession.shop_status_Friday = False
        if request.POST.get('saturday')!=None:
            profession.shop_status_saturday = True
        else:
            profession.shop_status_saturday = False
        profession.save()
        return redirect(f"/profession_details/{id}")
    else:
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'profession':profession}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,'profession':profession}
        return render(request, 'professional/profession-details.html', context)

def edit_profession_image(request,id):
    if request.method=='POST':
        profession_image=request.FILES['profession_image']
        profession_obj=Profession.objects.get(id=id)
        profession_obj.profession_image=profession_image
        profession_obj.save()
        return redirect(f'/profession_details/{id}')
    else:
        return redirect('/profession-profile-screen')

def delete_service(request,id):
    profession_id=request.GET['profession_id']
    ProfessionServices.objects.get(id=id).delete()
    return redirect(f'/profession_details/{profession_id}')

def add_profesion_gallery(request):
    if request.method == 'POST':
        image= request.FILES['image']
        profession_id=request.POST['profession_id']
        profession_obj=Profession.objects.get(id=profession_id)
        Professionimage.objects.create(image=image,profession=profession_obj)
        return redirect(f'/profession_details/{profession_id}')
    else:
        return redirect('/profession-profile-screen')

def add_profesion_video(request):
    if request.method == 'POST':
        video= request.FILES['video']
        profession_id=request.POST['profession_id']
        profession_obj=Profession.objects.get(id=profession_id)
        Professionvideo.objects.create(video=video,profession=profession_obj)
        return redirect(f'/profession_details/{profession_id}')
    else:
        return redirect('/profession-profile-screen')

def loadSeeAllPhotosAndVideos(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    profession=Profession.objects.get(id=id)
    profession_image=Professionimage.objects.filter(profession=profession)
    profession_video=Professionvideo.objects.filter(profession=profession)
    # print(profession_image)
    # My_Community=Community.objects.all()
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'profession':profession,'profession_image':profession_image,"profession_video":profession_video}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,'profession':profession,'profession_image':profession_image,"profession_video":profession_video}
    # context={'profession' : profession,'profession_image':profession_image,"My_community":My_Community,}
    return render(request, 'professional/see-all-photos-and-videos.html',context)

# -- whatsapp functionality --
def update_whatsapp_number(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method == 'POST':
        userprofile.country_code="91"
        mobile_pattern= re.compile("[6-9][0-9]{9}")
        if mobile_pattern.match(request.POST.get('whatsapp_number')):
            userprofile.whatsapp_number=request.POST.get('whatsapp_number')
            print('yes')
        else:
            print("no")
        # whatsapp_number= request.POST.get('whatsapp_number')
        # userprofile.whatsapp_number=whatsapp_number
        userprofile.save()
        return redirect('/profession-profile-screen')

def delete_Image(request,id):
    profession_id=request.GET['profession']
    Image=Professionimage.objects.get(id=id)
    Image.delete()
    return redirect(f'/profession_details/{profession_id}')

def delete_Video(request,id):
    profession_id=request.GET['profession']
    Video=Professionvideo.objects.get(id=id)
    Video.delete()
    return redirect(f'/profession_details/{profession_id}')

def delete_Profession(request,id):
    profession=Profession.objects.get(id=id)
    profession.delete()
    return redirect("profession-profile-screen")

def like_Review(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        profession_id=request.POST.get("post_id")
        print(profession_id)
        Profession_Review=ProfessionReview.objects.get(id=profession_id)
        if userprofile in Profession_Review.like.all():
            Profession_Review.like.remove(userprofile)
        else:
            Profession_Review.like.add(userprofile)
        like, created=Review_Like.objects.get_or_create(user_profile=userprofile,Profession_Review=Profession_Review)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()
        data={
            'value':like.value,
            'post': Profession_Review.like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(f"/profession-personal-details/{Profession_Review.Profession.id}")

def edit_service(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Service=ProfessionServices.objects.get(id=id)
    print(Service)
    if request.method=="POST":
        Service.service_name=request.POST.get("service_name")
        Service.service_price=request.POST.get("price")
        Service.save()
        return redirect(f"/profession_details/{Service.Profession.id}")
    else:
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"Service":Service}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,"Service":Service}
        return render(request, "professional/edit-service.html", context)