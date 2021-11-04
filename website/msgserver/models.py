from django.db import models
from django.core.exceptions import ValidationError
from msgserver import constants


#Ensures we have a min message length of 1. Max message length is checked again in the Message class(model) for max length
def validate_message_range(value):
    if len(value) < constants.MIN_MESSAGE_LENGTH:
        raise ValidationError('Out of range', code='message_length')

#Ensures our key is exactly KEY_LENGTH chars long (8) and that it's a key of only alphanum chars
def validate_key_range(value):
    if len(value) != constants.KEY_LENGTH:
        raise ValidationError('Key must be 8 chars long', code='KEY_length') 
    if value.isalnum() == False:
        raise ValidationError('Key must be alphanumeric', code='KEY_type')  


#Our database model class. At this moment, we use our dict key also as our unique primary key (sql)
#if we were to add more database cols to the message class, we would do it here. 
class Message(models.Model):
    message = models.CharField(max_length=160, validators=[validate_message_range])
    key = models.CharField(max_length=8, unique=True, primary_key=True,validators=[validate_key_range])

    def __str__(self):
        return str(self.message) + ',' + str(self.key) 

# Create your models here.
