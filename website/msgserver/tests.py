from django.test import TestCase
from msgserver.models import Message
from msgserver import constants

# Create your tests here.

class MessageTestCase(TestCase):

    def test_valid_create(self):
        response = self.client.post("/msgserver/create/" , {'message':'this is an allowable message' , 'key': '1234567a' })
        createdMessage = Message.objects.get(key='1234567a')
        self.assertEqual(createdMessage.message, 'this is an allowable message')
        self.assertEqual(createdMessage.key, '1234567a')

    def test_get_valid_message(self):
        response = self.client.post("/msgserver/create/" , {'message':'this is an allowable message' , 'key': '1234567a' })
        response = self.client.get("/msgserver/get/1234567a/")
        msg = response.content
        self.assertEqual(msg, b'Key is 1234567a and message is this is an allowable message ')


    def test_key_already_exists(self):
        response = self.client.post("/msgserver/create/" , {'message':'this is an allowable message' , 'key': '1234567a' })
        createdMessage = Message.objects.get(key='1234567a')
        response = self.client.post("/msgserver/create/" , {'message':'this message should not save' , 'key': '1234567a' })
        self.assertFormError(response, 'form', 'key' , 'Message with this Key already exists.') 



## UPDATE TEST ##
# 
    def test_valid_update(self): #################################
        response = self.client.post("/msgserver/create/" , {'message':'this is a message' , 'key': '1234567b' })
        #print(response.content)
        createdMessage = Message.objects.get(key='1234567b')
        response = self.client.post("/msgserver/update/1234567b" , {'message':'THIS MESSAGE GOT UPDATED'})
        #print(response._container[0])
        newMessage = Message.objects.get(key='1234567b')
        self.assertEqual(newMessage.message, 'THIS MESSAGE GOT UPDATED')
        self.assertEqual(newMessage.key, '1234567b')


##testing invalid keys here. You are unable to enter a key longer than 8 chars on the form ##
    def test_key_with_symbol(self):
        response = self.client.post("/msgserver/create/" , {'message':'this is a test message' , 'key': '12345$79' })
        self.assertFormError(response, 'form', 'key', 'Key must be alphanumeric')  
        # [params? where the error is, what caused the error, and what the error should be?] 

    def test_key_too_short(self):
        response = self.client.post("/msgserver/create/" , {'message':'this is a test message' , 'key': '1234579' })  ##add more key length tests
        self.assertFormError(response, 'form', 'key', 'Key must be 8 chars long')  


    def test_message_too_short(self):
        response = self.client.post("/msgserver/create/" , {'message':'' , 'key': '1234567b' })
        self.assertFormError(response, 'form', 'message', 'This field is required.')  
        

    def test_message_too_long(self):
        toSend = 'this is a message that tests length. It has to be at least 160 chars long, which is quite a lot of chars. Imagine you are writing a funny story to your best friend over text message. It is going to be a whole novel!'
        response = self.client.post("/msgserver/create/" , {'message':toSend, 'key': '1234567b' })
        self.assertFormError(response, 'form', 'message', 'Ensure this value has at most 160 characters (it has ' + str(len(toSend)) + ').'  )  

    ##CHECK FOR JSON FORMAT ##
    
    def test_for_formatting(self):
        response = self.client.post("/msgserver/create/" , {'message':'A Message' , 'key': '1234567c' })
        response = self.client.get("/msgserver/")
        msg = response.content
        self.assertEqual(msg, b'[{"model": "msgserver.message", "pk": "1234567c", "fields": {"message": "A Message"}}]')
