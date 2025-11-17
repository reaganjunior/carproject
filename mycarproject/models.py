
from django.db import models
from django.contrib.auth.models import User




class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Order(models.Model):
     
     STATUS_CHOICES = (
            ('Pending', 'Pending'),
           ('Delivered', 'Delivered'),
     ) 

     name = models.CharField(max_length=100)
     price = models.DecimalField(max_digits=10,decimal_places=1)
     location = models.CharField(max_length=100)
     fuel_type = models.CharField(max_length=50, default='petrol')
     mileage = models.CharField(max_length=50, default='0')
     transmission = models.CharField(max_length=50, default='manual')
     color = models.CharField(max_length=50, default='Black')
     year = models.IntegerField()
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') 
     buyer_name = models.CharField(max_length=100, default='reagan') 
     buyer_phone = models.CharField(max_length=15, default='+256 5685431')
     

  
     def __str__(self):
        return self.name





class Car(models.Model):
     

    
     name = models.CharField(max_length=100)
     price = models.DecimalField(max_digits=10,decimal_places=1)
     location = models.CharField(max_length=100)
     fuel_type = models.CharField(max_length=50, default='petrol')
     mileage = models.CharField(max_length=50, default='0')
     transmission = models.CharField(max_length=50, default='manual')
     color = models.CharField(max_length=50, default='Black')
     year = models.IntegerField()
     photo = models.ImageField(upload_to='images/',blank=False,default='icon.jpg')
    
     
 
    

     #def __str__(self):

        #return self.name
    



class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    number = models.CharField(max_length=20, blank=True, null=True) 
    message = models.TextField()
  

    def __str__(self):
        return f"Message from {self.full_name} ({self.email})"



class Admin(models.Model):
      admin_password = models.CharField(max_length=10)

      def __str__(self):
        return self.name
