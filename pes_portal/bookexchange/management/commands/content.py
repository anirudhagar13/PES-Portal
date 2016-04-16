from tester.models import *
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand,CommandError
from random import randint
import string
from django.utils import timezone
def randomizer(field):
	if field == 'phone':
		return randint(7*10**9, 10*10**9)

class Command(BaseCommand):
	
	def handle(self,*args,**options):
		#dept values are: eee cse ece civil ise me bt te
		#dob format: YYYY-MM-DD
		#sem values are: 1 2 3 4 5 6 7 8
		
		# clubs
		
		des03 = '''Ordell Ugo, the beginning vision, gives students a chance to participate in the process of developing ideas into research concepts and workable products. Starting from a single room with a small group of students it has grown into a hub of ideas where a large number of students work on innovative projects. Some students consider Ordell Ugo a turning point as it hones their leadership qualities, team spirit, industry exposure and ability to map practical implementation against theoretical concepts.Ordell Ugo is the first encounter with the world of research for students. Research takes the form of systematic inquiry involving the practical application of concepts they study. Students get to know about new things every day, from crimping Ethernet cable to writing a paper for an international conference. It is also about building bridges between the freshers and seniors, faculty and learners and striking interesting conversations. Ordell Ugo is a hub of activities, events and programs that gives the students a glimpse of the world of research and innovation.'''
		des01 = '''Samarpana is a student initiative for remembering the martyrs who have laid down their lives in the service of the nation. As the younger generation, it is our responsibility to appreciate the efforts of those who have contributed and sacrificed for us and as a civilized society, contribute something in return. To create awareness among the youth about the hardships faced by soldiers in defense, of the society and the sacrifices of the martyrs. To reach out to families of martyrs' and help them by creating a support structure for them to seek advice on various issues through experts and help them get in touch with individuals, societies or officials who can help them seek redressal to their issues.'''
		des02 = "The Techno-Cultural Fest of PES University, Bangalore. 2 days of fun, frolic, madness, competition, teamwork, and a lot of COLOURS! "
		des04 = "We orgabnise events that showcase the various shades of Indian Culture and Heritage and promote it.Ninaada is the Student's cultural forum in PESIT. It was founded with the ideal of promoting Indian heritage among youth! What better way to do this than cultural music and dance! Ninaada has organized many programmes, on PESIT campus, given by various, very famous, artistes!"
		des05 = "In keeping with the motto of “education for the real world” the students demonstrated their ability to go beyond raw concepts and abstract ideas. The annual event featured practical implementation of path breaking ideas in the form of projects successfully completed by students of all branches. The best projects were selected based on the creative component and practical utility. A walk through the venue showed once again that the students like every year have put in their best efforts to push the envelope. The enthusiasm of the participants showed that the creative spirit can make a difference like nothing else. Thanks for joining the celebration of creativity. "
		des06 = "PESIT E-Cell is a student-run, non-profit organization that helps in spreading awareness about entrepreneurship, and promotes young entrepreneurs in PESIT.A collaborative effort to help and motivate student entrepreneurs from campus to build upon, and scale up their ideas all the way from a distant dream to a reality."
		des07 = '''Student Nokia Developer is a Student Kingdom of enthusiast passionate mobile application developers where we get together to bring out the best of the best innovations that are possible on the capabilities of Nokia’s hand held devices. This is the forum which encourages the emerging students to get all help with respect to mobile application development and is driven completely by students.The idea behind this forum is to reach out many universities across the globe, reach the students there, promote the opportunities on developing mobile applications which will not only serve the purpose of being a part of their academic projects but has an immense potential to reach out people across the globe and get some recognition worldwide on the innovations and inventions that are not recognized. Help them financially as well by monetizing their applications with proper guidelines.'''
		des08 = "OpenSource philosophy is based on a simple theory that knowledge, of any form, grows when allowed to flow freely. Hence knowledge must be shared: and in its pure unadulterated form. In the realm of software, this means that the source code is open for anyone to see, share and learn. And in the case of hardware, this means that the assembly level implementations, the architecture, the hardware drivers are freely available to study and improve. This ideology and the environment that has grown around it has revolutionized the very nature of technological world and is generating ripples everyday. Some of the world’s largest collaborative projects are attributed to Open Source projects, most notable being the Linux Kernel, Ubuntu, Android, Firefox etc."
		des09 = "Ayana 2016 is a 24-hour hackathon, where participants bring their ideas to life.It blends creativity, talent and resolve to make a better India.Tech plays a pivotal role in shaping the future of our country and Ayana 2016 provides a platform for budding ideas to grow into revolutionary solutions. It provides hackers with an opportunity to showcase their skills nationwide. Ayana is being conducted for the past four years and attracts students and professionals across India competing for prizes upto Rs 3,00,000."
		des10 = "The Indian contemporary dance team of PESIT,Bangalore. Sanskrithi, the Indian contemporary dance team of PESIT, stands out because of the numerous specializations it has. The team has dancers trained in different dance forms such as Bharath Natyam, Kuchipudi, Mohiniattam, Kathak, Odissi, Yakshagana etc."
		des11 = "The official theatre and film fraternity at PES UNIVERSITY, Bangalore! The college's official dramatics and film making team. Nautanki maintains a member strength of around 30 students. Nautanki was both the mime and one-act play champions at the University (VTU) fest held at Dayanand Sagar College of Engineering, Bangalore."
		des12 = "PULSE is the western dance crew of PESIT. Founded in 2005, the crew has been actively taking part in various competitions and winning consistently. "
		des13 = "The Collegiate Social Responsibility Club of PES University, has been striving towards its aim of service to the less fortunate."
		des14 = "The current MadAds team of PESIT. Formed in 2012 we gave out first performance at the Pre-AT bash of Aatmatrisha 13' under the guidance of our father team, the Madmeniacs! Since then.. there has been no looking back xD "
		des15 = '''At PES University, the IEEE Student Branch plays an important role by providing the students, various opportunities to think outside their curriculum, learn and experiment with technology. With workshops, industrial visits, seminars and more, we strive to keep the learning curve increasing exponentially.
					We have always felt the need to work as a group and to achieve collective growth, an ideology that is widely cherished at PES University. This was the motivation behind the resurrection of the Student Branch.'''
		des16 = "Pesit's own newsletter by students. Published monthly."
		des17 = "Photography Club."


		Club.objects.create(club_id = "SM01", club_name = "Samarpana", contact_info = "Email id: ishdeep.94in@yahoo.in\nPhone number: +919008699817", objective = "An event to honor the martyr of the Indian Defense Forces.", description = des01)
		Club.objects.create(club_id = "AT02", club_name = "Aatmatrisha", contact_info = "Aman Tayyab\nCultural Secretary\n+91 95387 13111", objective = "Cultural festival of PES University.", description = des02)
		Club.objects.create(club_id = "OU03", club_name = "Ordell Ugo", contact_info = "http://research.pes.edu/contact", objective ="Virtual Company which works on real time Industry Projects.", description = des03)
		Club.objects.create(club_id = "NI04", club_name = "Ninaada", contact_info = "Name: Kuntal Nandi\nContact: 9899766431/9555166431\nEmail: k.nandi1803@gmail.com", objective = "Cultural night to promote Indian music, incorporates Spicmacy.", description = des04)
		Club.objects.create(club_id = "PR05", club_name = "Prakalpa", contact_info = "Address\nPES University, 100 Feet Ring Road, Banashankari 3rd Stage, Bangalore", objective = "A exhibition of all top projects of all departments displayed under one roof.", description = des05)
		Club.objects.create(club_id = "EC06", club_name = "E-Cell", contact_info = "Email id: pesitecell@gmail.com", objective = "Promoting of entrepreneurship.", description = des06)
		Club.objects.create(club_id = "SD07", club_name = "Student Nokia Developer", contact_info = "Email: support@studentnokiadeveloper.com", objective = "Conduct hashcode 24 hour hackathon.", description = des07)
		Club.objects.create(club_id = "OS08", club_name = "PES Open Source", contact_info = "website: pesos.pes.edu", objective = "Building India, Bit by Bit.", description = des08)
		Club.objects.create(club_id = "AY09", club_name = "Ayana", contact_info="Email:ayana@pes.edu\nPhone:+91 8095922529", objective = "24 hour Hackathon.", description = des09)
		Club.objects.create(club_id = "SN10", club_name = "Sanskriti", contact_info = "Contact: 9899766431/9555166431\nEmail: k.nandi1803@gmail.com", objective = "Indian Classical Dance Team", description = des10)
		Club.objects.create(club_id = "NA11", club_name = "Nautanki", contact_info = "Email id: nautankipes@gmail.com", objective = "Drama Team – Skits", description = des11)
		Club.objects.create(club_id = "PU12", club_name = "Pulse", contact_info = "Email id: pulse.pesit@gmail.com", objective = "Dance Team – Western", description = des12)
		Club.objects.create(club_id = "CR13", club_name = "CSR Club", contact_info = "Email id: pesitcsr@gmail.com", objective = "Social Responsibilities include adoption of Govt Schools, a blind School , environmental awareness, Blood Donation Camps, medical camps in villages.", description = des13)
		Club.objects.create(club_id = "PV14", club_name = "Paisa Vasool", contact_info = "Karthik - 9902204108\nArjun - 9916604094", objective = "Mad Ads – basically Skits, spoofs", description = des14)
		Club.objects.create(club_id = "IE15", club_name = "IEEE", contact_info ="Mrs. Divya Rao A\nEmail id: divyarao@pes.edu", objective = "The IEEE PESU Student Branch is a student – run professional body network at PES University under the worldwide IEEE banner.", description = des15)
		Club.objects.create(club_id = "PY16", club_name = "Papyrus", contact_info = "Ph No: 095359 69130", objective = "College Newspaper", description = des16)
		Club.objects.create(club_id = "PX17", club_name = "Pixels", contact_info = "Ph No: 081235 90013", objective = "Photography Club", description = des17)



		
		# to create users
		# to create club admins add extra field club_id="" while creating Signup object
		new_user = User.objects.create_user(username="1PI13CS099",password="ABC")
		new_user.save()
		Signup.objects.create(name="Neha M Kalibhat", email="neha.kalibhat@gmail.com", usn="1PI13CS099", dept="cse", phone="7829782761", sem="6", dob="1995-12-29")
		
		na = ["Anirudh Agarwal","Manisha Rachel Dawson","Mohit Mayank","Nagasundar","Navneet Singh","Niket Raj",
		 		"Parikshit Maheshwari","Prafful U M","Rohan Ds","Romasha Suman","Sharath K P","Smitha"]
		 		
		em = ["anirudhagarwal13@gmail.com","dawson.mrd@gmail.com","mohit.ritanil@gmail.com","nagasundarjogi@gmail.com",
		 		"jsr.navneet1@gmail.com","niketraj45@gmail.com","parikshit.maheshwari24@gmail.com","uprafful@gmail.com",
		 		"rohan0495@gmail.com","romasha.suman@gmail.com","sharathkp000@gmail.com",
		 		"smithagowdasmi@gmail.com"]

		un = ["CS199","CS085","CS091","CS097","CS098","CS100","CS103","CS108","CS125","CS126","CS141","CS161"]

		dep = ["cse","cse","cse","cse","eee","eee","eee","civil","civil","me","te","ece"]

		ph = ["8880527697","9535012206","9008696410","9036010289","8892111484","8867159511","9414170740","8892513147","9986180939","9886991554",
		 		"7259574777","9164958386"]

		db = ["1995-02-21","1995-09-17","1995-06-26","1995-08-24","1995-03-18","1995-04-16","1995-05-30","1995-10-30",
		 		"1995-04-26","1995-01-28","1995-11-11","1995-12-12"]

		for i in range(len(un)):
			new_user = User.objects.create_user(username="1PI13"+un[i],password="password")
			new_user.save()
			Signup.objects.create(name=na[i], email=em[i], usn="1PI13"+un[i], dept=dep[i], phone=ph[i], sem="6", dob=db[i])

		#admins
		new_user = User.objects.create_user(username="1PI12EE015",password="password")
		new_user.save()
		Signup.objects.create(name='Apoorv Jain', email='apoorv.jain@gmail.com', usn='1PI12EE015', dept='eee', phone=str(randomizer('phone')), sem=8, dob='1994-04-14', club_id='SM01')
		
		new_user = User.objects.create_user(username="1PI13ME015",password="password")
		new_user.save()
		Signup.objects.create(name='Aman Tayyab', email='aman.tayyab@yahoo.com', usn='1PI13ME015', dept='me', phone='9538713111', sem=8, dob='1994-03-15', club_id='AT02')
		
		new_user = User.objects.create_user(username="1PI12EC155",password="password")
		new_user.save()
		Signup.objects.create(name='Srikanta Somayaji', email='srikanta.somayaji@gmail.com', usn='1PI12EC155', dept='ece', phone=str(randomizer('phone')), sem=8, dob='1994-12-09', club_id='NI04')
		
		new_user = User.objects.create_user(username="1PI12TE055",password="password")
		new_user.save()
		Signup.objects.create(name='Akhila Parthasarathy', email='akhila.parthasarathy@gmail.com', usn='1PI12TE055', dept='te', phone=str(randomizer('phone')), sem=8, dob='1994-05-10', club_id='EC06')
		
		new_user = User.objects.create_user(username="1PI12CS121",password="password")
		new_user.save()
		Signup.objects.create(name='Ram Kashyap', email='ram.kashyap@gmail.com', usn='1PI12CS121', dept='cse', phone=8147558586, sem=8, dob='1994-06-11', club_id='SD07')
		
		new_user = User.objects.create_user(username="1PI13CS130",password="password")
		new_user.save()
		Signup.objects.create(name='Saimadhav Heblikar', email='saimadhavheblikar@gmail.com', usn='1PI13CS130', dept='cse', phone=9008442961, sem=6, dob='1995-05-31', club_id='OS08')
		
		new_user = User.objects.create_user(username="1PI12CS032",password="password")
		new_user.save()
		Signup.objects.create(name='Arvind Srikantan', email='arvindsri@yahoo.com', usn='1PI12CS032', dept='cse', phone=9591402872, sem=8, dob='1994-08-03', club_id='AY09')
		
		new_user = User.objects.create_user(username="1PI13BT088",password="password")
		new_user.save()
		Signup.objects.create(name='Preethi Sathyanandan', email='preethi.sathyanandan@yahoo.com', usn='1PI13BT088', dept='bt', phone=randomizer('phone'), sem=8, dob='1995-03-21', club_id='SN10')
		
		new_user = User.objects.create_user(username="1PI13IS002",password="password")
		new_user.save()
		Signup.objects.create(name='Abhigyan Nath', email='nath.abhigyan@gmail.com', usn='1PI13IS002', dept='ise', phone=randomizer('phone'), sem=6, dob='1995-01-02', club_id='NA11')
		
		new_user = User.objects.create_user(username="1PI13ME033",password="password")
		new_user.save()
		Signup.objects.create(name='Yash Sahai', email='yash.sahai@yahoo.com', usn='1PI13ME033', dept='me', phone=9663645597, sem=6, dob='1994-03-11', club_id='CR13')
		
		new_user = User.objects.create_user(username="1PI12ME161",password="password")
		new_user.save()
		Signup.objects.create(name='Siddharth Kadandale', email='siddharth.ks@gmail.com', usn='1PI12ME161', dept='me', phone=randomizer('phone'), sem=8, dob='1994-06-09', club_id='PV14')
		
		new_user = User.objects.create_user(username="1PI12CS055",password="password")
		new_user.save()
		Signup.objects.create(name='Karthik Kannapur', email='kkannapur@gmail.com', usn='1PI12CS055', dept='cse', phone=randomizer('phone'), sem=8, dob='1994-07-23', club_id='IE15')
		
		new_user = User.objects.create_user(username="1PI12EE123",password="password")
		new_user.save()
		Signup.objects.create(name='Sushanth Hegde', email='susanth.hegde@yahoo.com', usn='1PI12EE123', dept='eee', phone=8050163643, sem=8, dob='1994-01-13', club_id='PY16')
		
		new_user = User.objects.create_user(username="1PI12IS099",password="password")
		new_user.save()
		Signup.objects.create(name='Ravi Keerthi', email='ravi.keerthi@yahoo.com', usn='1PI12IS099', dept='ise', phone=8095019993, sem=8, dob='1994-11-25', club_id='PX17')
	
		# events
		samarpana_desc = 'Run for the soldiers, Run for those who safeguard you against enemies and conflict, Run for those who risk their flesh so that you can live in peace. Run for our Armed Forces.'
		Event.objects.create(club_id='SM01', event_id=1, event_name='Samarpana Run', event_date=str(timezone.now()), venue='PESU', contact_info='Email id: ishdeep.94in@yahoo.in\nPhone number: +919008699817', event_desc=samarpana_desc, no_part=3 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		at_desc = 'The techno-cultural fest of PES University, Bangalore.'
		Event.objects.create(club_id='AT02', event_id=1, event_name='Cultural Night', event_date=str(timezone.now()), venue='PESU', contact_info='Aman Tayyab\nCultural Secretary\n+919538713111', event_desc=at_desc, no_part=3 , no_reg=50, requirements="['name','email']")
		Event.objects.create(club_id='AT02', event_id=2, event_name='Pro Night', event_date=str(timezone.now()), venue='PESU', contact_info='Aman Tayyab\nCultural Secretary\n+919538713111', event_desc=at_desc, no_part=3 , no_reg=50, requirements="['name','email']")

		yamini_desc = 'An all night classical musical and dance experience.'
		Event.objects.create(club_id='NI04', event_id=1, event_name='Yamini', event_date=str(timezone.now()), venue='PESU', contact_info='Name: Kuntal Nandi\nContact: 9899766431/9555166431\nEmail: k.nandi1803@gmail.com', event_desc=yamini_desc, no_part=2 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		prakalpa_desc = 'Annual tech fair which showcases the best projects that PES has to offer.'
		Event.objects.create(club_id='PR05', event_id=1, event_name='Prakalpa \'15', event_date=str(timezone.now()), venue='PESU', contact_info='Address: PES University, 100 Feet Ring Road, Banashankari 3rd Stage, Bangalore', event_desc=prakalpa_desc, no_part=3 , no_reg=20, requirements="['name','email','phone']")

		endeavour_desc = 'Your chance to unveil the unique element to the world. Yes, we\'re back, bigger and better!'
		Event.objects.create(club_id='EC06', event_id=1, event_name='Endeavour', event_date=str(timezone.now()), venue='PESU', contact_info='Email id: pesitecell@gmail.com', event_desc=endeavour_desc, no_part=3 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		pesos_desc = 'A session on the game changers, contributions, communities, scope, opportunities and trends in open source. An enganging start to the journey of discovering the joys of open source.'
		Event.objects.create(club_id='OS08', event_id=1, event_name='Introduction to Open Source', event_date=str(timezone.now()), venue='Panini Seminar Hall, PESU', contact_info='Name: Saimadhav\nContact: 9008442961', event_desc=pesos_desc, no_part=3 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		ayana_desc = 'The hackathon you\'ve all been waiting for, is finally here! The theme for this year is "Building India, Bit by Bit". All you need are your laptops and the will to solve India\'s problems through technology. So clear your calendars and get ready for 24 hours of non stop coding, caffeine and fun!'
		Event.objects.create(club_id='AY09', event_id=1, event_name='Ayana 2016', event_date=str(timezone.now()), venue='PESU', contact_info='Email:ayana@pes.edu\nPhone: +918095922529', event_desc=ayana_desc, no_part=4 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		nautanki_desc = 'A skit performed by Nuatankians on the occasion of republic day.'
		Event.objects.create(club_id='NA11', event_id=1, event_name='Incredible India', event_date=str(timezone.now()), venue='PESU', contact_info='Email id: nautankipes@gmail.com', event_desc=nautanki_desc, no_part=3 , no_reg=50, requirements="['name','email','phone']")

		bdc_desc = 'Save lives. Donate Blood.'
		Event.objects.create(club_id='CR13', event_id=1, event_name='Blood Donation Camp', event_date=str(timezone.now()), venue='PESU', contact_info='Email id: pesitcsr@gmail.com', event_desc=bdc_desc, no_part=2 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		ieee_desc = 'Beat the test of time in answering logical and aptitude based questions to win exciting prizes.'
		Event.objects.create(club_id='IE15', event_id=1, event_name='The Quick Minute Challenge', event_date=str(timezone.now()), venue='PESU', contact_info='Venue: IEEE Stall', event_desc=ieee_desc, no_part=3 , no_reg=50, requirements="['name','email','phone','dept','sem']")

		pixels_desc = 'Show us your photography skills.'
		Event.objects.create(club_id='PX17', event_id=1, event_name='Layers', event_date=str(timezone.now()), venue='PESU', contact_info='Name: Sujai\nContact: 9008657564', event_desc=ieee_desc, no_part=3 , no_reg=50, requirements="['name','email']")
		
		# books: fill Seller table
		
		Seller.objects.create(book_name = "Let Us C", seller_id = Signup.objects.get(usn = "1PI13"+un[randint(0,len(un)-1)]), subject = "C Language")
		Seller.objects.create(book_name = "Introduction  to  The  Design  &  Analysis  of  Algorithms,  2nd  Edition,  Pearson  Education, 2007. ", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = " Design and Analysis of algorithms")
		Seller.objects.create(book_name = "Barry B Brey: The Intel Microprocessors ", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Microprocessor")
		Seller.objects.create(book_name = "Compilers-Principles, Techniques and Tools, Alfred V Aho, Monica S.Lam, Ravi Sethi, Jeffrey", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Compiler design ")
		Seller.objects.create(book_name = "Simulation Modeling and Analysis by Averill M. Law, W. David Kelton  ", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "System Modeling and Simulation")
		Seller.objects.create(book_name = "Discrete  and  Combinatorial  Mathematics,  5th  Edition,  Pearson  Education, 2004. ", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = " Graph Theory and Combinatorics")
		Seller.objects.create(book_name = "Fundamentals of Database SystemsElmasri and Navathe", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Data Base Management Systems")
		Seller.objects.create(book_name = "Theory of Computation: A Problem–Solving Approach, Kavi Mahesh", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Theory of Computation")
		Seller.objects.create(book_name = "Computer Networking ( A Top- down approach ), James F Kurose, Keith W", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Computer Networks -II")
		Seller.objects.create(book_name = "Software Engineering, Ian Somerville", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Software Engineering")
		Seller.objects.create(book_name = "Data Mining Concepts and Techniques", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Data Mining")
		Seller.objects.create(book_name = "Fundamentals of Multimedia , Ze-Nian Li and Mark", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Fundamentals of Multimedia")
		Seller.objects.create(book_name = "Multicore Programming, Increased Performance through Software Multi-threading", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Multi Core programming")
		Seller.objects.create(book_name = "Moving to the Cloud, Dinkar Sitaram", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Cloud Computing")
		Seller.objects.create(book_name = "Computer Security: Principles and practice", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Computer And Network Security")
		Seller.objects.create(book_name = "C++ Primer: Lippman", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Advanced C++")
		Seller.objects.create(book_name = "Java2, completet Reference", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Advanced Java Programming")
		Seller.objects.create(book_name = "Pattern Recognition and Machine Learning C Bishop, Springer Edition", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Applied Machine Learning")
		Seller.objects.create(book_name = "Operation Research- An Introduction", seller_id = Signup.objects.get(usn = "1PI13" + un[randint(0,len(un)-1)]), subject = "Operation Research")

		
		
