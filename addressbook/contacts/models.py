from django.db import models

# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=20)
    state= models.CharField(max_length=2)
    zip = models.CharField(max_length=5)

    def __str__(self):
        return '\n'.join([self.street, self.city, self.state, self.zip])

class Contact(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)

    email = models.EmailField()

    def __str__(self):
        return ' '.join([self.fname, self.lname, self.email])
