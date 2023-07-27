from django import forms

class ScorchyForm(forms.Form):
    scorchy_hold_0 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_1 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_2 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_3 = forms.BooleanField(initial=False, required=False)