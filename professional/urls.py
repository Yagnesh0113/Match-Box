from django.urls import path
from .import views
urlpatterns = [

    # --- Load Professions Pages ---
    path('profession-profile-screen', views.loadProfessionProfileScreen, name='profession-profile-screen'), # profession profile screen
    path('profession-profile-screen/<int:id>', views.loadProfessionProfileScreen, name='profession-profile-screen'), # profession profile screen
    
    path('add_profession', views.add_profession, name='add_profession'), # profession profile screen
    path('profession_details/<int:id>', views.profession_details, name='profession_details'), # profession profile screen
    path('add_services',views.add_services,name='add_services'),
    path('update_profession_details/<int:id>',views.update_profession_details,name='update_profession_details'),
    path('edit_profession_image/<int:id>',views.edit_profession_image,name='edit_profession_image'),
    path('delete_service/<int:id>',views.delete_service,name='delete_service'),
    path('add_profesion_gallery',views.add_profesion_gallery,name='add_profesion_gallery'),
    path('add_profesion_video',views.add_profesion_video,name='add_profesion_video'),
    path('See-all-photos-videos/<int:id>', views.loadSeeAllPhotosAndVideos, name='See-all-photos-videos'), # profession all photos and videos
    path('update_whatsapp_number',views.update_whatsapp_number,name='update_whatsapp_number'), # whatsapp url
    path('update_profile_image',views.update_profile_image,name='update_profile_image'), # whatsapp url
    
    path('Days_details/<int:id>',views.Days_details,name='Days_details'), # whatsapp url
    path('delete_Image/<int:id>',views.delete_Image,name='delete_Image'), # Delete Image
    path('delete_Video/<int:id>',views.delete_Video,name='delete_Video'), # Delete Video
    path('delete_Profession/<int:id>',views.delete_Profession,name='delete_Profession'), # Delete Profession
    path('like_Review',views.like_Review,name='like_Review'), # like comment
    path('edit_service/<int:id>',views.edit_service,name='edit_service'), # edit_Servvice
    path('update_details',views.update_details,name='update_details'), # edit_Servvice


]
