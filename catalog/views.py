import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm,SearchStudent,SearchBook

def index(request):
    """View function for home page of site."""
    form_student=SearchStudent()
    form_book=SearchBook()

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    num_genre=Genre.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre':num_genre,
        'num_visits': num_visits,
        'form_student':form_student,
        'form_book':form_book,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/' )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'bookinstance_list': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

def search_student(request):
    if(request.GET.get('choice')=='un'):
        book_instance = BookInstance.objects.filter(borrower__username__icontains=request.GET.get('name')).order_by('due_back')
        return render(request,'catalog/bookinstance_list_borrowed_user.html',{'bookinstance_list':book_instance})
    elif request.GET.get('choice')=='id':
        book_instance = BookInstance.objects.filter(borrower__username__icontains=request.GET.get('name')).order_by('due_back')
        return render(request,'catalog/bookinstance_list_borrowed_user.html',{'bookinstance_list':book_instance})
    elif request.GET.get('choice')=='fn':
        book_instance = BookInstance.objects.filter(borrower__first_name__icontains=request.GET.get('name')).order_by('due_back')
        return render(request,'catalog/bookinstance_list_borrowed_user.html',{'bookinstance_list':book_instance})
    elif request.GET.get('choice')=='n':
        book_instance = BookInstance.objects.filter(borrower__username__icontains=request.GET.get('name')).order_by('due_back')
        return render(request,'catalog/bookinstance_list_borrowed_user.html',{'bookinstance_list':book_instance})
    else:
        print('kuch nhi hua ;_;')
        return HttpResponseRedirect('/' )
    
def search_book(request):
    data=request.GET.get('name')
    if(request.GET.get('choice')=='book name'):
        link=reverse('book-detail', args=[str(Book.objects.get(title__icontains=data).id)])
        return HttpResponseRedirect(link)
    elif request.GET.get('choice')=='author':
        link=reverse('book-detail', args=[str(Book.objects.get(author__first_name__icontains=data).id)])
        return HttpResponseRedirect(link)
    #still to work on genre and book instance id
    elif request.GET.get('choice')=='genre':
        book_instance = BookInstance.objects.filter(borrower__first_name__icontains=data).order_by('due_back')
        return render(request,'catalog/bookinstance_list_borrowed_user.html',{'bookinstance_list':book_instance})
    elif request.GET.get('choice')=='book instance id':
        book_instance = BookInstance.objects.filter(borrower__username__icontains=data).order_by('due_back')
        return render(request,'catalog/bookinstance_list_borrowed_user.html',{'bookinstance_list':book_instance})
    else:
        print('kuch nhi hua ;_;')
    return HttpResponseRedirect('/' )

def genre_extended(request,name):
    if '%' in name:
        temp=''
        f=0
        for i in name:
            if i=='%':
                temp+=' '
                f=1
            elif f==0:
                temp+=i
            elif f==3:
                temp+=i
                f=0
            else:
                f+=1
        name=temp
    genre=Genre.objects.filter(master__name__icontains=name)
    c=0
    for _ in genre:
        c+=1
    if c!=0:
        return render(request,'catalog/genre_list.html',{'genre_list':genre})
    else:
        return HttpResponseRedirect('/' )
    
from django.views import generic
    
    
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    queryset = Book.objects.all() # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BookDetailView(generic.DetailView):
    model = Book
    
    
class AuthorListView(generic.ListView):
    model=Author
    paginate_by=10
    
    
class AuthorDetailView(generic.DetailView):
    model=Author

class GenreListView(generic.ListView):
    model=Genre
    paginate_by=10  
    
    def get_context_data(self, **kwargs):
        context = super(GenreListView, self).get_context_data(**kwargs)
        context['genre_list'] = Genre.objects.filter(master__isnull=True)
        return context
