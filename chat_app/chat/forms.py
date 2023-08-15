from django import forms

class ChatForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)