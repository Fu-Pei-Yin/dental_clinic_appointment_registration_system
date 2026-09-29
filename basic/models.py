from django.db import models
# Create your models here.
class Info(models.Model):
    user_name=models.CharField(max_length=20)
    user_ID=models.CharField(max_length=10)
    user_secret=models.CharField(max_length=20)
    user_address=models.CharField(max_length=50)
    user_tel=models.CharField(max_length=15)
    user_birth=models.DateTimeField()
    can_manage=models.BooleanField(default=False)
    identities=[['normal','一般身份'],['veterans','退伍軍人'],['disability','領有殘障手冊']]
    user_identity=models.CharField(max_length=15,choices=identities)
    def __str__(self):
        return self.user_name
class Service(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.IntegerField(default=150)
    def __str__(self):
        return self.name
class Schedule(models.Model):
    time=models.CharField(max_length=20,default='無')
    def __str__(self):
        return self.time
class Dentist(models.Model):
    name=models.CharField(max_length=100)
    services=models.ManyToManyField(Service,blank=True,related_name="dentists")
    time=models.ManyToManyField(Schedule,blank=True,related_name="dentists")
    def __str__(self):
        return self.name
class Contact(models.Model):
    name=models.CharField(max_length=50,)
    email=models.EmailField()
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name