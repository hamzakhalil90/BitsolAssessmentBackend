import ast
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import secrets
import string
from User_Management_Backend import settings
import datetime
import jwt
from cryptography.fernet import Fernet
import string
import secrets
from django.core.mail import send_mail
import threading
from User_Management_Backend.settings import EMAIL_HOST_USER


def generate_password(length=8):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def get_query_param(request, key, default):
    """
    @param request: request object
    @type request: request
    @param key: key to get data from
    @type key: str
    @param default: default variable to return if key is empty or doesn't exist
    @type default: str/None
    @return: key
    @rtype: str/None
    """
    if key in request.query_params:
        key = request.query_params.get(key)
        if key:
            return key
    return default


def get_params(name, instance, kwargs):
    """
     Helps prepare kwargs for querying database based on the set parameters
    """
    instance = check_for_one_or_many(instance)
    if type(instance) == list or type(instance) == tuple:
        kwargs[f"{name}__in"] = instance
    elif type(instance) == str and instance.lower() in ["true", "false"]:
        kwargs[f"{name}"] = bool(instance.lower() == "true")
    else:
        kwargs[f"{name}"] = instance
    return kwargs


def check_for_one_or_many(instances):
    """
    check if there is only one instance or multiple
    """
    try:
        instance = ast.literal_eval(instances)
        return instance
    except Exception as e:
        print(e)
        return instances


def convert_to_dict(self, data):
    """
    converts kwargs in to python dictionary
    """
    return {key: value for key, value in data} if data else {}


def get_filters(self, request, kwargs):
    """
    General function to get query params provided from a request,
    Helps prepare kwargs for querying database based on the set parameters
    """
    kwargs = self.convert_to_dict(kwargs)
    filter_kwargs = {}
    for arg in request.query_params:
        if arg in kwargs.keys() and request.query_params.get(arg):
            filter_kwargs = get_params(kwargs[arg], request.query_params.get(arg), filter_kwargs)
    return filter_kwargs


def send_password(first_name, last_name, email):
    password = generate_dummy_password()
    subject = "Welcome"
    message = f"""
                Hi {first_name} {last_name},
                Welcome to the site, your password is: {make_password(password)}
                        """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def generate_dummy_password(length=8):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def encrypt_token(token):
    """Encrypt the jwt token so users cannot see token content

    Args:
        token ([str]): [The jwt token]

    Returns:
        [str]: [The encrypted jwt token string]
    """
    secret_key_bytes = b"LD7i4Pe_VDdXhRyHSQrQe3RpIJ8RymjbU_zA0Yi4Hlg="
    fernet = Fernet(secret_key_bytes)
    return fernet.encrypt(token.encode()).decode("utf-8")


def generate_access_token(user):
    # nbf: Defines the time before which the JWT MUST NOT be accepted for processing
    access_token_payload = {
        'email': user.email,
        'iat': datetime.datetime.utcnow(),
        # 'role': users.role
    }
    exp_claim = {
        "exp": access_token_payload.get("iat") + datetime.timedelta(seconds=int(settings.JWT_TOKEN_EXPIRY_DELTA))}
    # Add expiry claim to token_payload
    token_payload = {**access_token_payload, **exp_claim}
    encoded_token = jwt.encode(token_payload, settings.JWT_ENCODING_SECRET_KEY, algorithm='HS256')
    jwt_token = encrypt_token(encoded_token)
    return jwt_token


def send_email(password, recipient):
    subject = "Account Created"
    message = f"""
    Use this password to access the app {password}
    """
    t = threading.Thread(target=send_mail,
                         args=(subject, message, EMAIL_HOST_USER, recipient))
    t.start()
    return True
