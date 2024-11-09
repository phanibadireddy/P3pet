from django.db import models

class register(models.Model):
    
    Name = models.CharField(max_length=20)
    phone = models.IntegerField()
    username = models.CharField(max_length=20,)
    mail = models.EmailField()
    password = models.CharField(max_length=20)
    purpose = models.CharField(max_length=20)
    def __str__(self):
        return self.Name
    
class ads(models.Model):
    owusername = models.CharField(max_length=20)
    ownername = models.CharField(max_length=20)
    phone = models.IntegerField()
    location = models.CharField(max_length=20)
    price = models.IntegerField()
    pet_type = models.CharField(max_length=100)
    pet_breed = models.CharField(max_length=100)
    pet_age = models.CharField(max_length=100)
    pet_color = models.CharField(max_length=100)
    pet_image1 = models.ImageField()
    pet_image2 = models.ImageField()
    pet_image3 = models.ImageField()
    def __str__(self):
        return self.ownername
class pay(models.Model):
    pname = models.CharField(max_length=20)
    cash =  models.IntegerField()
    
    def __str__(self):
        return self.pname
    
class Purchase(models.Model):
    bname = models.CharField(max_length=50)
    owname = models.CharField(max_length=50)
    itemname = models.CharField(max_length=20)
    cash = models.IntegerField()
    itembreed = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=50)
    
    def __str__(self):
        return self.bname
    
class Address(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    def __str__(self):
        return self.name
    
class DeliveryRequest(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    item = models.ForeignKey(ads, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class complaints(models.Model):
    user = models.CharField(max_length=20)
    rating = models.CharField(max_length=10)
    complaintname = models.CharField(max_length=20)
    complaintdesc = models.TextField(max_length=500)
    def __str__(self):
        return self.user