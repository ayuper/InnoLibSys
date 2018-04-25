from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserLoginForm, PatronEditForm, PatronAddForm, DocumentAddForm, ProfileForm, ProfileAddForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import Profile, Document, ReturnList, Copy
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime
from .functions import *
import unittest
from django.test import Client, TestCase

# Create your tests here.
class tests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.admin1 = create_admin('admin1', 'admin1')
		cls.d1 = Document.objects.create(title='Introduction to Algorithms',authors='Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein',price=5000, document_type=0, published_date=datetime.date.today(), keywords='Algorithms, Data Structures, Complexity, Computational Theory')
		cls.d2 = Document.objects.create(title='Algorithms + Data Structures = Programs', authors='Niklaus Wirth',best_seller=True,price=5000, document_type=0, published_date=datetime.date.today(), keywords='Algorithms, Data Structures, Search Algorithms, Pascal')
		cls.d3 = Document.objects.create(title='The Art of Computer Programming',authors='Donald E. Knuth',price=5000, document_type=0, published_date=datetime.date.today(), keywords='Algorithms, Combinatorial Algorithms, Recursion')
		cls.p1 = User.objects.create_user(username='p1', password='p1', first_name='Sergey', last_name='Afonso')
		cls.p2 = User.objects.create_user(username='p2', password='p2', first_name='Nadia', last_name='Teixeira')
		cls.p3 = User.objects.create_user(username='p3', password='p3', first_name='Elvira', last_name='Espindola')
		cls.s = User.objects.create_user(username='s', password='s', first_name='Andrey', last_name='Velo')
		cls.v = User.objects.create_user(username='v', password='v', first_name='Veronika', last_name='Rama')
		cls.p1.profile.adress='Via Margutta, 3'
		cls.p1.profile.phone_number='30001'
		cls.p1.profile.patron_type=4
		cls.p2.profile.adress='Via Sacra, 13'
		cls.p2.profile.phone_number='30002'
		cls.p2.profile.patron_type=4
		cls.p3.profile.adress='Via del Corso, 22'
		cls.p3.profile.phone_number='30003'
		cls.p3.profile.patron_type=4
		cls.s.profile.adress='Avenida Mazatlan 250'
		cls.s.profile.phone_number='30004'
		cls.s.profile.patron_type=1
		cls.v.profile.adress='Stret Atocha, 27'
		cls.v.profile.phone_number='30005'
		cls.v.profile.patron_type=2
	def test_c1(self):
		create_admin('admin2', 'admin2')
		self.assertEqual(Profile.objects.filter(admin=True).count(), 1)
	def test_c2(self):
		delete_all_objects()
		admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		self.assertEqual(Profile.objects.filter(librarian=True).count(), 3)
	def test_c3(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		create_document(l1, self.d1, 3)
		create_document(l1, self.d2, 3)
		create_document(l1, self.d3, 3)
		self.assertEqual(Document.objects.all().count(), 0)
	def test_c4(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		create_document(l2, self.d1, 3)
		create_document(l2, self.d2, 3)
		create_document(l2, self.d3, 3)
		create_patron(l2, self.p1)
		create_patron(l2, self.p2)
		create_patron(l2, self.p3)
		create_patron(l2, self.s)
		create_patron(l2, self.v)
		self.assertEqual(Document.objects.all().count(), 3)
		self.assertEqual(Profile.objects.filter(librarian=False, admin=False).count(), 5)
	def test_c5(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		data = {}
		data['copies'] = 2
		edit_document(l3, d1, data)
		self.assertEqual(Copy.objects.filter(document=d1).count(), 2)
	def test_c6(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		check_out_a_book(p1, d3, datetime.date.today())
		check_out_a_book(p2, d3, datetime.date.today())
		check_out_a_book(s, d3, datetime.date.today())
		check_out_a_book(v, d3, datetime.date.today())
		check_out_a_book(p3, d3, datetime.date.today())
		outstanding_request(l1, d3)
		self.assertEqual(Document.objects.filter(outstanding_request=True).count(), 0)
	def test_c7(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		check_out_a_book(p1, d3, datetime.date.today())
		check_out_a_book(p2, d3, datetime.date.today())
		check_out_a_book(s, d3, datetime.date.today())
		check_out_a_book(v, d3, datetime.date.today())
		check_out_a_book(p3, d3, datetime.date.today())
		outstanding_request(l3, d3)
		self.assertEqual(DocumentQueue.objects.filter(document=d3).count(), 0)
		self.assertEqual(Notifications.objects.filter(user=s).count(), 1)
		self.assertEqual(Notifications.objects.filter(user=p1).count(), 1)
		self.assertEqual(Notifications.objects.filter(user=p2).count(), 1)
		self.assertEqual(Notifications.objects.filter(user=v).count(), 1)
		self.assertEqual(Notifications.objects.filter(user=p3).count(), 1)
	def test_c8(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		check_out_a_book(p1, d3, datetime.date.today())
		check_out_a_book(p2, d3, datetime.date.today())
		check_out_a_book(s, d3, datetime.date.today())
		check_out_a_book(v, d3, datetime.date.today())
		check_out_a_book(p3, d3, datetime.date.today())
		outstanding_request(l1, d3)
		self.assertEqual(Log.objects.all().count(), 17)
	def test_c9(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		check_out_a_book(p1, d3, datetime.date.today())
		check_out_a_book(p2, d3, datetime.date.today())
		check_out_a_book(s, d3, datetime.date.today())
		check_out_a_book(v, d3, datetime.date.today())
		check_out_a_book(p3, d3, datetime.date.today())
		outstanding_request(l1, d3)
		self.assertEqual(Log.objects.all().count(), 17)
	def test_c10(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		search_list = search_query(v, 1, 'Introduction to Algorithms')
		self.assertEqual(len(search_list), 1)
	def test_c11(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		search_list = search_query(v, 1, 'Algorithms')
		self.assertEqual(len(search_list), 2)
	def test_c12(self):
		delete_all_objects()
		l1 = admin_create_librarian(self.admin1, 'l1', 'l1', True, False, False)
		l2 = admin_create_librarian(self.admin1, 'l2', 'l2', True, True, False)
		l3 = admin_create_librarian(self.admin1, 'l3', 'l3', True, True, True)
		d1 = create_document(l2, self.d1, 3)
		d2 = create_document(l2, self.d2, 3)
		d3 = create_document(l2, self.d3, 3)
		p1 = create_patron(l2, self.p1)
		p2 = create_patron(l2, self.p2)
		p3 = create_patron(l2, self.p3)
		s = create_patron(l2, self.s)
		v = create_patron(l2, self.v)
		search_list = search_query(v, 0, 'Algorithms')
		self.assertEqual(len(search_list), 3)