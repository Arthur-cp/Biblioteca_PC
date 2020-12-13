from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	publisher = models.CharField(max_length=100)
	genre = models.CharField(max_length=100)
	date_published = models.DateTimeField()
	quantity = models.IntegerField(default= 1)
	description = models.TextField(max_length=1000, help_text="Insira aqui uma breve descrição do livro" , default=' ')
	pic = models.ImageField(default='default_book.png', upload_to='book_image')


	def __str__(self):
		return self.title


class Borrower(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Book, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(null=True,blank=True)
    data_retorno = models.DateTimeField(null=True,blank=True)

    def get_absolute_url(self):
    	return reverse('book-detail', args=[str(self.id)])
       
    def __str__(self):
        return self.usuario.username+" pegou emprestado o livro: "+self.livro.title


