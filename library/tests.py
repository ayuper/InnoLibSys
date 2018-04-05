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
from .functions import check_out_a_book, check_dues, check_fines, return_book, renew, get_info
import unittest
from django.test import Client, TestCase

# Create your tests here.
class tests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.p1 = User.objects.create_user(username='p1', password='p1', first_name='Sergey', last_name='Afonso')
		cls.p2 = User.objects.create_user(username='p2', password='p2', first_name='Nadia', last_name='Teixeira')
		cls.p3 = User.objects.create_user(username='p3', password='p3', first_name='Elvira', last_name='Espindola')
		cls.s = User.objects.create_user(username='s', password='s', first_name='Andrey', last_name='Velo')
		cls.v = User.objects.create_user(username='v', password='v', first_name='Veronika', last_name='Rama')
		cls.p1.profile.adress='Via Margutta, 3'
		cls.p1.profile.phone_number='30001'
		cls.p1.profile.patron_type=4
		cls.p1.profile.save()
		cls.p2.profile.adress='Via Sacra, 13'
		cls.p2.profile.phone_number='30002'
		cls.p2.profile.patron_type=4
		cls.p2.profile.save()
		cls.p3.profile.adress='Via del Corso, 22'
		cls.p3.profile.phone_number='30003'
		cls.p3.profile.patron_type=4
		cls.p3.profile.save()
		cls.s.profile.adress='Avenida Mazatlan 250'
		cls.s.profile.phone_number='30004'
		cls.s.profile.patron_type=1
		cls.s.profile.save()
		cls.v.profile.adress='Stret Atocha, 27'
		cls.v.profile.phone_number='30005'
		cls.v.profile.patron_type=2
		cls.v.profile.save()
		cls.d1 = Document.objects.create(title='Introduction to Algorithms',authors='Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein',price=5000, document_type=0, published_date=datetime.date.today())
		cls.d2 = Document.objects.create(title='Design Patterns: Elements of Reusable Object-Oriented Software', authors='Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm',best_seller=True,price=1700, document_type=0, published_date=datetime.date.today())
		cls.d3 = Document.objects.create(title='Null References: The Billion Dollar Mistake',authors='Tony Hoare',price=700, document_type=0, published_date=datetime.date.today())
		for i in range(3):
			Copy.objects.create(user=None, document=cls.d1)
			Copy.objects.create(user=None, document=cls.d2)
			if i != 2:
				Copy.objects.create(user=None, document=cls.d3)
	def test_c1(self):
		user = User.objects.get(username=self.p1.username,password=self.p1.password)
		check_out_a_book(user, self.d1, datetime.date(2018, 3, 5))
		check_out_a_book(user, self.d2, datetime.date(2018, 3, 5))
		return_book(user, self.d2)
		dues = check_dues(user)
		fines = check_fines(user)
		self.assertEqual(dues, [(self.d1, 0)])
		self.assertEqual(fines, [(0, 0)])
	def test_c2(self):
		user = User.objects.get(username=self.p1.username,password=self.p1.password)
		check_out_a_book(user, self.d1, datetime.date(2018, 3, 5))
		check_out_a_book(user, self.d2, datetime.date(2018, 3, 5))
		p1_dues = check_dues(user)
		p1_fines = check_fines(user)
		user = User.objects.get(username=self.s.username,password=self.s.password)
		check_out_a_book(user, self.d1, datetime.date(2018, 3, 5))
		check_out_a_book(user, self.d2, datetime.date(2018, 3, 5))
		s_dues = check_dues(user)
		s_fines = check_fines(user)
		user = User.objects.get(username=self.v.username,password=self.v.password)
		check_out_a_book(user, self.d1, datetime.date(2018, 3, 5))
		check_out_a_book(user, self.d2, datetime.date(2018, 3, 5))
		v_dues = check_dues(user)
		v_fines = check_fines(user)
		self.assertEqual(p1_dues, [(self.d1, 0), (self.d2, 0)])
		self.assertEqual(p1_fines, [(0, 0), (0, 0)])
		self.assertEqual(s_dues, [(self.d1, 7), (self.d2, 14)])
		self.assertEqual(s_fines, [(7, 700), (14, 1400)])
		self.assertEqual(v_dues, [(self.d1, 21), (self.d2, 21)])
		self.assertEqual(v_fines, [(21, 2100), (21, 1700)])
	def test_c3(self):
		user = User.objects.get(username=self.p1.username,password=self.p1.password)
		check_out_a_book(user, self.d1, datetime.date(2018, 3, 29))
		renew(user, self.d1)
		self.assertEqual(get_info(user), [(self.d1, datetime.date(2018,4,30))])
		user = User.objects.get(username=self.s.username,password=self.s.password)
		check_out_a_book(user, self.d2, datetime.date(2018, 3, 29))
		renew(user, self.d2)
		self.assertEqual(get_info(user), [(self.d2, datetime.date(2018,4,16))])
		user = User.objects.get(username=self.v.username,password=self.v.password)
		check_out_a_book(user, self.d2, datetime.date(2018, 3, 29))
		renew(user, self.d2)
		self.assertEqual(get_info(user), [(self.d2, datetime.date(2018,4,9))])
		