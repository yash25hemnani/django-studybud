# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
        ]
    return Response(routes)
    # return JsonResponse(routes, safe = False)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all() #Python List
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data) # Response can pass dictionaries

@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(id=pk) #Python List
    serializer = RoomSerializer(rooms, many = False)
    return Response(serializer.data) # Response can pass dictionaries
