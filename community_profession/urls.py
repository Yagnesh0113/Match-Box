from django.urls import path
from .import views
urlpatterns = [
    # --- Load Professions Pages ---
    path('home-screen', views.loadHomeScreenPage, name='home-screen'), # load - home screen.
    path('profession-see-all', views.loadProfessionSeeAllScreen, name='profession-see-all'), # profession-see all screen
    path('search-nearest-professions/<int:id>', views.loadSearchNearestProfessions, name='search-nearest-professions'), # search nearest professions
    path('nearest-professions-list/<int:id>', views.loadNearestProfessionsList, name='nearest-professions-list'), # nearest professions list

    path('nearest-professions-list', views.loadNearestProfessionsList, name='nearest-professions-list'), # nearest professions list

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
    path('community-create-post-page', views.loadCommunityCreatePostPage, name='community-create-post-page'),
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
    path("Community_video",views.Community_video,name="Community_video"),
    path("Community_Question",views.Community_Question,name="Community_Question"),
    path("Community_My_Image",views.Community_My_Image,name="Community_My_Image"),
    path("Community_My_Video",views.Community_My_Video,name="Community_My_Video"),
    path("Community_My_Question",views.Community_My_Question,name="Community_My_Question"),
    path("like_post",views.like_post,name="like_post"),
    path("Community_Edit_My_Image/<int:id>",views.Community_Edit_My_Image,name="Community_Edit_My_Image"),
    path("Community_Delete_My_Image/<int:id>",views.Community_Delete_My_Image,name="Community_Delete_My_Image"),
    path("Community_Edit_My_Question/<int:id>",views.Community_Edit_My_Question,name="Community_Edit_My_Question"),
    path("Community_Delete_My_Question/<int:id>",views.Community_Delete_My_Question,name="Community_Delete_My_Question"),
    path("like_Question",views.like_Question,name="like_Question"),
    path("Community_Edit_My_Video/<int:id>",views.Community_Edit_My_Video,name="Community_Edit_My_Video"),
    path("Community_Delete_My_Video/<int:id>",views.Community_Delete_My_Video,name="Community_Delete_My_Video"),
    path("like_post_comment",views.like_post_comment,name="like_post_comment"),
    path("like_Answer",views.like_Answer,name="like_Answer"),
    path("like_news",views.like_news,name="like_news"),
    path("like_Comment_news",views.like_Comment_news,name="like_Comment_news"),
    path("news_comment_reply/<int:id>",views.news_comment_reply,name="news_comment_reply"),
    path("Review_Delete/<int:id>",views.Review_Delete,name="Review_Delete"),
    path("edit_review/<int:id>",views.edit_review,name="edit_review"),
    path("review_reply_delete/<int:id>",views.review_reply_delete,name="review_reply_delete"),
    path("edit_review_reply/<int:id>",views.edit_review_reply,name="edit_review_reply"),

    path('loaddata/', views.load_more, name='loaddata'),

    path('bookmark_post/<int:id>',views.bookmark_post,name='bookmark_post'),
    path('bookmark_question/<int:id>',views.bookmark_question,name='bookmark_question'),
    path('bookmark_News/<int:id>',views.bookmark_News,name='bookmark_News'),
    path('bookmark_page',views.bookmark_page,name='bookmark_page'),
    path('remove_post_bookmark/<int:id>',views.remove_post_bookmark,name='remove_post_bookmark'),
    path('remove_question_bookmark/<int:id>',views.remove_question_bookmark,name='remove_question_bookmark'),
    path('remove_news_bookmark/<int:id>',views.remove_news_bookmark,name='remove_news_bookmark'),


    path('report_post',views.report_post,name='report_post'),
    path('report_question',views.report_question,name='report_question'),
    path('report_news',views.report_news,name='report_news'),
    path('report_profile',views.report_profile,name='report_profile'),
    path('report_community',views.report_community,name='report_community'),


    

    path('edit_comment/<int:id>',views.edit_comment,name='edit_comment'),
    path('comment_delete/<int:id>',views.comment_delete,name='comment_delete'),

    path('edit_reply/<int:id>',views.edit_reply,name='edit_reply'),
    path('reply_delete/<int:id>',views.reply_delete,name='reply_delete'),

    path('delete_Answer/<int:id>',views.delete_Answer,name='delete_Answer'),
    path('edit_answer/<int:id>',views.edit_answer,name='edit_answer'),

    path('delete_answer_reply/<int:id>',views.delete_answer_reply,name='delete_answer_reply'),
    path('edit_answer_reply/<int:id>',views.edit_answer_reply,name='edit_answer_reply'),

    path('delete_news_commenrt/<int:id>',views.delete_news_commenrt,name='delete_news_commenrt'),
    path('edit_news_comment/<int:id>',views.edit_news_comment,name='edit_news_comment'),

    path('delete_news_reply/<int:id>',views.delete_news_reply,name='delete_news_reply'),
    path('edit_news_reply/<int:id>',views.edit_news_reply,name='edit_news_reply'),

    # -- privacy policy --
    path('privacy-policy', views.loadPrivacyPolicy, name='privacy-policy'),
    # -- terms and condition --
    path('terms-condition', views.loadTermsAndCondition, name='terms-condition'),

]