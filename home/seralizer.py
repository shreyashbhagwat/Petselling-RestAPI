from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CategorySeralizer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = "__all__"

class AnimalBreedSeralizer(serializers.ModelSerializer):
    class Meta():
        model = AnimalBreed
        fields = "__all__"

class AnimalcolorSeralizer(serializers.ModelSerializer):
    class Meta():
        model = Animalcolor
        fields = "__all__"
class AnimalImagesSeralizer(serializers.ModelSerializer):
    class Meta():
        model = AnimalImages
        fields = "__all__"

class AnimalSeralizer(serializers.ModelSerializer):
    animal_category = serializers.SerializerMethodField()

    def get_animal_category(self, obj):
        return obj.animal_category.category_name
    
    def create(self, data):
        
        animal_name = data.pop('animal_name', None)
        animal_gender = data.pop('animal_gender', None)
        animal_breed = data.pop('animal_breed')
        animal_color = data.pop("animal_color")

        for ab in animal_breed:
            animal_breed_obj = AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
            animal.animal_breed.add(animal_breed_obj)
        
        for ac in animal_color:
            animal_color_obj = Animalcolor.objects.get(animal_color = ac['animal_color'])
            animal.animal_color.add(animal_color_obj)
        

        
        animal = Animal.objects.create(animal_name=animal_name, animal_gender=animal_gender, **data,animal_category= Category.objects.get(category_name="Dog"))
        
        
        return animal
    
    def update(self , request , data):
        if "animal_breed" in data:
           animal_breed = data.pop('animal_breed')
           isinstance.animal_breed.all().clear()
           for ab in animal_breed:
            animal_breed_obj = AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
            isinstance.animal_breed.add(animal_breed_obj)
        

        if "animal_color" in data:
           animal_color = data.pop('animal_color')
           isinstance.animal_color.all().clear()
           for ac in animal_color:
            animal_color_obj = AnimalBreed.objects.get(animal_color=ac['animal_color'])
            isinstance.animal_breed.add(animal_color_obj)
           
        
        isinstance.animal_name= data.get("animal_name" ,isinstance.animal_name )
        isinstance.animal_description = data.get("animal_description",isinstance.animal_description)
        isinstance.animal_gender = data.get("animal_gender",isinstance.animal_gender)


    class Meta:
        model = Animal
        

        

class AnimalLocationSeralizer(serializers.ModelSerializer):
    class Meta():
        model = AnimalLocation
        fields = "__all__"


class RegisterSeralizer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    def valid(self, data):
        if 'username' in data:
            user = User.objects.filter(username = data['username'])
            if user.exists():
                raise serializers.ValidationError("Username is already taken")
        
        if 'email' in data:
            user = User.objects.filter(username = data['email'])
            if user.exists():
                raise serializers.ValidationError("email is already taken")
        
        return data

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']  

class LoginSeralizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def valid(self, data):
        username = data.get('username')
        if username:
            user = User.objects.filter(username=username)
            if not user.exists():
                raise serializers.ValidationError("Username does not exist. Please check your username or register.")
        return data
