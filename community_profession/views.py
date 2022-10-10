from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from Account.models import *
from professional.models import *
from professional.views import is_user_is_professional_user
from datetime import date, datetime
from django.http import JsonResponse
import haversine as hs
from haversine import Unit

# Create your views here.

# --- load -- home screen -- for community and profession ---
 
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
            # print(i)
            obj = obj.exclude(id=i.Commnunity_id.id)
    else:
        obj = None
    return Userprofile,joincommunityobj,obj,My_Community

@login_required(login_url='/')
def loadHomeScreenPage(request):
    # print(request.user)
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    profession=Admin_Profession.objects.all()[:14]
    print("profession: ",profession)
    Popular_profession=Profession.objects.order_by("Profession_Rating")[:5][::-1]
    print("Popular_profession: ",Popular_profession)
    Recent_Serch_obj=Recent_serach.objects.filter(User_obj=userprofile)[::-1]
    print("Recent_Serch_obj:",Recent_Serch_obj)
    if obj is not None:
        context={ 'Popular_profession':Popular_profession, 'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"profession":profession,"Recent":Recent_Serch_obj}
    else:
        context={ 'Popular_profession':Popular_profession,  'My_community':My_Community,'userprofile':userprofile,"profession":profession,"Recent":Recent_Serch_obj}
    return render(request, 'community_profession/home-screen.html',context)

# --- load -- profession see all screen ---
@login_required(login_url='/')
def loadProfessionSeeAllScreen(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    profession=Admin_Profession.objects.all()
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"profession":profession}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,"profession":profession}
    return render(request, 'community_profession/profession-see-all.html',context)

# --- load -- search nearest professions list ---
@login_required(login_url='/')
def loadSearchNearestProfessions(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    profession=Admin_Profession.objects.get(id=id)
    state=State.objects.all()
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"profession":profession,'state':state}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,"profession":profession,'state':state}
    return render(request, 'community_profession/search-nearest-professions.html',context)

# --- load -- nearest profession list ---
@login_required(login_url='/')
def loadNearestProfessionsList(request,id=None):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        State_obj=State.objects.get(id=request.POST.get("state"))
        City_obj=request.POST.get("city")
        if State_obj!=None:
            Profession_obj=Profession.objects.filter(profession=id,shop_state=State_obj,shop_city=City_obj)
        else:
            Profession_obj=Profession.objects.filter(profession=id)
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"Profession_obj":Profession_obj}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,"Profession_obj":Profession_obj}
        return render(request, 'community_profession/nearest-professions-list.html',context)
    else:
        
        lat=float(request.GET['lat'])
        lon=float(request.GET['lon'])   
        loc1=(lat,lon)
        # print(loc1)
        pro_id= request.GET['id']

        Profession_obj=Profession.objects.filter(profession=pro_id)
        distance=dict()
        for i in Profession_obj:
            loc2=(i.profession_latitude,i.profession_longitude)
            # print(loc2)
            dis=round(hs.haversine(loc1,loc2,unit=Unit.KILOMETERS),2)
            if dis<1:
                dis=str(round(hs.haversine(loc1,loc2,unit=Unit.METERS),2))+' m'
            else:
                dis=str(dis)+' km'
            distance[i]=dis
           

        distance={k: v for k, v in sorted(distance.items(), key=lambda item: item[1])}
        # print(distance)
 
        
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile, "Profession_obj":Profession_obj, 'distance':distance}
        else:
            context={'joincommunityobj':joincommunityobj,"My_community":My_Community,'userprofile':userprofile, "Profession_obj":Profession_obj, 'distance':distance}

        return render(request, 'community_profession/nearest-professions-list.html',context)

from django.db.models import Avg
import json
# --- load -- profession personal details page ---
@login_required(login_url='/')
def loadProfessionPersonalDetails(request, id):
    userprofile, joincommunityobj, obj, My_Community = userprofileobj(request)
    Profession_obj = Profession.objects.get(id=id)
    # print(Profession_obj.id)
    Profession_service_obj = ProfessionServices.objects.filter(Profession=Profession_obj)
    Profession_Image_obj = Professionimage.objects.filter(profession=Profession_obj)[:3]
    Profession_Video_obj = Professionvideo.objects.filter(profession=Profession_obj)[:2]
    if Recent_serach.objects.filter(Profession_obj=Profession_obj, User_obj=userprofile):
        # print("The data is already exits")
        if request.method == "POST":
            review = request.POST.get("Comment")
            rate = request.POST.get("rating")

            print(request.POST)
            ProfessionReview.objects.create(Profession=Profession_obj, user_profile=userprofile, Review=review,
                                            Rate=rate)
            Rating = ProfessionReview.objects.aggregate(Avg('Rate'))
            Profession_obj.Profession_Rating = float(round(Rating['Rate__avg'], 1))
            Profession_obj.save()
            return redirect(f"/profession-personal-details/{id}")
        else:
            
            ProfessionReview_obj = ProfessionReview.objects.filter(Profession=Profession_obj)[::-1][0:3]
            ProfessionReview_obj_count = ProfessionReview.objects.filter(Profession=Profession_obj).count()

            if obj is not None:
                context = {'joincommunityobj': joincommunityobj, "My_community": obj, 'userprofile': userprofile,
                           "Profession_obj": Profession_obj, "Profession_service_obj": Profession_service_obj,
                           "Profession_Image_obj": Profession_Image_obj, "ProfessionReview_obj": ProfessionReview_obj,
                           "Profession_Video_obj": Profession_Video_obj,
                           "ProfessionReview_obj_count": ProfessionReview_obj_count}
            else:
                context = {'My_community': My_Community, 'userprofile': userprofile, "Profession_obj": Profession_obj,
                           "Profession_service_obj": Profession_service_obj,
                           "Profession_Image_obj": Profession_Image_obj, "ProfessionReview_obj": ProfessionReview_obj,
                           "Profession_Video_obj": Profession_Video_obj,
                           "ProfessionReview_obj_count": ProfessionReview_obj_count}
            return render(request, 'community_profession/profession-personal-details.html', context)
    else:
        Recent_serach.objects.create(Profession_obj=Profession_obj, User_obj=userprofile)
        if request.method == "POST":
            review = request.POST.get("Comment")
            rate = request.POST.get("rating")
            # print(review)
            ProfessionReview.objects.create(Profession=Profession_obj, User_Profile=userprofile, Review=review,
                                            Rate=rate)
            Rating = ProfessionReview.objects.aggregate(Avg('Rate'))
            # print(Profession_obj.Profession_Rating)
            Profession_obj.Profession_Rating = float(round(Rating['Rate__avg'], 1))
            Profession_obj.save()
            return redirect(f"/profession-personal-details/{id}")
        else:
            ProfessionReview_obj = ProfessionReview.objects.filter(Profession=Profession_obj)[::-1][0:3]
            
            ProfessionReview_obj_count = ProfessionReview.objects.filter(Profession=Profession_obj).count()

            if obj is not None:
                context = {'joincommunityobj': joincommunityobj, "My_community": obj, 'userprofile': userprofile,
                           "Profession_obj": Profession_obj, "Profession_service_obj": Profession_service_obj,
                           "Profession_Image_obj": Profession_Image_obj, "ProfessionReview_obj": ProfessionReview_obj,
                           "Profession_Video_obj": Profession_Video_obj,
                           "ProfessionReview_obj_count": ProfessionReview_obj_count}
            else:
                context = {'My_community': My_Community, 'userprofile': userprofile, "Profession_obj": Profession_obj,
                           "Profession_service_obj": Profession_service_obj,
                           "Profession_Image_obj": Profession_Image_obj, "ProfessionReview_obj": ProfessionReview_obj,
                           "Profession_Video_obj": Profession_Video_obj,
                           "ProfessionReview_obj_count": ProfessionReview_obj_count}
            return render(request, 'community_profession/profession-personal-details.html', context)

@login_required(login_url='/')
def review_Reply(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Profession_review=ProfessionReview.objects.get(id=id)
    # # print(Profession_review)
    # # print(Profession_review.id)
    if request.method=="POST":
        Reply=request.POST.get("reply")
        # # print(Reply)
        ProfessionReview_Reply.objects.create(Review=Profession_review,User_Profile=userprofile,Review_Reply=Reply)
        obj=ProfessionReview_Reply.objects.filter(Review=Profession_review)
        Profession_review.Reply=len(obj)
        Profession_review.save()
        return redirect(f"/review_Reply/{id}")
    else:
        Review_obj=ProfessionReview_Reply.objects.filter(Review=Profession_review)
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"Profession_review":Profession_review,"Review_obj":Review_obj}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,"Profession_review":Profession_review,"Review_obj":Review_obj}
        return render(request, 'community_profession/review-reply.html',context)

@login_required(login_url='/')
def like_post_comment(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        post_obj=request.POST.get("post_id")
        print(post_obj)
        post=Post_Commment.objects.get(id=post_obj)
        if userprofile in post.Comment_like.all():
            post.Comment_like.remove(userprofile)
        else:
            post.Comment_like.add(userprofile)
        like, created=Post_Comment_Like.objects.get_or_create(user_profile=userprofile,Post_comment=post)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()

        data={
            'value':like.value,
            'post': post.Comment_like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(f"/add_comment/{post.User_Post.id}")

@login_required(login_url='/')
def like_post(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        post_obj=request.POST.get("post_id")
        post=UserPost.objects.get(id=post_obj)
        print("yes")
        if userprofile in post.Like.all():
            post.Like.remove(userprofile)
        else:
            post.Like.add(userprofile)
        like, created=Like.objects.get_or_create(user_profile=userprofile,Post=post)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()

        data={
            'value':like.value,
            'post':post.Like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect("community-screen")

@login_required(login_url='/')
def like_Question(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        question_obj=request.POST.get("post_id")
        print(question_obj)
        Question=User_Question.objects.get(id=question_obj)
        print('yes')
        if userprofile in Question.Question_Like.all():
            Question.Question_Like.remove(userprofile)
        else:
            Question.Question_Like.add(userprofile)
        like, created=Question_Like.objects.get_or_create(user_profile=userprofile,Question=Question)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()
        data={
            'value':like.value,
            'post':Question.Question_Like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect("community-screen")

@login_required(login_url='/')
def like_Answer(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        answer_obj=request.POST.get("post_id")
        Answer=User_Answer.objects.get(id=answer_obj)
        if userprofile in Answer.Answer_Like.all():
            Answer.Answer_Like.remove(userprofile)
        else:
            Answer.Answer_Like.add(userprofile)
        like, created=Answer_Like.objects.get_or_create(user_profile=userprofile,Answer=Answer)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()
        data={
            'value':like.value,
            'post':Answer.Answer_Like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect(f"/Add_Answer/{Answer.Question.id}")

# --- load -- see all photos and videos of professions ---
@login_required(login_url='/')
def loadSeeAllPhotosAndVideos(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Profession_Image_obj=Professionimage.objects.filter(profession=id)
    Profession_video_obj=Professionvideo.objects.filter(profession=id)
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"Profession_Image_obj":Profession_Image_obj,"Profession_video_obj":Profession_video_obj}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,"Profession_Image_obj":Profession_Image_obj,"Profession_video_obj":Profession_video_obj}
    return render(request, 'community_profession/see-all-photos-and-videos.html',context)

# --- load -- photo screen ---
@login_required(login_url='/')
def loadPhotoScreen(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Profession_Image_obj=Professionimage.objects.get(id=id)
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"Profession_Image_obj":Profession_Image_obj}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,"Profession_Image_obj":Profession_Image_obj}
    return render(request, 'community_profession/photo-screen.html',context)

# --- load -- video screen ---
@login_required(login_url='/')
def loadVideoScreen(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Profession_video_obj=Professionvideo.objects.get(id=id)
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"Profession_video_obj":Profession_video_obj}
    else:
        context={'My_community':My_Community,'userprofile':userprofile,"Profession_video_obj":Profession_video_obj}
    return render(request, 'community_profession/video-screen.html',context)

# --- load -- user - profile screen ---
@login_required(login_url='/')
def loadUserProfileScreen(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if obj is not None:
        context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile}
    else:
        context={'My_community':My_Community,'userprofile':userprofile}
    return render(request, 'community_profession/profile-screen-for-users.html',context)

# --- load -- profession - profile screen ---

# --- load -- community - screen ---
@login_required(login_url='/')
def loadCommunityScreen(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Community_obj=POST_and_Question.objects.all()[::-1]
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    # User_POST_Question=POST_and_Question.objects.all()[::-1]
    # User_POST_Question_obj=POST_and_Question.objects.all()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)[::-1]
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    # # print(User_POST_Question_obj.Question)
    if obj is not None:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":Community_obj,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"Question":User_Question_obj}
    else:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":Community_obj,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"Question":User_Question_obj}
    return render(request, 'community_profession/community.html',context)

@login_required(login_url='/')
def Community_image(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()

    
    User_post_obj=UserPost.objects.filter(post_type1=False).exclude(User_Profile=userprofile)
    print(User_post_obj)
    for i in User_post_obj:
        User_post_obj_image=Community_Post.objects.filter(user_post=i.id)[::-1]

    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)[::-1]
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        # # print(User_POST_Question_obj.Question)
    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_post_obj_image":User_post_obj_image,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_post_obj_image":User_post_obj_image,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
    return render(request, 'community_profession/community.html',context)

@login_required(login_url='/')
def Community_video(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()

    User_post_video=UserPost.objects.filter(post_type1=True).exclude(User_Profile=userprofile)
    for i in User_post_video:
        User_post_obj_video = Community_Post.objects.filter(user_post=i.id)[::-1]

    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        # # print(User_POST_Question_obj.Question)
    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_post_obj_video":User_post_obj_video,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_post_obj_video":User_post_obj_video,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
    return render(request, 'community_profession/community.html',context)

# remaining
@login_required(login_url='/')
def Community_My_Video(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    
    User_post_obj_id=UserPost.objects.filter(User_Profile=userprofile,post_type1=True)
    print(User_post_obj_id)
    for i in User_post_obj_id:
        User_post_obj = Community_Post.objects.filter(user_post=i.id)[::-1]


    # User_POST_Question_obj=POST_and_Question.objects.all()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    # # print(User_POST_Question_obj.Question)
    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST_my_video":User_post_obj,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST_my_video":User_post_obj,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
    return render(request, 'community_profession/community.html',context)

@login_required(login_url='/')
def Community_Question(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()

    User_question=User_Question.objects.filter(User_id="Public").exclude(User_Profile=userprofile)
    # print(User_question)
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_question":User_question,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_question":User_question,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
    return render(request, 'community_profession/community.html',context)

@login_required(login_url='/')
def Community_My_Image(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()

    User_post_obj_id=UserPost.objects.filter(User_Profile=userprofile, post_type1=False)
    for i in User_post_obj_id:
        User_post_obj = Community_Post.objects.filter(user_post=i.id)[::-1]

    # User_POST_Question_obj=POST_and_Question.objects.all()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    # # print(User_POST_Question_obj.Question)
    # print('yes')
    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST_my_image":User_post_obj,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST_my_image":User_post_obj,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
    return render(request, 'community_profession/community.html',context)

@login_required(login_url='/')
def Community_My_Question(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    User_question=User_Question.objects.filter(User_Profile=userprofile)
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST_my_question":User_question,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST_my_question":User_question,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
    return render(request, 'community_profession/community.html',context)

@login_required(login_url='/')
def User_Post(request):
    if request.method=="POST":
        user=request.user
        User_type=UserType.objects.get(user_id=user)
        User_Profile_obj=UserProfile.objects.get(usertype=User_type)
        try:
            Post_Image=request.FILES["File"]
        except:
            Post_Image=None
        # print(Post_Image)
        # # print(type(str(Post_Image)))
        # # print(".jpg" in Post_Image)
        Describe=request.POST.get("description")
        Post_Date=date.today()
        now = datetime.now()
        Post_Time = now.strftime("%H:%M:%S")
        # # print(user)
        # # print(User_type)
        # # print(User_Profile_obj)
        # print('Post_Image : ',Post_Image)
        # # print('Describe : ',Describe)
        # # print('Post_Date : ',Post_Date)
        # # print('Post_Time : ',Post_Time)
        if Post_Image is not None and ('.mp4' in str(Post_Image) or '.mov' in str(Post_Image)):
            Post=UserPost(User_Profile=User_Profile_obj,Image=Post_Image,Description=Describe,Post_Date=Post_Date,Post_Time=Post_Time,post_type1=True)
        else:
             Post=UserPost(User_Profile=User_Profile_obj,Image=Post_Image,Description=Describe,Post_Date=Post_Date,Post_Time=Post_Time,post_type1=False)

        #
        Post.save()
        POST_and_Question.objects.create(Post=Post)
        return redirect("community-screen")
    else:
        return redirect("community-screen")

@login_required(login_url='/')
def add_comment(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Post_obj=UserPost.objects.get(id=id)
    if request.method=="POST":
        Comment=request.POST.get("comment")
        Comment_Date=date.today()
        now = datetime.now()
        comment_time = now.strftime("%H:%M:%S")
        Post_Commment.objects.create(User_Post=User_Post_obj,User_Profile=userprofile,Comment=Comment,Comment_Date=Comment_Date,Commenet_Time=comment_time)
        obj=Post_Commment.objects.filter(User_Post=User_Post_obj)
        # # print(len(obj))
        User_Post_obj.Post_comment=len(obj)
        User_Post_obj.save()
        return redirect(f"/add_comment/{id}")
    else:
        # # print(User_Post_obj)
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        All_Comment=Post_Commment.objects.filter(User_Post=User_Post_obj)[::-1]
        Comment_Count=Post_Commment.objects.filter(User_Post=User_Post_obj).count()
        # Post_reply=Comment_reply.objects.filter(Comment=All_Comment.id)
        # My_Community=Community.objects.all()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Date=date.today()
        Our_News_count=News.objects.filter(Date=Date).count()
        # print(User_Post_obj.Post_comment)
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,
            "Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,'User_Post_obj':User_Post_obj,
            "All_Comment":All_Comment,'Comment_Count':Comment_Count,}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,
            'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,'User_Post_obj':User_Post_obj,
            "All_Comment":All_Comment,'Comment_Count':Comment_Count,}
        #   context={"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'User_Post_obj':User_Post_obj,"All_Comment":All_Comment,'Comment_Count':Comment_Count,'My_community':My_Community,"Our_News_count":Our_News_count}
        return render(request, 'community_profession/add-comment.html',context)

@login_required(login_url='/')
def Post_comment_reply(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Post_obj=Post_Commment.objects.get(id=id)
    if request.method=="POST":
        Post_Reply=request.POST.get("reply")
        # print(Post_Reply)
        Post_Reply_Date=date.today()
        now = datetime.now()
        Post_Reply_Time = now.strftime("%H:%M:%S")
        Comment_reply.objects.create(Comment=Post_obj,User_Profile=userprofile,Reply=Post_Reply,Reply_Date=Post_Reply_Date,Reply_Time=Post_Reply_Time)
        obj=Comment_reply.objects.filter(Comment=Post_obj)
        Post_obj.Post_comment_reply=len(obj)
        Post_obj.save()
        return redirect(f"/Post_comment_reply/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        Reply=Comment_reply.objects.filter(Comment=Post_obj)
        # My_Community=Community.objects.all()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Date=date.today()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Our_News_count=News.objects.filter(Date=Date).count()
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,'Reply':Reply,"Post_obj":Post_obj}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,'Reply':Reply,"Post_obj":Post_obj}
        # context={"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"Post_obj":Post_obj,'Reply':Reply,'My_community':My_Community,"Our_News_count":Our_News_count}
        return render(request, 'community_profession/comment-reply.html',context)

@login_required(login_url='/')
def edit_reply(request,id):
    obj=Comment_reply.objects.get(id=id)
    if request.method=="POST":
        Reply=request.POST.get("reply")
        # print(review)
        obj.Reply=Reply
        obj.save()
        return redirect(f"/Post_comment_reply/{obj.Comment.id}")
    else:
        return redirect(f"/Post_comment_reply/{obj.Comment.id}")

@login_required(login_url='/')
def reply_delete(request, id):
    obj=Comment_reply.objects.get(id=id)
    obj1=obj.Comment.Post_comment_reply
    obj2=obj1-1
    obj.Comment.Post_comment_reply=obj2
    obj.Comment.save()
    obj.delete()
    return redirect(f"/Post_comment_reply/{obj.Comment.id}")

@login_required(login_url='/')
def Create_Community(request):
    if request.method=="POST":
        user=request.user
        User_type=UserType.objects.get(user_id=user)
        User_Profile_obj=UserProfile.objects.get(usertype=User_type)
        Community_name=request.POST.get("Communiy_Name")
        try:
            Community_image=request.FILES["Communiy_Image"]
        except:
            Community_image=None
        Community_profile=request.FILES["Communiy_Profile"]
        Community_Private=request.POST.get("private")
        Community_Restricted=request.POST.get("restricted")
        Community_Public=request.POST.get("public")
        Adult_content=request.POST.get("adult")
        community_description=request.POST.get("community_descrition")
        if Community_Public != None:
            Community_Public = True
        else:
            Community_Public = False
        if Community_Restricted != None:
            Community_Restricted = True
        else:
            Community_Restricted = False
        if Community_Private != None:
            Community_Private = True
        else:
            Community_Private = False
        if Adult_content != None:
            Adult_content = True
        else:
            Adult_content = False
        
        if Community.objects.filter(Community_Name=Community_name):
            # print("The Community Name Is Already exits")
            return redirect("community-screen")
        else:
            comunity_obj=Community.objects.create(
            User_Profile=User_Profile_obj,Community_Name=Community_name,
            Community_Cover_Image=Community_image, Public=Community_Public,
            Private=Community_Private,Restricted=Community_Restricted,
            Adult_Content=Adult_content,Community_Profile_Image=Community_profile,
            community_Description=community_description,
            )
            comunity_obj.save()
            Join_Community.objects.create(User_profile=User_Profile_obj,Commnunity_id=comunity_obj)
            return redirect("community-screen")
    else:
        return redirect("community-screen")

@login_required(login_url='/')
def Edit_Community(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    edit_coummunity=Community.objects.get(id=id)
    if request.method=="POST":
        edit_coummunity.Community_Name=request.POST.get("Communiy_Name")
        try:
            edit_coummunity.Community_Cover_Image=request.FILES["Communiy_Image"]
        except:
            pass
        try:
            edit_coummunity.Community_Profile_Image=request.FILES["Communiy_Profile"]
        except:
            pass
        edit_coummunity.community_Description=request.POST.get("description")
        edit_coummunity.save()
        return redirect(f"/community-profile-screen/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Date=date.today()
        Our_News_count=News.objects.filter(Date=Date).count()
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,"edit_coummunity":edit_coummunity,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"Our_News_count":Our_News_count}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,'My_community':My_Community,'userprofile':userprofile,"edit_coummunity":edit_coummunity,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"Our_News_count":Our_News_count}
        return render(request, 'community_profession/edit-community.html',context)

@login_required(login_url='/')
def Delete_Community(request,id):
    # # print(id)
    delete_obj=Community.objects.get(id=id)
    delete_obj.delete()
    return redirect("community-screen")

@login_required(login_url='/')
def Add_question(request):
    if request.method=="POST":
        user=request.user
        User_type=UserType.objects.get(user_id=user)
        User_Profile_obj=UserProfile.objects.get(usertype=User_type)
        Question_obj=request.POST.get("question")
        User_id=request.POST.get("UserId")
        # print(User_id)
        Question_Date=date.today()
        now = datetime.now()
        Question_Time = now.strftime("%H:%M:%S")
        # # print(Question_obj)
        if User_Question.objects.filter(Question=Question_obj):
            # print("The Question has Been exits")
            return redirect("community-screen")
        else:
            Question_add=User_Question(Date=Question_Date,Time=Question_Time,User_Profile=User_Profile_obj,Question=Question_obj,User_id=User_id)
            Question_add.save()
            if Question_add.User_id=="Public":
                POST_and_Question.objects.create(Question=Question_add)
                return redirect("community-screen")
            else:
                return redirect("community-screen")
    else:
        return redirect("community-screen")

@login_required(login_url='/')
def Add_Answer(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Question=User_Question.objects.get(id=id)
    if request.method=="POST":
        Answer_obj=request.POST.get("answer")
        Answer_Date=date.today()
        now = datetime.now()
        Answer_Time = now.strftime("%H:%M:%S")
        User_Answer.objects.create(Question=Question,User_Profile=userprofile,Answer=Answer_obj,Date=Answer_Date,Time=Answer_Time)
        obj=User_Answer.objects.filter(Question=Question)
        Question.answer=len(obj)
        Question.save()
        return redirect(f"/Add_Answer/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        Answer_id=User_Answer.objects.filter(Question=Question)[::-1]
        Answer_count=User_Answer.objects.filter(Question=Question).count()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Date=date.today()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Our_News_count=News.objects.filter(Date=Date).count()
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"count":Answer_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"i":Question,"user":userprofile,'Answer_id':Answer_id}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"count":Answer_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"i":Question,"user":userprofile,'Answer_id':Answer_id}
            # context={"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"i":Question,"user":userprofile,'Answer_id':Answer_id,'My_community':My_Community,"Our_News_count":Our_News_count}
        return render(request,'community_profession/add-answer.html',context)

@login_required(login_url='/')
def Add_Answer_Reply(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Answer=User_Answer.objects.get(id=id)
    if request.method=="POST":
        Reply_obj=request.POST.get("reply")
        reply_Date=date.today()
        now = datetime.now()
        reply_Time = now.strftime("%H:%M:%S")

        Answer_Reply.objects.create(Answer=Answer,User_Profile=userprofile,Reply=Reply_obj,Reply_date=reply_Date,Reply_Time=reply_Time)
        obj=Answer_Reply.objects.filter(Answer=Answer)
        Answer.reply=len(obj)
        Answer.save()
        return redirect(f"/Add_Answer_Reply/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        Answer_obj=Answer_Reply.objects.filter(Answer=Answer)
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Date=date.today()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Our_News_count=News.objects.filter(Date=Date).count()
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"Answer_obj":Answer,'Reply':Answer_obj,}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"Answer_obj":Answer,'Reply':Answer_obj,}
        return render(request, 'community_profession/answer-reply.html',context)

@login_required(login_url='/')
def Join_Coummunity(request,id):
    user=request.user
    User_type=UserType.objects.get(user_id=user)
    User_Profile_obj=UserProfile.objects.get(usertype=User_type)
    Our_Community=Community.objects.get(id=id)
    Communi_id=[]
    Communi_id.append(Our_Community.id)
    member_Count=Join_Community.objects.filter(Commnunity_id=Our_Community).count()
    Join=Join_Community(User_profile=User_Profile_obj,Commnunity_id=Our_Community)
    Our_Community.community_member=member_Count+1
    Our_Community.save()
    Join.save()
    member_Count=Join_Community.objects.filter(Commnunity_id=Our_Community).count()
    return redirect(f"/community-profile-screen/{id}")

# --- load -- community-answer - screen ---
@login_required(login_url='/')
def loadCommunityAnswerScreen(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]   #Show in Pop up
    User_Question_obj_id=User_Question.objects.filter(User_id=userprofile.id)[::-1]  #Show in screen
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count() #Show The Dedicated Question
    # My_Community=Community.objects.all()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    Date=date.today()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id) # show The in add question modal
    Our_News_count=News.objects.filter(Date=Date).count()

    # print(User_Question_obj_id)
    if obj is not None:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"Question_obj":User_Question_obj_id}
    else:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"Question_obj":User_Question_obj_id}
    return render(request, 'community_profession/community-answer.html',context)

# --- load --  users questions answer - screen ---
@login_required(login_url='/')
def loadCommunityUsersQuestionsAnswerScreen(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    Date=date.today()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Our_News_count=News.objects.filter(Date=Date).count()
    if obj is not None:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,}
    return render(request, 'community_profession/users-questions-answer.html',context)

# --- load -- normal user community screen ---
@login_required(login_url='/')
def loadNormalUserCommunityScreen(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    Date=date.today()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Our_News_count=News.objects.filter(Date=Date).count()
    if obj is not None:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
    else:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,}
    return render(request, 'community_profession/normal-user-community-screen.html',context)

# --- load -- community profile screen ---
@login_required(login_url='/')
def loadCommunityProfileScreen(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    # print(userprofile.id)
    Date=date.today()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    Our_News_count=News.objects.filter(Date=Date).count()
    community_obj=Community.objects.get(id=id)
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)

    if Join_Community.objects.filter(User_profile=userprofile,Commnunity_id=community_obj):
        z=Join_Community.objects.get(User_profile=userprofile,Commnunity_id=community_obj)
    else:
        z=None
    # print(z)
    Community_Post_obj=Community_Post.objects.filter(Community_obj=community_obj.id)[::-1]
    if obj is not None:
        context={'z':z,"Question":User_Question_obj,"Question_count":User_Question_count,         "Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"i":community_obj,"Community_Post_obj":Community_Post_obj,}
    else:
        context={'z':z,"Question":User_Question_obj,"Question_count":User_Question_count,    "Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"i":community_obj,"Community_Post_obj":Community_Post_obj,}
    return render(request, 'community_profession/community-profile-screen.html',context)

# --- load -- community create post page ---
@login_required(login_url='/')
def loadCommunityCreatePostPage(request, id=None):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if id==None:
        if request.method=="POST":
            community_obj=request.POST.get("CommunityId")
            Community_id=Community.objects.get(id=community_obj)
            try:
                Post_Image=request.FILES["File"]
            except:
                Post_Image=None
            Describe=request.POST.get("description")
            Post_Date=date.today()
            now = datetime.now()
            Post_Time = now.strftime("%H:%M:%S")

            if Post_Image is not None and ('.mp4' in str(Post_Image) or '.mov' in str(Post_Image)):
                obj1=UserPost.objects.create(User_Profile=userprofile,Image=Post_Image,Description=Describe,Post_Date=Post_Date,Post_Time=Post_Time,post_type1=True)
            else:
                obj1=UserPost.objects.create(User_Profile=userprofile,Image=Post_Image,Description=Describe,Post_Date=Post_Date,Post_Time=Post_Time,post_type1=False)

            post=Community_Post(Community_obj=Community_id,Community_type="Community",user_post=obj1)
            post.save()
            POST_and_Question.objects.create(Post=post)
            return redirect("community-screen")
        else:
            return redirect("community-screen")
    else:
        Community_obj=Community.objects.get(id=id)
        if request.method=="POST":
            try:
                Community_image=request.FILES["images"]
            except:
                Community_image=None
            Community_Description=request.POST.get("description")
            Community_Post_Date=date.today()
            now = datetime.now()
            Community_Post_time = now.strftime("%H:%M:%S")

            if Community_image is not None and ('.mp4' in str(Community_image) or '.mov' in str(Community_image)):
                obj=UserPost.objects.create(User_Profile=userprofile,Image=Community_image,Description=Community_Description,Post_Date=Community_Post_Date,Post_Time=Community_Post_time,post_type1=True)
            else:
                obj=UserPost.objects.create(User_Profile=userprofile,Image=Community_image,Description=Community_Description,Post_Date=Community_Post_Date,Post_Time=Community_Post_time,post_type1=False)
            
            # Community_Post.objects.create(Community_obj=Community_obj,Community_type="Community",user_post=obj)
            post=Community_Post(Community_obj=Community_obj,Community_type="Community",user_post=obj)
            post.save()
            POST_and_Question.objects.create(Post=post)
            return redirect(f"/community-profile-screen/{id}")
        else:
            Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
            Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
            # My_Community=Community.objects.all()
            User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
            User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
            Date=date.today()
            User_id=UserProfile.objects.all().exclude(id=userprofile.id)
            Our_News_count=News.objects.filter(Date=Date).count()
            if obj is not None:
                context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"i":Community_obj}
            else:
                context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"i":Community_obj}
            return render(request, 'community_profession/community-create-post-page.html',context)

# --- load -- write-comment-screen ---
@login_required(login_url='/')
def loadCommunityWriteCommentScreen(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)

    Community_obj=Community_Post.objects.get(id=id)
    if request.method=="POST":
        Post_Comment_obj=request.POST.get("Comment")
        Post_Date=date.today()
        now = datetime.now()
        Post_time = now.strftime("%H:%M:%S")
        Post_obj=Post_Commment.objects.create(User_Post=Community_obj.user_post,User_Profile=userprofile,Comment=Post_Comment_obj,Comment_Date=Post_Date,Commenet_Time=Post_time)
        
        obj=Post_Commment.objects.filter(User_Post=Community_obj.user_post)
        Community_obj.user_post.Post_comment=len(obj)
        Community_obj.user_post.save()
        
        Community_Post_Comment.objects.create(Community_Post_obj=Community_obj,Community_Comment=Post_obj)
        return redirect(f"/community-write-comment-screen/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        # print("Answer_later_obj : ",Answer_later_obj)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        # print("Answer_later_count : ", Answer_later_count)
        Date=date.today()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        # print("User_Question_obj : ",User_Question_obj)
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        # print("User_Question_count : ",User_Question_count)
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        # print("User_id : ",User_id)
        Our_News_count=News.objects.filter(Date=Date).count()
        All_comment=Community_Post_Comment.objects.filter(Community_Post_obj=Community_obj)[::-1]
        # print("All_comment : ",All_comment)
        All_comment_count=Community_Post_Comment.objects.filter(Community_Post_obj=Community_obj).count()
        # print("All_comment_count : ",All_comment_count)
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"i":Community_obj,"All_comment":All_comment,"count":All_comment_count}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"i":Community_obj,"All_comment":All_comment,"count":All_comment_count}
        return render(request, 'community_profession/write-comment-screen.html',context)

@login_required(login_url='/')
def edit_comment(request,id):
    obj=Community_Post_Comment.objects.get(id=id)
    if request.method=="POST":
        review=request.POST.get("Review")
        obj.Community_Comment.Comment=review
        obj.Community_Comment.save()
        return redirect(f"/community-write-comment-screen/{obj.Community_Post_obj.id}")
    else:
        return redirect(f"/community-write-comment-screen/{obj.Community_Post_obj.id}")

@login_required(login_url='/')
def comment_delete(request, id):
    obj=Community_Post_Comment.objects.get(id=id)
    print(obj)
    obj1=obj.Community_Comment.User_Post.Post_comment
    print(obj1)
    obj2=obj1-1
    obj.Community_Comment.User_Post.Post_comment=obj2
    obj.Community_Comment.User_Post.save()
    obj.Community_Comment.delete()
    return redirect(f"/community-write-comment-screen/{obj.Community_Post_obj.id}")

# --- load -- comment reply screen ---
@login_required(login_url='/')
def loadCommunityCommentReplyScreen(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Community_Post_Comment_obj=Community_Post_Comment.objects.get(id=id)
    if request.method=="POST":
        Post_Reply=request.POST.get("reply")
        Post_Date=date.today()
        now = datetime.now()
        Post_time = now.strftime("%H:%M:%S")
        Community_Comment_reply.objects.create(Community_Comment=Community_Post_Comment_obj,User_Profile=userprofile,Reply=Post_Reply,Reply_Date=Post_Date,Reply_Time=Post_time)
        return redirect(f"/community-comment-reply-screen/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Date=date.today()
        Our_News_count=News.objects.filter(Date=Date).count()
        Community_our=Community_Comment_reply.objects.filter(Community_Comment=Community_Post_Comment_obj)[::-1]
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"Comment":Community_Post_Comment_obj,"Community":Community_our,}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"Comment":Community_Post_Comment_obj,"Community":Community_our,}
        # context={"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"Comment":Community_Post_Comment_obj,"Community":Community_our,'My_community':My_Community,"Our_News_count":Our_News_count}
        return render(request, 'community_profession/comment-reply-screen.html',context)

@login_required(login_url='/')
def news(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Our_News=News.objects.all()[::-1]
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    Our_News_count=News.objects.filter(Date=Date).count()
    if obj is not None:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"News":Our_News}
    else:
        context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"News":Our_News}
    return render(request, 'community_profession/news.html',context)

@login_required(login_url='/')
def like_news(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        news_obj=request.POST.get("post_id")
        our_news=News.objects.get(id=news_obj)
        if userprofile in our_news.News_like.all():
            our_news.News_like.remove(userprofile)
        else:
            our_news.News_like.add(userprofile)
        like, created=News_Main_Like.objects.get_or_create(user_profile=userprofile,news=our_news)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()
        data={
            'value':like.value,
            'post':our_news.News_like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect("news")

@login_required(login_url='/')
def news_comment(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Our_News=News.objects.get(id=id)
    if request.method=="POST":
        Comment=request.POST.get("comment")
        # # print(Comment)
        News_Date=date.today()
        now = datetime.now()
        News_time = now.strftime("%H:%M:%S")
        News_Comment.objects.create(User_Profile=userprofile,
        News_id=Our_News,Comment=Comment,Date=News_Date,Time=News_time)
        obj=News_Comment.objects.filter(News_id=Our_News)
        Our_News.comment=len(obj)
        Our_News.save()
        return redirect(f"/news_comment/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        # My_Community=Community.objects.all()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Comment_obj=News_Comment.objects.filter(News_id=Our_News)
        Comment_Count=News_Comment.objects.filter(News_id=Our_News).count()
        Date=date.today()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Our_News_count=News.objects.filter(Date=Date).count()
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"News":Our_News,"All_Comment":Comment_obj,"Comment_Count":Comment_Count}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"user":userprofile,"News":Our_News,"All_Comment":Comment_obj,"Comment_Count":Comment_Count}
        # context={"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,"News":Our_News,"User":User_Profile_obj,"All_Comment":Comment_obj,"Comment_Count":Comment_Count}
        return render(request,'community_profession/news-comment.html',context)

@login_required(login_url='/')
def like_Comment_news(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        news_obj=request.POST.get("post_id")
        our_comment_news=News_Comment.objects.get(id=news_obj)
        if userprofile in our_comment_news.News_comment_like.all():
            our_comment_news.News_comment_like.remove(userprofile)
        else:
            our_comment_news.News_comment_like.add(userprofile)
        like, created=News_Comment_Like.objects.get_or_create(user_profile=userprofile,news_comment=our_comment_news)
        if not created:
            if like.value=="Like":
                like.value="Unlike"
            else:
                like.value="Like"
        like.save()
        data={
            'value':like.value,
            'post':our_comment_news.News_comment_like.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect("news")

@login_required(login_url='/')
def edit_news_comment(request, id):
    obj=News_Comment.objects.get(id=id)
    if request.method=="POST":
        comment_obj=request.POST.get("Review")
        obj.Comment=comment_obj
        obj.save()
        return redirect(f"/news_comment/{obj.News_id.id}")
    else:
        return redirect(f"/news_comment/{obj.News_id.id}")

@login_required(login_url='/')
def delete_news_commenrt(request, id):
    news_comment_obj=News_Comment.objects.get(id=id)
    obj=news_comment_obj.News_id.comment
    obj1=obj-1
    news_comment_obj.News_id.comment=obj1
    news_comment_obj.News_id.save()
    news_comment_obj.delete()
    return redirect(f"/news_comment/{news_comment_obj.News_id.id}")

@login_required(login_url='/')
def news_comment_reply(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    Post_obj=News_Comment.objects.get(id=id)
    if request.method=="POST":
        News_Reply=request.POST.get("reply")
        # print(News_Reply)
        News_Reply_Date=date.today()
        now = datetime.now()
        News_Reply_Time = now.strftime("%H:%M:%S")
        News_Comment_reply.objects.create(Comment=Post_obj,User_Profile=userprofile,Reply=News_Reply,Reply_Date=News_Reply_Date,Reply_Time=News_Reply_Time)
        obj=News_Comment_reply.objects.filter(Comment=Post_obj)
        Post_obj.reply=len(obj)
        Post_obj.save()
        return redirect(f"/news_comment_reply/{id}")
    else:
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        Reply=News_Comment_reply.objects.filter(Comment=Post_obj)
        # My_Community=Community.objects.all()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Date=date.today()
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Our_News_count=News.objects.filter(Date=Date).count()
        if obj is not None:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,'Reply':Reply,"Post_obj":Post_obj}
        else:
            context={"Question":User_Question_obj,"Question_count":User_Question_count,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,'Reply':Reply,"Post_obj":Post_obj}
        # context={"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"Post_obj":Post_obj,'Reply':Reply,'My_community':My_Community,"Our_News_count":Our_News_count}
        return render(request, 'community_profession/news-comment-reply.html',context)

@login_required(login_url='/')
def edit_news_reply(request, id):
    obj=News_Comment_reply.objects.get(id=id)
    if request.method=="POST":
        reply=request.POST.get("Review")
        obj.Reply=reply
        obj.save()
        return redirect(f"/news_comment_reply/{obj.Comment.id}")
    else:
        return redirect(f"/news_comment_reply/{obj.Comment.id}")

@login_required(login_url='/')
def delete_news_reply(request, id):
    obj=News_Comment_reply.objects.get(id=id)
    # print(obj)
    obj1=obj.Comment.reply
    # print(obj1)
    obj2=int(obj1)-1
    obj.Comment.reply=obj2
    obj.Comment.save()
    obj.delete()
    return redirect(f"/news_comment_reply/{obj.Comment.id}")

@login_required(login_url='/')
def ans_later(request,id):
    # # print(id)
    Question=User_Question.objects.get(id=id)
    # # print(Question)
    Answer_Date=date.today()
    now = datetime.now()
    Answer_time = now.strftime("%H:%M:%S")
    user=request.user
    User_type=UserType.objects.get(user_id=user)
    User_Profile_obj=UserProfile.objects.get(usertype=User_type)
    if Answer_later.objects.filter(Question=Question,User_Profile=User_Profile_obj):
        # print("the Question Already Added")
        return redirect("community-screen")
    else:
        Answer_later.objects.create(Question=Question,User_Profile=User_Profile_obj,Date=Answer_Date,Time=Answer_time)
        Question.Answer_later=True
        Question.save()
        return redirect("community-screen")

@login_required(login_url='/')
def delete_ans_later(request,id):
    Answer=Answer_later.objects.get(id=id)
    Question=User_Question.objects.get(id=Answer.Question.id)
    Question.Answer_later=False
    Question.save()
    Answer.delete()
    return redirect("community-screen")

@login_required(login_url='/')
def Unjoin(request,id):
    # print(id)
    unjoin=Join_Community.objects.get(id=id)
    comunity_obj=Community.objects.get(id=unjoin.Commnunity_id.id)

    # print(comunity_obj)
    comunity_obj.community_member=comunity_obj.community_member-1
    # print(unjoin)
    unjoin.delete()
    comunity_obj.save()
    return redirect("community-screen")

@login_required(login_url='/')
def serach_profession(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        profession_obj=request.POST.get("profesion_search")
        Profession_obj=Profession.objects.filter(shop_name__icontains=profession_obj)
        # print(Profession_obj)
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'profession':Profession_obj}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,'profession':Profession_obj}
        return render(request,'community_profession/profession-search.html',context)
    else:
        return render(request,'community_profession/home-screen.html')

@login_required(login_url='/')
def serach_Community(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        Community_obj=request.POST.get("search_community")
        community_obj=Community.objects.filter(Community_Name__icontains=Community_obj)
        # print(community_obj)
        if obj is not None:
            context={'joincommunityobj':joincommunityobj,"My_community":obj,'userprofile':userprofile,'community_obj':community_obj}
        else:
            context={'My_community':My_Community,'userprofile':userprofile,'community_obj':community_obj}
        return render(request,'community_profession/home-screen.html',context)
    else:
        return render(request,'community_profession/home-screen.html')

# drop down

@login_required(login_url='/')
def Community_Edit_My_Image(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_post_obj=UserPost.objects.get(id=id)
    if request.method=="POST":
        User_post_obj.Description=request.POST.get("Description")
        User_post_obj.save()
        return redirect("community-screen")
    else:
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Date=date.today()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Our_News_count=News.objects.filter(Date=Date).count()
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        if obj is not None:
            context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":User_post_obj,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
        else:
            context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":User_post_obj,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
        return render(request, 'community_profession/community-edit-my-image.html',context)

@login_required(login_url='/')
def Community_Delete_My_Image(request, id):
    User_post_obj=UserPost.objects.get(id=id)
    User_post_obj.delete()
    return redirect("community-screen")

@login_required(login_url='/')
def Community_Edit_My_Question(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_question=User_Question.objects.get(id=id)
    if request.method=="POST":
        User_question.Question=request.POST.get("Question")
        User_question.Question_Edit=True
        User_question.save()
        return redirect("Community_My_Question")
    else:
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Date=date.today()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Our_News_count=News.objects.filter(Date=Date).count()
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        if obj is not None:
            context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":User_question,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
        else:
            context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":User_question,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
        return render(request, 'community_profession/community-edit-my-question.html',context)

@login_required(login_url='/')
def Community_Delete_My_Question(request, id):
    User_question=User_Question.objects.get(id=id)
    User_question.delete()
    return redirect("Community_My_Question")

@login_required(login_url='/')
def Community_Edit_My_Video(request,id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    User_post_obj=UserPost.objects.get(id=id)
    if request.method=="POST":
        User_post_obj.Description=request.POST.get("Description")
        User_post_obj.save()
        return redirect("Community_My_Video")
    else:
        User_id=UserProfile.objects.all().exclude(id=userprofile.id)
        Date=date.today()
        User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
        User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
        Our_News_count=News.objects.filter(Date=Date).count()
        Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
        Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()
        if obj is not None:
            context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":User_post_obj,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,}
        else:
            context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,"userid":User_id,"User_POST":User_post_obj,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile}
        return render(request, 'community_profession/community-edit-my-video.html',context)

@login_required(login_url='/')
def Community_Delete_My_Video(request, id):
    User_post_obj=UserPost.objects.get(id=id)
    User_post_obj.delete()
    return redirect("Community_My_Video")

@login_required(login_url='/')
def Review_Delete(request,id):
    obj=ProfessionReview.objects.get(id=id)
    obj.delete()
    return redirect(f"/profession-personal-details/{obj.Profession.id}")

@login_required(login_url='/')
def edit_review(request,id):
    obj=ProfessionReview.objects.get(id=id)
    if request.method=="POST":
        review=request.POST.get("Review")
        # print(review)
        obj.Review=review
        obj.save()
        return redirect(f"/profession-personal-details/{obj.Profession.id}")
    else:
        return redirect(f"/profession-personal-details/{obj.Profession.id}")

@login_required(login_url='/')
def review_reply_delete(request, id):
    obj=ProfessionReview_Reply.objects.get(id=id)
    obj1=obj.Review.Reply
    obj2=obj1-1
    obj.Review.Reply=obj2
    obj.Review.save()
    obj.delete()
    return redirect(f"/review_Reply/{obj.Review.id}")

@login_required(login_url='/')
def edit_review_reply(request,id):
    obj=ProfessionReview_Reply.objects.get(id=id)
    if request.method=="POST":
        review=request.POST.get("Review_reply")
        # print(review)
        obj.Review_Reply=review
        obj.save()
        return redirect(f"/review_Reply/{obj.Review.id}")
    else:
        return redirect(f"/review_Reply/{obj.Review.id}")

def load_more(request):
    # print(request.body)
    offset = request.GET.get('offset')
    # print(offset)
    offset_int = int(offset)
    
    limit = 2
    # post_obj = Post.objects.all()[offset_int:offset_int+limit]
    post_obj = list(ProfessionReview.objects.values()[offset_int:offset_int+limit])
    data = {
        'posts': post_obj
    }
    # print(data)
    return JsonResponse(data=data)

@login_required(login_url='/')
def bookmark_post(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    post = Community_Post.objects.get(id=id)
    Bookmark.objects.create(user_profile=userprofile,post=post)
    post.user_post.Post_bookmark=True
    post.user_post.save()
    return redirect("community-screen")

@login_required(login_url='/')
def bookmark_question(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    question = User_Question.objects.get(id=id)
    # print("Question")
    Bookmark.objects.create(user_profile=userprofile,question=question)
    question.Question_bookmark=True
    question.save()
    return redirect("community-screen")

@login_required(login_url='/')
def bookmark_News(request, id):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    News_obj = News.objects.get(id=id)
    # print("news")
    Bookmark.objects.create(user_profile=userprofile,news=News_obj)
    News_obj.News_bookmark=True
    News_obj.save()
    return redirect("news")

@login_required(login_url='/')
def bookmark_page(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    bookmark=Bookmark.objects.filter(user_profile=userprofile)[::-1]
    User_id=UserProfile.objects.all().exclude(id=userprofile.id)
    Date=date.today()
    User_Question_obj=User_Question.objects.filter(User_id=userprofile.id)[::-1][:3]#"Question":User_Question_obj
    User_Question_count=User_Question.objects.filter(User_id=userprofile.id).count()
    Our_News_count=News.objects.filter(Date=Date).count()
    Answer_later_obj=Answer_later.objects.filter(User_Profile=userprofile)
    Answer_later_count=Answer_later.objects.filter(User_Profile=userprofile).count()

    # # print({{ request.path }}, {{ request.get_full_path }})
    a=request.path
    # print(a)

    if obj is not None:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,
        "userid":User_id,'My_community':obj,"Our_News_count":Our_News_count,'userprofile':userprofile,'joincommunityobj':joincommunityobj,"bookmark":bookmark}
    else:
        context={"Question_count":User_Question_count,"Question":User_Question_obj,"Answer":Answer_later_obj,"Answer_count":Answer_later_count,
        "userid":User_id,'My_community':My_Community,"Our_News_count":Our_News_count,'userprofile':userprofile,"bookmark":bookmark}
    return render(request, 'community_profession/Bookmark.html',context)

@login_required(login_url='/')
def remove_post_bookmark(request, id):
    post=UserPost.objects.get(id=id)
    bookmark=Bookmark.objects.get(post=post.id)
    post.Post_bookmark=False
    post.save()
    bookmark.delete()
    return redirect("bookmark_page")

@login_required(login_url='/')
def remove_question_bookmark(request, id):
    question=User_Question.objects.get(id=id)
    bookmark=Bookmark.objects.get(question=question.id)
    question.Question_bookmark=False
    question.save()
    bookmark.delete()
    return redirect("bookmark_page")

@login_required(login_url='/')
def remove_news_bookmark(request, id):
    news_obj=News.objects.get(id=id)
    bookmark=Bookmark.objects.get(news=news_obj.id)
    news_obj.News_bookmark=False
    news_obj.save()
    bookmark.delete()
    return redirect("bookmark_page")

@login_required(login_url='/')
def report_post(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        post=request.POST.get("post_id")
        print(post)
        post_id=UserPost.objects.get(id=int(post))
        report=request.POST.get("report_descrition")
        adult=request.POST.get("adult")
        abuse=request.POST.get("abuse")

        if adult != None:
            adult = True
        else:
            adult = False

        if abuse != None:
            abuse = True
        else:
            abuse = False
        
        Repost_Date=date.today()
        now = datetime.now()
        Repost_Time = now.strftime("%H:%M:%S")

        Report.objects.create(report_description=report,user_profile=userprofile,post=post_id,report_date=Repost_Date,report_time=Repost_Time,adult_content=adult,abusing_content=abuse)

        return redirect("community-screen")
    else:
        return redirect("community-screen")

@login_required(login_url='/')
def report_question(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        question=request.POST.get("question_id")
        question_id=User_Question.objects.get(id=int(question))
        report=request.POST.get("report_descrition")
        adult=request.POST.get("adult")
        abuse=request.POST.get("abuse")
        
        if adult != None:
            adult = True
        else:
            adult = False

        if abuse != None:
            abuse = True
        else:
            abuse = False
        
        Repost_Date=date.today()
        now = datetime.now()
        Repost_Time = now.strftime("%H:%M:%S")

        Report.objects.create(report_description=report,user_profile=userprofile,question=question_id,report_date=Repost_Date,report_time=Repost_Time,adult_content=adult,abusing_content=abuse)

        return redirect("community-screen")
    else:
        return redirect("community-screen")

@login_required(login_url='/')
def report_news(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        news_obj=request.POST.get("news_id")
        news_id=News.objects.get(id=int(news_obj))
        report=request.POST.get("report_descrition")
        adult=request.POST.get("adult")
        abuse=request.POST.get("abuse")
        
        if adult != None:
            adult = True
        else:
            adult = False

        if abuse != None:
            abuse = True
        else:
            abuse = False
        
        Repost_Date=date.today()
        now = datetime.now()
        Repost_Time = now.strftime("%H:%M:%S")

        Report.objects.create(report_description=report,user_profile=userprofile,news_id=news_id,report_date=Repost_Date,report_time=Repost_Time,adult_content=adult,abusing_content=abuse)

        return redirect("news")
    else:
        return redirect("news")

@login_required(login_url='/')
def report_profile(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        profile=request.POST.get("profile_id")
        report=request.POST.get("report_descrition")
        adult=request.POST.get("adult")
        abuse=request.POST.get("abuse")
        
        if adult != None:
            adult = True
        else:
            adult = False

        if abuse != None:
            abuse = True
        else:
            abuse = False
        
        Repost_Date=date.today()
        now = datetime.now()
        Repost_Time = now.strftime("%H:%M:%S")

        Report.objects.create(report_description=report,user_profile=userprofile,user_id=profile,report_date=Repost_Date,report_time=Repost_Time,adult_content=adult,abusing_content=abuse)

        return redirect(f"/profession-profile-screen/{profile}")
    else:
        return redirect(f"/profession-profile-screen/{profile}")

@login_required(login_url='/')
def report_community(request):
    userprofile,joincommunityobj,obj,My_Community=userprofileobj(request)
    if request.method=="POST":
        community_id=request.POST.get("community_id")
        Community_id=Community.objects.get(id=int(community_id))
        report=request.POST.get("report_descrition")
        adult=request.POST.get("adult")
        abuse=request.POST.get("abuse")

        if adult != None:
            adult = True
        else:
            adult = False

        if abuse != None:
            abuse = True
        else:
            abuse = False
        
        Repost_Date=date.today()
        now = datetime.now()
        Repost_Time = now.strftime("%H:%M:%S")

        Report.objects.create(report_description=report,user_profile=userprofile,community_id=Community_id,report_date=Repost_Date,report_time=Repost_Time,adult_content=adult,abusing_content=abuse)

        return redirect(f"/community-profile-screen/{Community_id.id}")
    else:
        return redirect(f"/community-profile-screen/{Community_id.id}")

@login_required(login_url='/')
def delete_Answer(request, id):
    Answer_obj=User_Answer.objects.get(id=id)
    print(Answer_obj)
    obj=Answer_obj.Question.answer
    print(obj)
    obj2=obj-1
    Answer_obj.Question.answer=obj2
    Answer_obj.Question.save()
    Answer_obj.delete()
    return redirect(f"/Add_Answer/{Answer_obj.Question.id}")

@login_required(login_url='/')
def edit_answer(request,id):
    obj=User_Answer.objects.get(id=id)
    if request.method=="POST":
        review=request.POST.get("Review")
        obj.Answer=review
        obj.save()
        return redirect(f"/Add_Answer/{obj.Question.id}")
    else:
        return redirect(f"/Add_Answer/{obj.Question.id}")

@login_required(login_url='/')
def delete_answer_reply(request, id):
    reply_obj=Answer_Reply.objects.get(id=id)
    print(reply_obj)
    obj=reply_obj.Answer.reply
    print(obj)
    obj2=obj-1
    reply_obj.Answer.reply=obj2
    reply_obj.Answer.save()
    reply_obj.delete()
    return redirect(f"/Add_Answer_Reply/{reply_obj.Answer.id}")

@login_required(login_url='/')
def edit_answer_reply(request,id):
    obj=Answer_Reply.objects.get(id=id)
    if request.method=="POST":
        review=request.POST.get("Review")
        obj.Reply=review
        obj.save()
        return redirect(f"/Add_Answer_Reply/{obj.Answer.id}")
    else:
        return redirect(f"/Add_Answer/{obj.Answer.id}")


# -- load privacy policy page --
def loadPrivacyPolicy(request):
    return render(request, 'community_profession/privacy-policy.html')

# -- load Terms & Condition page --
def loadTermsAndCondition(request):
    return render(request, 'community_profession/terms-condition.html')