from django.shortcuts import render,redirect
from tester.models import Signup,Seller
from django.http import JsonResponse,HttpResponse
from .forms import UploadBookForm
# Create your views here.

def populate_students(request):
	base_usn = '1pi13cs'
	for i in range(10):
		student = Student(Usn=base_usn + str(i))
		student.save()

	print ('saved')

def populate_upforsale(request):
	for i in range(5):
		student = Student(Usn = '1pi13cs'+str(i))
		entry = Seller(book_name="Intro", seller_id=student)
		entry.save()

def get_book_data():
	my_list = list()

	for seller in Seller.objects.all():
	
		my_dict = {
		"usn":str(seller.seller_id.Usn).upper(),
		"book_name":str(seller.book_name)
		}
		my_list.append(my_dict)

	return my_list



def list_books_for_sale(request):
	if request.method == 'GET':
		data = get_book_data()
		print (data)
		return render(request,'up_for_sale.html',{'data':data})

def upload_book(request):
	if request.method == 'POST':
		form = UploadBookForm(request.POST)

		if form.is_valid():
			new_book = form.save(commit=False)
			'''seller_id to be taken from the user's session
				hardcoded for now '''
			new_book.seller_id = Student('1pi13cs3')
			new_book.save() 
			return redirect('list_books_for_sale')
		else:
			form = UploadBookForm()
			return render(request,'upload_book.html',{'form':form})

	else:
		form = UploadBookForm()
		return render(request,'upload_book.html',{'form':form})


def buy(request):
	print (request.POST)

	return HttpResponse(request.POST)

def search_book(request):
	print (request.GET)

	return HttpResponse(request.GET);