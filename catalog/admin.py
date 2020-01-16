from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

class BookAdminInline(admin.TabularInline):
    model=Book

class AutorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BookAdminInline]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display= ('book','id','status','borrower','due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )


#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Author,AutorAdmin)
admin.site.register(Genre)
#admin.site.register(BookInstance)