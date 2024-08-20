from django import forms
from .models import Message 

class SendMessageForm(forms.ModelForm):
    body= forms.CharField(widget= forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Message...'}), required= True)
    
    class Meta:
        model= Message
        fields= ['body']