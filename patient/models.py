from django.db import models
from basic.models import Dentist,Service

# Create your models here.
class Register(models.Model):
    patient_name=models.CharField(max_length=20)
    dentist=models.ForeignKey(Dentist,on_delete=models.CASCADE,db_constraint=False,default=1)
    service=models.ForeignKey(Service,on_delete=models.CASCADE,db_constraint=False,default=1)
    appointment_date=models.DateField()
    def __str__(self):
        return self.patient_name