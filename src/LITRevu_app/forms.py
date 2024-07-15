from django import forms
from .models import Ticket, Review
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-4 border-tertiary rounded-md w-96'
            ' text-center',
            'placeholder': 'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-4 border-tertiary rounded-md w-96'
            ' text-center',
            'placeholder': 'Mot de passe'})
    )


class registerForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border-4 border-tertiary rounded-md'
            'w-full text-center',
            'placeholder': 'Nom d\'utilisateur'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-4 border-tertiary rounded-md'
            'w-full text-center',
            'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-4 border-tertiary rounded-md'
            'w-full text-center',
            'placeholder': 'Confirmez le mot de passe'})
    )


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
            'title': forms.TextInput(attrs={
                'class': 'border-4 border-tertiary mt-2 w-11/12 font-semibold',
                'placeholder': 'Entrez le titre du livre'}),
            'description': forms.Textarea(attrs={
                'class': 'border-4 border-tertiary mt-2 w-11/12 font-semibold',
                'placeholder': 'Ajoutez une description détaillée'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'mt-2 hidden border-4 border-tiercary',
                'id': 'file-input',
            })
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
            'headline': forms.TextInput(attrs={
                'class': 'border-4 border-tertiary mt-2 w-11/12 font-semibold',
                'placeholder': 'Entrez un titre'}),
            'rating': forms.RadioSelect(
                choices=[(i, str(i)) for i in range(6)],
                attrs={
                    'class': 'flex flex-row space-x-20',
                    'id': 'id_rating',
                    }),
            'body': forms.Textarea(attrs={
                'class': 'border-4 border-tertiary mt-2 w-11/12 font-semibold',
                'placeholder': 'Ajoutez votre commentaire'}),
        }
