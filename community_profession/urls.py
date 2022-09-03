from django.urls import path
from .import views
urlpatterns = [
    # --- Load Professions Pages ---
    path('home-screen', views.loadHomeScreenPage, name='home-screen'), # load - home screen.
    path('profession-see-all', views.loadProfessionSeeAllScreen, name='profession-see-all'), # profession-see all screen
    path('search-nearest-professions/<int:id>', views.loadSearchNearestProfessions, name='search-nearest-professions'), # search nearest professions
    path('nearest-professions-list/<int:id>', views.loadNearestProfessionsList, name='nearest-professions-list'), # nearest professions list
    path('profession-personal-details/<int:id>', views.loadProfessionPersonalDetails, name='profession-personal-details'), # profession personal details.
    path('see-all-photos-videos/<int:id>', views.loadSeeAllPhotosAndVideos, name='see-all-photos-videos'), # profession all photos and videos
    path('photo-screen/<int:id>', views.loadPhotoScreen, name='photo-screen'), # photo screen
    path('video-screen/<int:id>', views.loadVideoScreen, name='video-screen'), # video screen
    path('user-profile-screen', views.loadUserProfileScreen, name='user-profile-screen'), # user profile screen
    # path('profession-profile-screen', views.loadProfessionProfileScreen, name='profession-profile-screen'), # profession profile screen
    # --- load Community Pages ---
    path('community-screen', views.loadCommunityScreen, name='community-screen'), # load community --- HOME SCREEN ---
    path('community-answer', views.loadCommunityAnswerScreen, name='community-answer'), # load community answer screen
    path('community-users-questions-answer', views.loadCommunityUsersQuestionsAnswerScreen, name='community-users-questions-answer'),#
    path('normal-user-community-screen', views.loadNormalUserCommunityScreen, name='normal-user-community-screen'),
    path('community-profile-screen/<int:id>', views.loadCommunityProfileScreen, name='community-profile-screen'),
    path('community-create-post-page/<int:id>', views.loadCommunityCreatePostPage, name='community-create-post-page'),
    path('community-write-comment-screen/<int:id>', views.loadCommunityWriteCommentScreen, name='community-write-comment-screen'),
    path('community-comment-reply-screen/<int:id>', views.loadCommunityCommentReplyScreen, name='community-comment-reply-screen'),

    # ========================================================
    path("User_Post",views.User_Post,name="User_Post"),
    path("add_comment/<int:id>",views.add_comment,name="add_comment"),
    path("Post_comment_reply/<int:id>",views.Post_comment_reply,name="Post_comment_reply"),
    path("Create_Community",views.Create_Community,name="Create_Community"),
    path("Add_question",views.Add_question,name="Add_question"),
    path("Add_Answer/<int:id>",views.Add_Answer,name="Add_Answer"),
    path("Add_Answer_Reply/<int:id>",views.Add_Answer_Reply,name="Add_Answer_Reply"),
    path("Join_Coummunity/<int:id>",views.Join_Coummunity,name="Join_Coummunity"),
    path("news",views.news,name="news"),
    path("news_comment/<int:id>",views.news_comment,name="news_comment"),
    path("ans_later/<int:id>",views.ans_later,name="ans_later"),
    # path("answer/<int:id>",views.answer,name="answer"),
    path("delete_ans_later/<int:id>",views.delete_ans_later,name="delete_ans_later"),
    path("Unjoin/<int:id>",views.Unjoin,name="Unjoin"),
    path("Edit_Community/<int:id>",views.Edit_Community,name="Edit_Community"),
    path("Delete_Community/<int:id>",views.Delete_Community,name="Delete_Community"),
    path("review_Reply/<int:id>",views.review_Reply,name="review_Reply"),
    path("serach_profession",views.serach_profession,name="serach_profession"),
    path("serach_Community",views.serach_Community,name="serach_Community"),
    path("Community_image",views.Community_image,name="Community_image"),
    path("Community_Question",views.Community_Question,name="Community_Question"),
    path("Community_My_Image",views.Community_My_Image,name="Community_My_Image"),
    path("Community_My_Question",views.Community_My_Question,name="Community_My_Question"),
    path("like_post/<int:id>",views.like_post,name="like_post"),
]