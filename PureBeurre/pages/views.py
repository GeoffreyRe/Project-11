import logging
from django.shortcuts import render

# Create your views here.


def home(request):
    """
    This view renders home template
    """
    return render(request, "pages/home.html")


def legal_notices(request):
    """
    This view renders legal notices template
    """

    return render(request, "pages/legal_notices.html")


def contact(request):
    """
    This view renders contact template
    """
    return render(request, 'pages/contact.html')

def trigger_error(request):
    logging.exception("Une zero division error va arriver")
    division_zero = 1/0
