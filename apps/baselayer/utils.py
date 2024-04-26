import ast
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import secrets
import string
from User_Management_Backend import settings

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
