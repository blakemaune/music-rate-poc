from django import forms
from .models import Album, Rating

class SearchForm(forms.ModelForm):
	name = forms.CharField(required=False)
	artist = forms.CharField(required=False)
	class Meta:
		model = Album
		fields = ('name', 'artist')

class RatingForm(forms.ModelForm):
	class Meta:
		model = Rating
		fields = ('value', 'comment')

class SearchResult(forms.Form):
	name = forms.CharField()
	img = forms.CharField()