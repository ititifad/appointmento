from .models import *
import json
from celery import task
from django.core.mail import send_mail
from .models import Appointment
# from twilio.rest import Client
from django.conf import settings
import json
import requests

def checkout(request, id, first_name, last_name, gender, location, hospital, specialist, app_date, message, phone):
    appointment = Appointment.objects.create(id=id, first_name=first_name, last_name=last_name, gender=gender, location=location, phone=phone, hospital=hospital, specialist=specialist, app_date=app_date, message=message)
    
    return appointment

@task
def appointment_created(appointment_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    appointment = Appointment.objects.get(id=appointment_id)
    subject = f'Appointment nr. {appointment.id}'
    message = f'Dear {appointment.first_name},from {appointment.location}, phone {appointment.phone} \n\n' \
        f'have successfully placed an appointment.' \
        f'with {appointment.specialist}.'
    mail_sent = send_mail(subject,
                                  message,
                                  'dex90jay@gmail.com',
                                  [appointment.phone])
    return mail_sent

def send_sms( patient_name, specialist_name, specialist_phone, patient_location, app_date, patient_phone):
            URL = 'https://apisms.beem.africa/v1/send'
            api_key ='6fa1c6173155f296'
            secret_key ='MjBjNzk1YTVmYzRiYTk4YjFiNjQ0ZTFhOTQwOTQ0Mjg4ZmE4MDYxYjIwMTY1Nzg0YmQzZjEzMGEwMWI2NmM0Yg=='
            content_type = 'application/json'
            source_addr = 'geitatech'
            apikey_and_apisecret = api_key + ':' + secret_key

            first_request = requests.post(url = URL,data = json.dumps({
            'source_addr': source_addr,
            'schedule_time': '',
            'encoding': '0',
            'message': f"Hello, {patient_name} from {patient_location}, phone {patient_phone},requests an appointment on {app_date},",
            'recipients': [
            {
            'recipient_id': 1,
            'dest_addr': specialist_phone,
            },
            ],
            }),
        
            headers = {
            'Content-Type': content_type,
            'Authorization': 'Basic ' + api_key + ':' + secret_key,
            },
            auth=(api_key,secret_key),verify=False)

            print(first_request.status_code)
            print(first_request.json())
            return (first_request.json())
            
            @app.errorhandler(500)
            def server_error(e):
                errorName='Error'
                return Response(
                    json.dumps(errorName),
                    status=500,
                    )
                return send_sms
    