from django.shortcuts import render,redirect,render_to_response
from tester.models import Signup,Seller,Pending_transactions,Club
from django.http import JsonResponse,HttpResponse
from .forms import UploadBookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from welcomepage.views import navbar_functions

# Create your views here.


def get_book_data(user_usn=None,book_name=None):

	""" serializes all books data and return them to the caller"""
	
	my_list = list()
	sellers = []
	if(user_usn != None):
		sellers = Seller.objects.exclude(seller_id_id = user_usn)
	elif (book_name != None):
		sellers = Seller.objects.filter(book_name__contains=book_name)

	for seller in sellers:
	
		my_dict = {
		"usn":str(seller.seller_id_id),
		"book_name":str(seller.book_name)
		}
		my_list.append(my_dict)

	return my_list

def list_books_for_sale(request):

	""" renders the page that displays all the books for sale"""
	#if request.method=='POST' and request.POST.get('logout'):
	#	return my_logout(request)
	
	navfunc = navbar_functions(request)
	newdict = navfunc.copy()
	
	try:
		user_usn = request.session['usn']
	except KeyError:
		user_usn = None
	books_data = get_book_data(user_usn) # get serialized book data from get_book_data method
	paginator = Paginator(books_data,3)

	page=request.GET.get('page')
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)

		# print (data)
	newdict.update({'data':data})
	clubs = Club.objects.all()
	newdict.update({"clubs":clubs})
	return render(request,'up_for_sale.html',newdict)
	
def upload_book(request):
	
	"""renders the form to upload a new book and makes an entry into the backend (Seller's table) """

	#if request.method=='POST' and request.POST.get('logout'):
	#	return my_logout(request)

	navfunc = navbar_functions(request)
	newdict = navfunc.copy()
	
	if request.method == 'POST':
		form = UploadBookForm(request.POST)

		if form.is_valid():
			new_book = form.save(commit=False)
			
			new_book.seller_id = Signup.objects.get(usn=request.session['usn'])
			new_book.save() 
			return redirect('list_books_for_sale')
		else:
			form = UploadBookForm()
			newdict.update({'form':form})
			clubs = Club.objects.all()
			newdict.update({"clubs":clubs})
			return render(request,'upload_book.html',newdict)

	else:
		form = UploadBookForm()
		newdict.update({'form':form})
		clubs = Club.objects.all()
		newdict.update({"clubs":clubs})
		
		return render(request,'upload_book.html',newdict)


def buy(request):

	""" in response to the AJAX request, makes an entry into Pending Transactions when user clicks on buy"""

	print (request.POST, request.session['usn'])

	book_name = request.POST['book_name']
	buyer_usn = Signup.objects.get(usn = request.session['usn'])
	seller_usn = Seller.objects.get(seller_id_id = request.POST['seller_id'], book_name = book_name)

	new_entry = Pending_transactions(buyer_id=buyer_usn, seller=seller_usn,book_name=book_name)
	new_entry.save()
	
	return HttpResponse(request.POST)

def search_book(request):

	"""searches the db based on the query string specified by the user and returns the list of 
	books matching the search criteria"""

	book_name = request.GET.get('book_name')
	data = get_book_data(book_name = book_name)
	# print data
	return JsonResponse({'data':data})