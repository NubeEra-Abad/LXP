from lxpapiapp.models import *
from .learnerserializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Case, When, Value, Max
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.conf import settings
from urllib.parse import quote_plus
import csv
from django.db import connection
from django.shortcuts import get_object_or_404
