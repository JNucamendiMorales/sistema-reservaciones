import json
import csv
import calendar
from .models import Salon,Reservacion,Reservacion,Favorito
from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.safestring import mark_safe
from django.db.models import Q,Count,Sum,Avg,F
from django.db.models.functions import ExtractMonth,ExtractWeek,TruncDate,TruncDay,TruncMonth
from django.utils.timezone import now, make_aware, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages,admin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from .serializers import SalonSerializer, ReservacionSerializer
from rest_framework import viewsets
from datetime import datetime,timedelta
from .forms import RegistroForm,ReservacionForm,SalonForm,ReservacionAdminForm
from decimal import Decimal
from myapp.Descargas.export_charts import exportar_csv,exportar_pdf,exportar_xlsx_nativo
#from weasyprint import HTML
#from xhtml2pdf import pisa
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter


from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required







