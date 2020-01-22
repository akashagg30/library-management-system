from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

student_choices=[
        ('un','username'),
        #('id','id'),
        ('fn','first name'),
        #('n','full name')
        ]

book_choices=[
        ('book name','book name'),
        ('author','author name'),
        #('genre','genre'),
        #('book instance id','book instance id')
        ]

class RenewBookForm(forms.Form):
    renewal_date=forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    
    def clean_renewal_date(self):
        data=self.cleaned_data['renewal_date']
        
        if data <datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
            
        return data
    
class SearchStudent(forms.Form):
    choice=forms.CharField(label='search student by ',widget=forms.Select(choices=student_choices))
    name=forms.CharField(label='')
    
class SearchBook(forms.Form):
    choice=forms.CharField(label='search book by ',widget=forms.Select(choices=book_choices))
    name=forms.CharField(label='')
    