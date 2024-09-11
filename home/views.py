from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import *
from .seralizer import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permission import *
# Create your views here.


class AnimalDetailsViews(APIView):
    def get(self, request, pk):

        try:
            
            queryset = get_object_or_404(Animal, pk=pk)
            queryset.incrementViews()  
            serializer = AnimalSeralizer(queryset)
            return Response({'status': True, 'message': "Animal fetched with GET", "data": serializer.data})

        except Exception as e:
            print(e) 
            return Response({"status": 500, 'message': "Failed to fetch animal with GET", "data": {}})



class AnimalView(APIView):

    def get(self , request):
        queryset = Animal.objects.all()

        if request.GET.get('search'):
            search = request.GET.get('search')
            queryset = queryset.filter(
                Q(animal_description__icontains = search) |
                Q(animal_gender__iexact = search) |
                Q(animal_breed__animal_breed__icontains = search)

            )



        serializers = AnimalSeralizer(queryset , many = True)
        return Response({'status': True , 'message' : "Animal Fetch with GET" , "data":serializers.data})
    
    
class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSeralizer(data=data)
            if serializer.is_valid():
                user = User.objects.create(
                    username = serializer.data['username'],
                    email = serializer.data['email']
                )
                user.set_password(serializer.data['password'])
                user.save()

                  
                return Response({
                    "Status": 200,
                    "Message": "Account created",
                    "data": {}
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "Status": 500,
                    "Message": "Invalid details",
                    "data": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "Status": 500,
                "Message": "An error occurred",
                "Error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPI(APIView):
    
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSeralizer(data=data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username, password=password)

                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({
                        'message': 'Login successfully',
                        'data':{
                            'token' : str(token)
                        }
                    })
                else:
                    return Response({
                        "Status": False,
                        "Message": "Invalid username or password"
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    "Status": False,
                    "Message": "Invalid data",
                    "Errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "Status": 500,
                "Message": "An error occurred",
                "Error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AnimalCreateAPI(APIView):
    permission_classes = [IsAuthenticated , IsPetOwnerPermission]
    authentication_classes = [TokenAuthentication]

    def get(self , request):
        queryset = Animal.objects.filter(animal_owner = request.user)

        if request.GET.get('search'):
            search = request.GET.get('search')
            queryset = queryset.filter(
                Q(animal_description__icontains = search) |
                Q(animal_gender__iexact = search) |
                Q(animal_breed__animal_breed__icontains = search)

            )



        serializers = AnimalSeralizer(queryset , many = True)
        return Response({'status': True , 'message' : "Animal Fetch with GET" , "data":serializers.data})

    def post(self, request):
        try:
            data = request.data
            data['animal_owner'] = request.user.id
            serializer = AnimalSeralizer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Animal Created",
                    "data": serializer.data
                })
            return Response({
                "status": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": False,
                "message": "An error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self , request):
        try:
            data = request.data
            if data.get('id') is None:
                return Response({
                    "status": False,
                    "message": "Animal Id  required",
                    "data": {}
                })
            animal_obj = Animal.objects.filter(id = data.get('id'))

            if not animal_obj.exists():
                return Response({
                    "status": False,
                    "message": "invalid animal id",
                    "data": {}
                })
            
            animal_obj = animal_obj.first()
            self.check_object_permissions(request ,animal_obj )

            serializer = AnimalSeralizer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "Updated Animal",
                    "data": serializer.data
                })
            return Response({
                "status": False,
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": False,
                "message": "An error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
