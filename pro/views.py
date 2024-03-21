import random
from urllib import request

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Import your custom user creation form
from .models import Customer  # Import your custom user model if you have one



def index(request):
    return render(request, "home.html")


def login(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username:
                messages.error(request, 'Please enter your username.')
                return render(request, 'login.html')

            if not password:
                messages.error(request, 'Please enter your password.')
                return render(request, 'login.html')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('home1')
            else:
                error_message = "Invalid username or password. Please try again."
                return render(request, 'login.html', {'error_message': error_message})
        else:
            return render(request, 'login.html')


from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            # If passwords don't match, return an error message
            return HttpResponse("Your password and confirm password do not match!!")
        else:
            # Check if the username or email already exists
            if User.objects.filter(username=uname).exists():
                return HttpResponse("Username already exists. Please choose a different one.")
            elif User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists. Please use a different one.")
            else:
                # Create the user and save it
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()

                # Send email
                subject = 'Registration Confirmation'
                message = 'Thank you for registering with us!'
                recipient = email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

                # Add a success message for email sent
                messages.success(request, 'Registration successful! Confirmation email has been sent.')

                # Redirect to the login page after successful registration
                return redirect('login')
    else:
        # If the request method is not POST, render the registration form
        return render(request, 'register.html')


def view(request):
    query = request.GET.get('q', '')

    availability_filter = request.GET.get('availability', 'all')
    buy_or_read_counter = {}
    books = [
        {
            'title': '1984',
            'author': 'George Orwell',
            'genre': 'Dystopian Fiction',
            'availability': 'Available',
            'Price': '350',
            'description': 'A chilling dystopian novel depicting a totalitarian regime and the struggle for freedom.',

            'icon': 'icon1.png'  # Icon file name for this book
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'genre': 'Fiction',
            'availability': 'Available',
            'Price': '460',
            'description': 'A classic tale of racial injustice and moral growth set in the American South.',

            'icon': 'icon2.png'  # Icon file name for this book
        },
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'genre': 'Classic Literature',
            'availability': 'Not Available',
            'Price': '250',
            'description': ' A story of wealth, love, and tragedy in the Jazz Age of America.',
            'icon': 'icon3.png',
            'pdf_filename': 'p1.pdf',
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'genre': 'Romance',
            'availability': 'Available',
            'Price': '350',
            'description': 'A timeless romance exploring societal expectations and the complexities of love.',
            'icon': 'icon4.png'  # Icon file name for this book
        },
        {
            'title': 'Harry Potter and the Sorcerer\'s Stone',
            'author': 'J.K. Rowling',
            'genre': 'Fantasy',
            'availability': 'Available',
            'Price': '350',
            'description': 'The enchanting beginning of a magical journey filled with friendship, courage, and adventure.',
            'icon': 'icon5.png'  # Icon file name for this book
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'genre': 'Literary Fiction',
            'availability': 'Available',
            'Price': '480',
            'description': ' A poignant exploration of teenage angst and alienation in post-World War II America.',
            'icon': 'icon6.png'  # Icon file name for this book
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'genre': 'Fantasy',
            'availability': 'Available',
            'Price': '320',
            'description': 'A whimsical tale of Bilbo Baggins unexpected journey to reclaim a lost treasure guarded by a dragon.',
            'icon': 'icon7.png'  # Icon file name for this book
        },
        {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'genre': 'Political Satire',
            'availability': 'Available',
            'Price': '240',
            'description': ' A satirical allegory depicting the corruption of power and the dangers of totalitarianism through the lens of farm animals.',
            'icon': 'icon8.png'  # Icon file name for this book
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'genre': 'Fantasy',
            'availability': 'Available',
            'Price': '370',
            'description': 'An epic fantasy saga chronicling the quest to destroy the One Ring and defeat the dark lord Sauron.',
            'icon': 'icon9.png'  # Icon file name for this book
        },
        {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'genre': 'Dystopian Fiction',
            'availability': 'Available',
            'Price': '320',
            'description': 'A dystopian vision of a future society where happiness is mandatory, but at what cost?',
            'icon': 'icon10.png'  # Icon file name for this book
        },
        {
            'title': 'The Chronicles of Narnia',
            'author': 'C.S. Lewis',
            'genre': 'Fantasy',
            'availability': 'Available',
            'Price': '350',
            'description': ' A timeless series of magical adventures and moral allegories set in the land of Narnia.',
            'icon': 'icon11.png'  # Icon file name for this book
        },
        {
            'title': 'Moby-Dick',
            'author': 'Herman Melville',
            'genre': 'Adventure',
            'availability': 'Available',
            'Price': '260',
            'description': 'An epic tale of obsession and revenge as Captain Ahab hunts the legendary white whale.',
            'icon': 'icon12.png'  # Icon file name for this book
        },
        {
            'title': 'The Picture of Dorian Gray',
            'author': 'Oscar Wilde',
            'genre': 'Gothic Fiction',
            'availability': 'NOT Available',
            'Price': '350',
            'description': 'A Gothic masterpiece exploring vanity, morality, and the consequences of eternal youth.',
            'icon': 'icon13.png',
            'pdf_filename': 'p2.pdf',

        },



        {
            'title': 'Frankenstein',
            'author': 'Mary Shelley',
            'genre': 'Gothic Fiction',
            'availability': 'Available',
            'Price': '350',
            'description': 'A groundbreaking work of science fiction exploring the ethical implications of creation and the pursuit of knowledge.',
            'icon': 'icon14.png'  # Icon file name for this book
        },
        {
            'title': 'Wuthering Heights',
            'author': 'Emily Bronte',
            'genre': 'Gothic Fiction',
            'availability': 'Available',
            'Price': '480',
            'description': ' A haunting tale of love, obsession, and revenge on the windswept moors of Yorkshire.',
            'icon': 'icon15.png'  # Icon file name for this book
        },
        {
            'title': 'The Adventures of Huckleberry Finn',
            'author': 'Mark Twain',
            'genre': 'Adventure',
            'availability': 'NOTAvailable',
            'Price': '450',
            'description': ' A classic adventure story of Huck Finn and Jim journey down the Mississippi River, confronting racism and injustice along the way.',
            'icon': 'icon16.png' ,
            'pdf_filename': 'p3.pdf',# Icon file name for this book
        },
        {
            'title': 'The Odyssey',
            'author': 'Homer',
            'genre': 'Epic Poetry',
            'availability': 'Available',
            'Price': '350',
            'description': ' An ancient Greek epic following the journey of Odysseus as he tries to return home after the Trojan War.',
            'icon': 'icon17.png'  # Icon file name for this book
        },
        {
            'title': 'The Road',
            'author': 'Cormac McCarthy',
            'genre': 'Post-Apocalyptic Fiction',
            'availability': 'Available',
            'Price': '650',
            'description': 'A bleak yet poignant tale of survival and love in a post-apocalyptic world.',
            'icon': 'icon18.png'  # Icon file name for this book
        },
        {
            'title': 'The Shining',
            'author': 'Stephen King',
            'genre': 'Horror',
            'availability': 'NOT Available',
            'Price': '550',
            'description': 'A chilling horror story of a family trapped in a haunted hotel, where darkness lurks around every corner.',
            'icon': 'icon19.png' ,
            'pdf_filename': 'p4.pdf',# Icon file name for this book
        },


        {
            'title': 'The Diary of a Young Girl',
            'author': 'Anne Frank',
            'genre': 'Biography/Autobiography',
            'availability': 'Available',
            'Price': '250',
            'description': 'The moving diary of a young Jewish girl hiding from the Nazis during World War II, offering a glimpse into the human spirit in the face of adversity.',
            'icon': 'icon20.png'  # Icon file name for this book
        },
        {
            'title': 'The Little Prince',
            'author': 'Antoine de Saint-Exupéry',
            'genre': 'Children\'s Literature',
            'availability': 'Available',
            'Price': '350',
            'description': ' Antoine de Saint-Exupérys enchanting tale navigates the wonders of childhood innocence and the complexities of human relationships, offering timeless wisdom.',
            'icon': 'icon21.png'  # Icon file name for this book
        },
        {
            'title': 'The Count of Monte Cristo',
            'author': 'Alexandre Dumas',
            'genre': 'Adventure',
            'availability': 'Available',
            'Price': '450',
            'description': ' Alexandre Dumas epic adventure unfolds in a tale of betrayal, revenge, and redemption, captivating readers with its thrilling narrative and intricate plot twists.',
            'icon': 'icon22.png'  # Icon file name for this book
        },
        {
            'title': 'Jane Eyre',
            'author': 'Charlotte Brontë',
            'genre': 'Gothic Fiction',
            'availability': 'Available',
            'Price': '350',
            'description': 'Charlotte Brontës classic Gothic novel delves into themes of love, independence, and societal constraints, weaving a compelling narrative of resilience and self-discovery.',
            'icon': 'icon23.png'  # Icon file name for this book
        },
        {
            'title': 'The Brothers Karamazov',
            'author': 'Fyodor Dostoevsky',
            'genre': 'Philosophical Fiction',
            'availability': 'Available',
            'Price': '150',
            'description': 'Fyodor Dostoevskys philosophical masterpiece explores the complexities of faith, morality, and free will, presenting a profound reflection on the human condition.',
            'icon': 'icon24.png'  # Icon file name for this book
        },
        {
            'title': 'Les Misérables',
            'author': 'Victor Hugo',
            'genre': 'Historical Fiction',
            'availability': 'Available',
            'Price': '350',
            'description': 'Victor Hugos sweeping historical epic follows the struggles of love, justice, and redemption amidst the backdrop of 19th-century France, resonating with themes of compassion and hope.',
            'icon': 'icon25.png'  # Icon file name for this book
        },
        {
            'title': 'The Bell Jar',
            'author': 'Sylvia Plath',
            'genre': 'Semi-autobiographical Fiction',
            'availability': 'Available',
            'Price': '250',
            'description': 'Sylvia Plaths semi-autobiographical novel delves into the depths of mental illness and societal pressures, offering a poignant exploration of identity and disillusionment.',
            'icon': 'icon26.png'  # Icon file name for this book
        },
        {
            'title': 'The Outsiders',
            'author': 'S.E. Hinton',
            'genre': 'Young Adult Fiction',
            'availability': 'Available',
            'Price': '350',
            'description': ' S.E. Hintons seminal work captures the tumultuous lives of teenagers navigating social divides and personal struggles, resonating with themes of friendship, loyalty, and belonging.',
            'icon': 'icon27.png'  # Icon file name for this book
        },
        {
            'title': 'The Secret Garden',
            'author': 'Frances Hodgson Burnett',
            'genre': 'Children\'s Literature',
            'availability': 'Available',
            'Price': '450',
            'description': 'Frances Hodgson Burnetts timeless childrens classic celebrates the healing power of nature and the transformative journey of self-discovery, inspiring generations with its enchanting narrative',
            'icon': 'icon28.png'  # Icon file name for this book
        },
        {
            'title': 'One Hundred Years of Solitude',
            'author': 'Gabriel García Márquez',
            'genre': 'Magical Realism',
            'availability': 'Available',
            'Price': '450',
            'description': 'Gabriel García Márquezs groundbreaking work of magical realism immerses readers in the mythical world of Macondo, weaving a multi-generational saga of love, loss, and the cyclical nature of time.',
            'icon': 'icon29.png'  # Icon file name for this book
        },
        {
            'title': 'మహా ప్రస్థానం',
            'author': 'Srirangam Srinivasarao',
            'genre': 'Poetry',
            'availability': 'Not Available',
            'Price': '350',
            'description': ': A profound poetic exploration of life journey and human emotions, penned by Srirangam Srinivasarao.',
            'icon': 'icon30.png' ,
            'pdf_filename': 'p5.pdf',# Icon file name for this book
        },
        {
            'title': 'అమ్మ యాత్ర',
             'author': 'Viswanatha Satyanarayana',
            'genre': 'Novel',
            'availability': 'Available',
            'Price': '250',
            'description': 'Viswanatha Satyanarayanas poignant narrative intricately weaves familial bonds and societal norms, evoking profound reflections.',
            'icon': 'icon31.png'  # Icon file name for this book
        },
        {
            'title': 'మందారం',
            'author': 'Chalam',
            'genre': 'Novel',
            'availability': 'Available',
            'Price': '450',
            'description': ' Chalams compelling narrative delves into the complexities of human relationships and societal constraints, offering a thought-provoking exploration.',
            'icon': 'icon32.png'  # Icon file name for this book
        },
        {
            'title': 'మైదానం',
            'author': 'Chalam',
            'genre': 'Novel',
            'availability': 'Available',
            'Price': '350',
            'description': 'Chalams insightful storytelling captures the essence of human aspirations and societal dynamics, presenting a compelling narrative of personal growth.',
            'icon': 'icon33.png'  # Icon file name for this book
        },
        {
            'title': 'మొగలు',
            'author': 'Gurram Jashuva',
            'genre': 'Poetry',
            'availability': 'Available',
            'Price': '200',
            'description': 'Gurram Jashuvas poetic collection mesmerizes with its evocative imagery and profound reflections, offering a glimpse into the human condition.',
            'icon': 'icon34.png'  # Icon file name for this book
        },
        {
            'title': 'The Hitchhiker\'s Guide to the Galaxy',
            'author': 'Douglas Adams',
            'genre': 'Science Fiction',
            'availability': 'Not Available',
            'Price': '350',
            'description': ' Douglas Adams witty narrative takes readers on an intergalactic journey filled with humor and existential ponderings.',
            'icon': 'icon35.png',
            'pdf_filename': 'p6.pdf',# Icon file name for this book
        },
        {
            'title': 'The Alchemist',
            'author': 'Paulo Coelho',
            'genre': 'Philosophical Fiction',
            'availability': 'Available',
            'Price': '250',
            'description': 'Paulo Coelhos timeless tale follows the journey of self-discovery and destiny, weaving a narrative of dreams, omens, and spiritual awakening.',
            'icon': 'icon36.png'  # Icon file name for this book
        },
        {
            'title': 'The Hunger Games',
            'author': 'Suzanne Collins',
            'genre': 'Dystopian Fiction',
            'availability': 'Available',
            'Price': '450',
            'description': 'Suzanne Collins gripping dystopian trilogy explores themes of survival, rebellion, and sacrifice in a world consumed by power and oppression.',
            'icon': 'icon37.png'  # Icon file name for this book
        },
        {
            'title': 'A Game of Thrones',
            'author': 'George R.R. Martin',
            'genre': 'Fantasy',
            'availability': 'Available',
            'Price': '550',
            'description': ' George R.R. Martins epic fantasy saga unfolds in a world of political intrigue, power struggles, and mythical creatures, captivating readers with its intricate plot.',
            'icon': 'icon38.png'  # Icon file name for this book
        },
        {
            'title': 'The Girl with the Dragon Tattoo',
            'author': 'Stieg Larsson',
            'genre': 'Crime Fiction',
            'availability': 'Available',
            'Price': '350',
            'description': 'Stieg Larssons riveting thriller intertwines complex characters, dark secrets, and investigative journalism, unraveling a web of intrigue and suspense.',
            'icon': 'icon39.png' # Icon file name for this book
        },
        {
            'title': 'The Girl on the Train',
            'author': 'Paula Hawkins',
            'genre': 'Thriller',
            'availability': 'Available',
            'Price':'350',
            'description': 'Paula Hawkins gripping psychological thriller follows the intertwined lives of three women, blurring the lines between truth and perception in a suspenseful narrative.',
            'icon': 'icon40.png'  # Icon file name for this book
        }

    ]


    # Assign random prices within the range to each book



        # Apply filtering logic
    filtered_books = books
    if availability_filter != 'all':
        filtered_books = [book for book in filtered_books if book['availability'] == availability_filter]

    if query:
        filtered_books = [book for book in filtered_books if query.lower() in book['title'].lower()]

    pdfs_dir = settings.STATIC_URL + 'pdfs/'

    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        # Logic for handling post request

    return render(request, 'view.html', {'books': filtered_books, 'query': query, 'pdfs_dir': pdfs_dir,
                                         'availability_filter': availability_filter})
def home1(request):
    # Your home1 view logic here
    return render(request, 'home1.html')

# views.py
from django.contrib.auth import logout
from django.shortcuts import render, redirect

def custom_logout(request):
    logout(request)
    return redirect('home')  # Assuming 'home' is the name of the URL pattern for home.html


def cart_view(request):
    # Retrieve book details from the request query parameters
    book_name = request.GET.get('book_name')
    author_name = request.GET.get('author_name')
    price = request.GET.get('price')  # Retrieve the price from the query parameters

    # Pass book details and price to the template context
    context = {
        'book_name': book_name,
        'author_name': author_name,
        'price': price
    }

    # Render the cart.html template with the provided context
    return render(request, 'cart.html', context)



def thank(request):
    # Logic for processing payment and order confirmation
    return render(request, 'thankyou.html')

# views.py

from django.shortcuts import render
from .models import Order


from django.shortcuts import render, redirect
from .forms import AddressForm  # Import your AddressForm from forms.py
from .models import Book  # Import your Book model

from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Book

from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Book


def whereabouts(request):
    # Process the address form data
    # Retrieve book details from the form data

    # Render the cart.html template with the provided context

    # Retrieve the book based on the provided details
    # Pass book details and price to the template context

    if request.method == 'POST':
          form = AddressForm(request.POST)
          return render(request, 'whereabouts.html')

    else:
          form = AddressForm()
          return render(request, 'whereabouts.html',context)


from django.shortcuts import render, redirect
from .forms import BookForm

from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book


def Addbook(request):
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                new_book = form.save()  # Save the form and get the newly added book object
                request.session['new_book_id'] = new_book.id  # Store the ID of the newly added book in session
                return redirect('view')  # Redirect to the view page after successfully adding the book
        else:
            form = BookForm()
        return render(request, 'Addbook.html', {'form': form})