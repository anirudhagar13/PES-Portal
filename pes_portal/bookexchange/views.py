from django.shortcuts import render,redirect,render_to_response
from tester.models import Signup,Seller,Pending_transactions
from django.http import JsonResponse,HttpResponse
from .forms import UploadBookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from welcomepage.views import navbar_functions

# Create your views here.


def get_book_data(user_usn=None,book_name=None):

	""" serializes all books data and return them to the caller"""
	
	my_list = list()
	if(book_name == None):
		sellers = Seller.objects.exclude(seller_id_id = user_usn)
	elif (book_name != None):
		sellers = Seller.objects.filter(book_name__contains=book_name, subject__contains = book_name).exclude(seller_id_id = user_usn)


	for seller in sellers:
	
		borrowed = False
		if len(Pending_transactions.objects.filter(buyer_id_id = user_usn ,book_name = seller.book_name)) >0:
			borrowed = True

		my_dict = {
		"usn":seller.seller_id_id.encode('utf8'),
		"book_name":seller.book_name.encode('utf8'),
		"borrowed": borrowed
		}
		my_list.append(my_dict)

	return my_list


def list_books_for_sale(request):

	""" renders the page that displays all the books for sale"""
	
	try:
		user_usn = request.session['usn']
	except:
		user_usn = None
	books_data = get_book_data(user_usn) # get serialized book data from get_book_data method
	paginator = Paginator(books_data,10)

	page=request.GET.get('page')
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)

		# print (data)
	return render(request,'up_for_sale.html',navbar_functions(request, {'data':data}))


def get_buyers_details(usn):

	buyers = []
	buyers_list = list()
	# get seller objects of the current active user which is required to query the Pending Transactions table

	sellers = Seller.objects.filter(seller_id_id = usn) 
	
	#keep appending the list of buyers for every seller object
	
	for seller in sellers :
		buyers.extend(Pending_transactions.objects.filter(seller = seller))

	#for every buyer retrieve all his info from the Signup table
	
	for buyer in buyers:
		
		buyer_signup_obj = Signup.objects.get(usn = buyer.buyer_id_id) 
		
		temp_dict = {
		'name' : buyer_signup_obj.name,
		'email': buyer_signup_obj.email,
		'phone': buyer_signup_obj.phone,
		'book' : buyer.book_name,
		'dept' : buyer_signup_obj.dept,
		'sem'  : buyer_signup_obj.sem,
		}
		buyers_list.append(temp_dict)
	return buyers_list

		
def delete_book(request):
	
	""" deletes the book from record once the seller seals the deal with one of the interested buyers """
	try:
		user_usn = request.session.get('usn')
	except:
		user_usn = None
	book_name = request.POST.get('book_name').strip()
	email_id = request.POST.get('email').strip()
	pending_list = list()
	
	sellers = Seller.objects.filter(seller_id_id = user_usn, book_name=book_name)
	
	for seller in sellers:
		temp_seller = Pending_transactions.objects.filter(book_name=book_name, seller = seller )
		pending_list.extend(temp_seller)
		Pending_transactions.objects.filter(book_name=book_name, seller = seller ).delete()
		temp_seller.delete()

	sellers.delete()
	mailing_list = list() # query and fill in the list of users waiting for this particular book 

	for user in pending_list:
		user_usn = user.buyer_id_id
		user_email = Signup.objects.get(usn = user_usn).email
		if user_email != email_id:
			mailing_list.append(user_email)	

	# pending_list.delete()
	# send mail to all the users in the pending list

	mail_subject = "PES TImes : Book Transaction"
	mail_message = "The seller was not interested in 'giving IT to you' :P" + "\nBook name: " + book_name

	send_mail(mail_subject,mail_message,settings.EMAIL_HOST_USER,mailing_list,fail_silently=False)
	
	Seller.objects.filter(seller_id_id = user_usn, book_name=book_name).delete()
	# Pending_transactions.objects.filter(book_name=book_name, seller = seller ).delete()
	return HttpResponse(request.POST)




def view_buyers(request):

	""" renders the page displaying all the interested buyers """
	usn = request.session.get('usn')
	buyers = get_buyers_details(usn)
		
	return render(request,"view_buyers.html",navbar_functions(request, {'buyers':buyers}))	



def upload_book(request):
	
	"""renders the form to upload a new book and makes an entry into the backend (Seller's table) """

	if request.method == 'POST':
		form = UploadBookForm(request.POST)

		if form.is_valid():
			try:
				new_book = form.save(commit=False)
				new_book.seller_id = Signup.objects.get(usn=request.session['usn'])
				new_book.save()
			except:
				print("You have already uploaded this book")
			return redirect('list_books_for_sale')
		else:
			form = UploadBookForm()
			return render(request,'upload_book.html',navbar_functions(request, {'form':form}))

	else:
		form = UploadBookForm()
		return render(request,'upload_book.html',navbar_functions(request, {'form':form}))


def buy(request):

	""" in response to the AJAX request, makes an entry into Pending Transactions when user clicks on buy"""

	#print (request.POST, request.session['usn'])

	book_name = request.POST['book_name']
	buyer_usn = Signup.objects.get(usn = request.session['usn'])
	seller_usn = Seller.objects.get(seller_id_id = request.POST['seller_id'], book_name = book_name)

	new_entry = Pending_transactions(buyer_id=buyer_usn, seller=seller_usn,book_name=book_name)
	new_entry.save()
	
	return HttpResponse(request.POST)

def cancel_buy(request):
	
	""" in response to AJAX request , deletes an entry from Pending Transactions when user clicks on cancel """

	book_name = request.POST['book_name']
	buyer_usn = Signup.objects.get(usn = request.session['usn'])
	seller_usn = Seller.objects.get(seller_id_id = request.POST['seller_id'], book_name = book_name)
	Pending_transactions.objects.filter(buyer_id=buyer_usn, seller=seller_usn,book_name=book_name).delete()

	return HttpResponse(request.POST)	

def search_book(request):

	"""searches the db based on the query string specified by the user and returns the list of 
	books matching the search criteria"""

	book_name = request.GET.get('book_name')
	user_usn = request.session['usn']
	data = get_book_data(user_usn = user_usn, book_name = book_name)
	#print data
	return JsonResponse({'data':data})