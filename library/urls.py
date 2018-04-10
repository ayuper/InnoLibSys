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
	path('manage/patrons/add/', views.patron_add, name='add-patron'),
	path('manage/documents/', views.ManageDocumentsViews.as_view(), name='manage-documents'),
	path('manage/documents/<int:id>/', views.document, name='manage-document'),
	path('manage/documents/<int:id>/edit/', views.document_edit, name='manage-document-edit'),
	path('manage/documents/<int:id>/delete/', views.document_delete, name='delete-document'),
	path('manage/documents/add/', views.DocumentAddView.as_view(), name='add-document'),
	path('documents/', views.DocumentsView.as_view(), name='my-documents'),
	path('documents/<int:id>/', views.my_document, name='my-document'),
	path('documents/<int:id>/return/', views.document_return, name='document-return'),
	path('documents/check-out/', views.DocumentsCheckOutView.as_view(), name='check-out-document'),
	path('documents/check-out/<int:id>/', views.document_check_out, name='get-document'),
	path('manage/return/', views.DocumentsReturnView.as_view(), name='return-documents'),
	path('manage/return/<int:id>/', views.document_lreturn, name='return-document'),
	path('manage/documents/overdue/', views.OverdueDocumentsView.as_view(), name='overdue-documents'),
	path('manage/documents/overdue/<int:id>/', views.overdue_copy, name='overdue-copy'),
	path('mycard/', views.mycard, name='my-card'),
	path('manage/documents/<int:id>/checked/', views.PatronsCheckedView.as_view(), name='checked-patrons'),
	path('documents/<int:id>/renew/', views.document_renew, name='renew-document'),
	path('manage/documents/<int:id>/queue/', views.queue_view, name='get-queue'),
]