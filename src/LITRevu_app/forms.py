from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Entrez le titre du livre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Ajoutez une description détaillée'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire',
        }
        widgets = {
            'headline': forms.TextInput(attrs={'placeholder': 'Entrez un titre'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(6)]),
            'body': forms.Textarea(attrs={'placeholder': 'Ajoutez votre commentaire'}),
        }