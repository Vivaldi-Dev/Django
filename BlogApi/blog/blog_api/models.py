from django.db import models

class post(models.Model):
    title = models.CharField(max_length=255)
    Slug = models.SlugField()
    author = models.TextField(default="Anonymous") 
    intro = models.TextField()
    body =  models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to='imagess/')
 


def __str__(self):
        return self.title