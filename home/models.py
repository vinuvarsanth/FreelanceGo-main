from django.db import models
from django.conf import settings

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=12,null=True,unique=True)
    def __str__(self):
        return self.name
    
def get_post_image_filepath(self, filename):
    return 'post_images/' + str(self.pk) + '/post_image.png'
    
class Posting(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200,null=True)
    abstract = models.TextField(null=True)
    detail_description = models.TextField(null=True)
    skills = models.CharField(max_length=200,null=True)
    budget = models.CharField(max_length=200,null=True)
    image = models.ImageField(max_length=255,upload_to=get_post_image_filepath,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
