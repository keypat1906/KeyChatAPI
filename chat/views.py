from django.contrib.auth.models import User
from chat.models import Message, UserProfile
from chat.serializers import MessageSerializer, UserSerializer
from rest_framework import viewsets, status, mixins, filters

from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework.decorators import api_view

from chat.utils import EventCustomPagination


@api_view(('GET','POST',))
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        print(data)
        try:
            user = User.objects.create_user(username=data['username'])
            UserProfile.objects.create(user=user)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({'error': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
def message_all(request):
    """
    This function return all the recent messages 
    """

    paginator = EventCustomPagination(request)
    last_month = datetime.today() - timedelta(days=30)
    messages = Message.objects.filter(timestamp__gte=last_month)
    page = paginator.paginate_queryset(messages, request)

    serializer = MessageSerializer(page, many=True, context={'request': request})
    for message in messages:
        message.is_read = True
        message.save()

    return paginator.get_paginated_response(serializer.data)


@api_view(('GET','POST'))
def message_list(request, receiver=None, sender=None):
    """
    List recent message for a specific sender and create a new message.
    """
    if request.method == 'GET':
        paginator = EventCustomPagination(request)
        last_month = datetime.today() - timedelta(days=30)

        if User.objects.filter(id=receiver).exists() and User.objects.filter(id=sender).exists():
            messages = Message.objects.filter(sender_id=sender, receiver_id=receiver).filter(timestamp__gte=last_month)
        else:
            return Response("receiver or sender not found",status=status.HTTP_404_NOT_FOUND)


        page = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(page, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return paginator.get_paginated_response(serializer.data)


    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



