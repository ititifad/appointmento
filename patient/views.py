from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .forms import AppointmentBookForm
from .tasks import send_sms, appointment_created, checkout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

class PersonListView(ListView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'patient_list.html'
    
def createAppointment(request):
    if request.method == 'POST':
        form = AppointmentBookForm(request.POST, None)
        
        if form.is_valid():
            form.save()
            email_subject = f'New Appointment: {form.cleaned_data["first_name"]}: {form.cleaned_data["location"]}'
            email_message = f'{form.cleaned_data["first_name"]}, from {form.cleaned_data["location"]}, phone {form.cleaned_data["phone"]} \n\n' \
                            f'requests an appointment.' \
                            f'with {form.cleaned_data["specialist"]} on {form.cleaned_data["app_date"]}'
            send_mail(email_subject, email_message, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL)
            # id = form.cleaned_data['id']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # gender = form.cleaned_data['gender']
            # phone = form.cleaned_data['phone']
            # location = form.cleaned_data['location']
            # hospital = form.cleaned_data['hospital']
            # specialist = form.cleaned_data['specialist']
            # message = form.cleaned_data['message']
            # app_date = form.cleaned_data['app_date']
        
            # appointment = checkout(request, id, first_name, last_name, gender, location, hospital, specialist, app_date, message, phone)
            # appointment_created(appointment)
            return render(request, 'success.html')
    
    form = AppointmentBookForm()
    return render(request, 'patient_form.html',{'form': form})
class PersonCreateView(CreateView):
    model = Appointment
    fields = ('first_name', 'last_name', 'gender', 'location', 'hospital', 'specialist','phone', 'message', 'app_date')
    success_url = reverse_lazy('patient_changelist')
    template_name = 'patient_form.html'
    
class PersonUpdateView(UpdateView):
    model = Appointment
    ffields = ('first_name', 'last_name', 'gender', 'location', 'hospital', 'specialist','phone', 'message', 'app_date')
    success_url = reverse_lazy('person_changelist')
    template_name = 'patient_form.html'

def load_specialists(request):
    hospital_id = request.GET.get('hospital')
    specialists = Specialist.objects.filter(hospital_id=hospital_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'specialists': specialists})

def success(request):
    return render(request, 'success.html')