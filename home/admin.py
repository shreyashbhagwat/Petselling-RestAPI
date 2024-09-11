from django.contrib import admin
from .models import *

# admin.site.register(Category)
# admin.site.register(AnimalBreed)
# admin.site.register(Animalcolor)
# admin.site.register(Animal)
# admin.site.register(AnimalLocation)
# admin.site.register(AnimalImages)

models = [Category ,AnimalBreed , Animalcolor , Animal ,AnimalLocation , AnimalImages ]


for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass