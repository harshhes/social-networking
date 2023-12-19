from django.db.models import Q

from .models import User, FriendRequest
from .serializer import (
    RegisterUserSerializer,
    ListUsersSerializer,
    UserSerializer,
    SendFriendRequestSerializer
    )
from .service import LoginService, CustomPagination, FriendRequestService
from .utils import HTTPResponse, get_user

from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import serializers


class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()



class LoginUserView(APIView):
    def post(self, request, *args):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        __service = LoginService().user_authentication(email=email, password=password)

        return Response(__service, __service['code'])



class ListUsersView(ListAPIView):
    serializer_class = ListUsersSerializer
    queryset = User.objects.all()
    permission_classes =  (IsAuthenticated, IsAdminUser)


class SearchUserView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def post(self, request):
        data = request.query_params.get('q',"")
        exact_match = User.objects.filter(Q(email=data) | Q(first_name=data) | Q(last_name=data)).first()
        if exact_match:
            serializer = UserSerializer(exact_match)
            return Response(serializer.data, 200)

        name_containing_users = User.objects.filter(Q(first_name__icontains=data) | Q(last_name__icontains=data))[:10]
        
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(name_containing_users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class SendFriendRequestView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        from_user = request.user
        __service = FriendRequestService(data)
        return __service.send_request(from_user)
        
    
class AcceptFriendRequestView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, pk=None):

        user = get_user(request.user)
        pk = self.kwargs.get('pk')
        return FriendRequestService().accept_request(user=user, pk=pk)


class RejectFriendRequestView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, pk=None):

        user = get_user(request.user)
        pk = self.kwargs.get('pk')
        return FriendRequestService().reject_request(user=user, pk=pk)


class PendingRequestsView(GenericAPIView):
    """List Pending Requests"""
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None):
        user = get_user(request.user)
        return FriendRequestService().get_all_pending_requests(user)
    

class AcceptedRequestsView(GenericAPIView):
    """View responsible for generating List of Friends"""
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None):
        user = get_user(request.user)
        return FriendRequestService().list_friends(user)
    

