from django.forms import ModelForm
from .models import Room, Message
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room # Specify which model the form is for
        fields = '__all__' # Will generate a form with all fields as there were in the table
        # You can either use a list to specify which form items you want or you can use the
        # exclude method to remove specific elements of the form
        exclude = ['host', 'participants']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']