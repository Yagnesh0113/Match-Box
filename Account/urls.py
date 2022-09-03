from django.urls import path
from .import views
urlpatterns = [
    path('sign-up', views.loadSignUpPage, name='sign-up'), # load - default page - sign up - normal user
    path('sign-up-profession', views.loadSignUpForProfession, name='sign-up-profession'), # load - signup for profession
    path('', views.loadSignInPage, name='sign-in'), # load - sign in for both normal and professional user.
    path('forgot-password', views.loadForgotPasswordPage, name='forgot-password'), # load - forgot password.
    path('user_logout', views.user_logout, name='user_logout'), # load logout function.
    path('load_city', views.load_city, name='load_city'), # load logout function.
    path('professional_or_community', views.professional_or_community, name='professional_or_community'), # load logout function.
    path('new_community_user', views.new_community_user, name='new_community_user'), # load logout function.
    path('new_professonal_user', views.new_professonal_user, name='new_professonal_user'), # load logout function.




]
