from django import forms

class Form(forms.Form):
        name=forms.CharField(widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'placeholder':'Enter your name'
            }
        ))
        birthYear=forms.IntegerField(widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'placeholder':'Enter your year of birth',
            'type':'number'
            }
        ))
        gender=forms.CharField(widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'placeholder':'Enter "male" or "female" '
            }
        ))
#-------------------------------------------------------------------------------------------------------------------------------------------------
class SearchForm(forms.Form):
        text=forms.CharField(widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'placeholder':'Enter text eg: I have a back pain. Please be specific.',
            'size':45
            }
        ))
