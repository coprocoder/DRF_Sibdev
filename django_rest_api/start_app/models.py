from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datafile = models.FileField(upload_to='')
    # owner = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    # description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.created) #+ str(self.datafile)

class Deal(models.Model):
    customer = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    total = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return str(self.customer)

# For additional modules (не по ТЗ)
class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

# For additional modules (не по ТЗ)
class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('Author', related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.title