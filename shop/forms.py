from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Added new fields: postcode, state, payment_method
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'postcode', 'city', 'state', 'payment_method'
        ]
        
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        
        # Automatically add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
            # Add help text (Placeholders) in English (standard in Malaysia)
            if field_name == 'first_name':
                field.widget.attrs['placeholder'] = 'First Name'
            elif field_name == 'last_name':
                field.widget.attrs['placeholder'] = 'Last Name'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'example@email.com'
            elif field_name == 'phone':
                field.widget.attrs['placeholder'] = 'e.g. 0112345678'
            elif field_name == 'address':
                field.widget.attrs['placeholder'] = 'Unit/House No, Street Name'
                # Make the address field readonly if you plan to update it automatically from the map
                # field.widget.attrs['readonly'] = 'readonly'
            elif field_name == 'postcode':
                field.widget.attrs['placeholder'] = 'e.g. 50088'
                field.widget.attrs['maxlength'] = '5' # Malaysian postcode is always 5 digits
            elif field_name == 'city':
                field.widget.attrs['placeholder'] = 'e.g. Subang Jaya'
            elif field_name == 'state':
                # State field will be a Dropdown automatically if Choices are set in the Model
                field.widget.attrs['class'] = 'form-select' # Bootstrap class for select menus
            elif field_name == 'payment_method':
                field.widget.attrs['class'] = 'form-check-input' # Styling for radio buttons