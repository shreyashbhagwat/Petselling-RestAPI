from django.db import models
from django.contrib.auth.models import User
from .Choices import *
import uuid
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True, editable= False)
    updated_at = models.DateField(auto_now=True)
    uuid = models.UUIDField(default= uuid.uuid4 , primary_key= True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.category_name


class AnimalBreed(BaseModel):
    animal_breed = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.animal_breed

class Animalcolor(BaseModel):
    animal_color = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.animal_color

class Animal(BaseModel):
    animal_owner = models.ForeignKey(User , models.CASCADE , related_name= "animal")
    animal_category = models.ForeignKey(Category , models.CASCADE , related_name= "category")
    animal_views = models.IntegerField(default=0)
    animal_likes = models.IntegerField(default=1)
    animal_name = models.CharField(max_length=100)
    animal_description = models.TextField()
    animal_slug = models.SlugField(max_length=1000 , unique= True)
    animal_gender = models.CharField(max_length=50 , choices= Gender_choices)
    animal_breed = models.ManyToManyField(AnimalBreed , blank= True)
    animal_color = models.ManyToManyField(Animalcolor , blank= True)

    def incrementViews(self):
        self.animal_views += 1
        self.save()
    def incrementLikes(self):
        self.animal_likes += 1
        self.save()


    class Meta:
        ordering = ["-animal_name"]

    def __str__(self) -> str:
        return self.animal_name

class AnimalLocation(BaseModel):
    animal_model = models.ForeignKey(Animal , on_delete= models.CASCADE , related_name= "location")
    location = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.animal.animal_name} Location'

    

class AnimalImages(BaseModel):
    animal_model = models.ForeignKey(Animal , on_delete= models.CASCADE , related_name= "images")
    animal_images = models.ImageField(upload_to="animals")
    def __str__(self) -> str:
        return f'{self.animal.animal_name} Images'
    
    