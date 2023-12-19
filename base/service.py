import traceback

from .models import User, FriendRequest, Status
from .utils import custom_response_obj, get_user, HTTPResponse
from .serializer import SendFriendRequestSerializer, FriendRequestSerializer

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta

from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauthlib import common

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LoginService:
    """Login Service class to handle User Authentication and access token generation"""

    def user_authentication(self, email, password):
        try:
            username = User.objects.get(email=email)
            correct_password = username.check_password(password)
            if correct_password:
                return self.__generate_token(username)
            else:
                return {'status': 'error', 'response': 'Wrong email or password', 'code':400}

        except ObjectDoesNotExist:
            print('user doesnot exist')
            return {'status': 'error', 'response': 'User does not exist', 'code':404}
        except Exception as e:
            traceback.print_exc()
            print('exception while login', e)
            return {'status': 'error', 'response': 'Internal server error','code':500}


    def __generate_token(self, user):
        application = Application.objects.all()[:1]
        expires = timezone.now() + timedelta(seconds=3600) # 1 hour
        current_token = common.generate_token()
        refresh_token = common.generate_token()
        access_token = AccessToken(
            user=user,
            scope='',
            expires=expires,
            token=current_token,
            application=application[0]
        )
        access_token.save()
        refresh_token_data = RefreshToken(
            user=user,
            token=refresh_token,
            application=application[0],
            access_token=access_token
        )
        refresh_token_data.save()
        user.last_login=timezone.now()
        user.save(update_fields=['last_login'])
        return {'status': 'success','access_token': current_token, 'refresh_token': refresh_token, 'expiry': expires,'user':user.username,'first_name':user.first_name, "code":200}





class FriendRequestService:
    """Friend Request Service class to manage send/accept/reject friend requests"""

    def __init__(self, data=None):
        self.__data = data

    def __check_to_user(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return False
        
    def __check_from_user(self, from_user):
        return get_user(from_user)

    def send_request(self, from_user):
        to_user = self.__check_to_user(email=self.__data.get('to_user'))

        if not to_user:
            return HTTPResponse(404).not_found("User does not exist")
        
        if not self.__check_from_user(from_user):
            return HTTPResponse(401).unauthorized('User Unauthorised')
        
        __current_time = timezone.now()
        __minute_ago = __current_time - timedelta(minutes=1)

        recent_requests_count = FriendRequest.objects.filter(
            from_user=from_user,
            created_at__gte=__minute_ago,
            created_at__lte=__current_time
        ).count()

        if recent_requests_count >= 3:
            return Response({
                "status_code": 429,
                "status": "error",
                "response": "You've reached the limit for sending friend requests in a minute."}, 429
                )  
        
        existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
        if existing_request:
            return HTTPResponse(400).bad_request(f"Friend request already exists and is {existing_request.status}.")
        
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return HTTPResponse(200).success_response(f"Friend request sent to {to_user.email}")
        
    def accept_request(self, user, pk):

        pending_request = user.received_requests.filter(
            id=pk,status=Status.pending.value).only('status').first()
        if pending_request:
            pending_request.status = Status.accepted.value
            pending_request.save()
            return HTTPResponse(200).success_response("Friend request Accepted")
        
        return HTTPResponse(404).not_found("Friend Request not found")
    
    def reject_request(self, user, pk):

        pending_request = user.received_requests.filter(
            id=pk,status=Status.pending.value).only('status').first()
        
        if pending_request:
            pending_request.delete()
            """we can do this either ways: delete a rejected request so that user can request again or save it with a rejected status for the records:
            `pending_request.status = Status.rejected.value`
            `pending_request.save()`"""
            return HTTPResponse(200).success_response("Friend request Rejected")
        
        return HTTPResponse(404).not_found("Friend Request not found")

        
    def get_all_pending_requests(self, user):
        
        pending_requests = user.received_requests.filter(status=Status.pending.value)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return HTTPResponse(200).success_response(serializer.data)
        

    def list_friends(self, user):

        friends = user.sent_requests.filter(status=Status.accepted.value)
        serializer = FriendRequestSerializer(friends, many=True)
        return HTTPResponse(200).success_response(serializer.data)
    
        



        
