from django.test import TestCase
from django.shortcuts import HttpResponse, render, redirect
import json
from app01 import models

# Create your tests here.

def test(request):
    return HttpResponse('ashia')
