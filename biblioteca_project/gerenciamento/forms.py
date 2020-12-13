from django import forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrower
        exclude = ['data_emprestimo', 'data_retorno']