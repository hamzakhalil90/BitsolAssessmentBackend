from apps.baselayer.baseauthentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers import UserDetailSerializer, UserListingSerializer
from apps.users.models import User
from apps.baselayer.baseapiviews import BaseAPIView, get_first_error_message_from_serializer_errors
from apps.baselayer.base_pagination import paginate_data
from apps.baselayer.utils import get_query_param
from apps.baselayer.response_messages import *
from django.contrib.auth.hashers import make_password
from apps.baselayer.utils import generate_password, send_email
from User_Management_Backend.settings import EMAIL_HOST_USER


class UserAPIView(BaseAPIView):
    """
    User endpoint to manage CRUDs
    """
    # authentication_classes = [BaseAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get_serializer(self, api_type):
        return UserListingSerializer if api_type == "list" else UserDetailSerializer

    def get_password(self):
        password = generate_password(8)
        password_hashed = make_password(password)
        return password, password_hashed

    def get(self, request):
        serializer_class = self.get_serializer(api_type=request.query_params.get("api_type"))
        kwargs = {}
        id = get_query_param(request, "id", None)
        order = get_query_param(request, 'order', 'desc')
        order_by = get_query_param(request, 'order_by', "created_at")
        search = get_query_param(request, 'search', None)

        if id:
            kwargs["guid"] = id
        if order and order_by:
            if order_by == "head":
                order_by = "head__first_name"
            if order == "desc":
                order_by = f"-{order_by}"
        if search:
            kwargs["name__icontains"] = search
        data = self.serializer_class.Meta.model.objects.filter(**kwargs)
        data, count = paginate_data(data, request)
        serialized_data = serializer_class(data, many=True)
        response_data = {
            "conut": count,
            "data": serialized_data.data
        }
        return self.send_success_response(data=response_data, message=SUCCESSFUL)

    def create(self, request, *args, **kwargs):
        try:
            password, hashed_password = self.get_password()
            request.POST._mutable = True
            addresses = request.data.pop("address")
            request.data.update({"password": hashed_password, "username": request.data.get("email")})
            request.POST._mutable = False
            serialized_data = self.serializer_class(data=request.data, context={"address": addresses})
            if serialized_data.is_valid():
                response_data = serialized_data.save()
                send_email(password, [request.data.get("email")])
                return self.send_created_response(data=self.serializer_class(response_data).data, message=SUCCESSFUL)
            return self.send_bad_request_response(message=get_first_error_message_from_serializer_errors(
                serialized_data.errors, UNSUCCESSFUL))
        except Exception as e:
            return self.send_internal_server_error_response(errors_details=str(e))

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        addresses = request.data.pop("address")
        request.POST._mutable = False
        if "id" not in request.data:
            return self.send_not_found_response(errors_details=ID_NOT_PROVIDED)
        instance = self.serializer_class.Meta.model.objects.get(guid=request.data.get("id"))
        if not instance:
            return self.send_not_found_response(errors_details=ID_NOT_PROVIDED)
        serialized_data = self.serializer_class(instance, data=request.data, partial=True,
                                                context={"address": addresses})
        if serialized_data.is_valid():
            response_data = serialized_data.save()
            return self.send_success_response(data=self.serializer_class(response_data).data, message=SUCCESSFUL)
        return self.send_bad_request_response(message=get_first_error_message_from_serializer_errors(
            serialized_data.errors, UNSUCCESSFUL))

    def destroy(self, request, *args, **kwargs):
        try:
            if "id" not in request.query_params:
                return self.send_not_found_response(errors_details=ID_NOT_PROVIDED)
            instance = self.serializer_class.Meta.model.objects.get(guid=request.query_params.get("id"))
            if not instance:
                return self.send_not_found_response(errors_details=ID_NOT_PROVIDED)
            instance.delete()
            return self.send_success_response(message=SUCCESSFUL)
        except Exception as e:
            return self.send_internal_server_error_response(errors_details=str(e))
