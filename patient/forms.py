from django import forms
from .models import Appointment, Specialist, Hospital

class DateInput(forms.DateInput):
    input_type = 'date'

class AppointmentBookForm(forms.ModelForm):
    app_date = forms.DateField(widget=DateInput)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {'app_date' : DateInput()}
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialist'].queryset = Specialist.objects.none()
        
        if 'hospital' in self.data:
            try:
                hospital_id = int(self.data.get('hospital'))
                self.fields['specialist'].queryset = Specialist.objects.filter(hospital_id=hospital_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['specialist'].queryset = self.instance.hospital.specialist_set.order_by('name')