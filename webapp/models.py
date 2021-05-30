from django.db import models


class Person (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Phone (models.Model):
    phone_number = models.CharField(max_length=16)
    active = models.BooleanField(default=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number

