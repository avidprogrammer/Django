from django.db import models

# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)

    def __str__(self):
        return '\n'.join([self.street, self.city, self.state, self.zip])

class Contact(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)

    email = models.EmailField()

    def __str__(self):
        return ' '.join([self.fname, self.lname, self.email])

class Bill(models.Model):
    IA = 'ItemA'
    IB = 'ItemB'
    IC = 'ItemC'
    ID = 'ItemD'
    IE = 'ItemE'

    ITEMS = ((IA, IA),
             (IB, IB),
             (IC, IC),
             (ID, ID),
             (IE, IE),
            )

    PRICES = {IA   : '10',
              IB   : '20',
              IC   : '30',
              ID   : '40',
              IE   : '50',
             }
    
    person_name  = models.CharField(max_length=25)
    company_name = models.CharField(max_length=25)
    ship_date = models.DateField()
    item = models.TextField(choices=ITEMS)
    price = PRICES.get(item, '0')
    
    def __str__(self):
        return ' '.join([self.person_name, 
                         self.company_name,
                         str(self.ship_date),
                         self.item])
