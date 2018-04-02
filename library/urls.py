from django.urls import path, include
from . import views
from django.contrib.auth.views import logout

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('index/', views.IndexView.as_view(), name='index'),
	path('logout/', logout, {'next_page':'/library/login'}, name='logout'),
	path('manage/patrons/', views.ManagePatronsViews.as_view(), name='manage-patrons'),
	path('manage/patrons/<int:id>/', views.patron, name='manage-patron'),
	path('manage/patrons/<int:id>/edit/', views.patron_edit, name='manage-patron-edit'),
	path('manage/patrons/<int:id>/delete/', views.patron_delete, name='delete-patron'),
	path('manage/patrons/add/', views.PatronAddView.as_view(), name='add-patron'),
	path('manage/documents/', views.ManageDocumentsViews.as_view(), name='manage-documents'),
	path('manage/documents/<int:id>/', views.document, name='manage-document'),
	path('manage/documents/<int:id>/edit/', views.document_edit, name='manage-document-edit'),
	path('manage/documents/<int:id>/delete/', views.document_delete, name='delete-document'),
	path('manage/documents/add/', views.DocumentAddView.as_view(), name='add-document'),
]