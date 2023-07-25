from django import forms

class ScorchyForm(forms.Form):
    hold_feature_value = forms.IntegerField(initial=0, required=False)
    scorchy_hold_node_1 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_fruit_1 = forms.CharField(initial="", required=False)
    scorchy_hold_node_2 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_fruit_2 = forms.CharField(initial="", required=False)
    scorchy_hold_node_3 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_fruit_3 = forms.CharField(initial="", required=False)
    scorchy_hold_node_4 = forms.BooleanField(initial=False, required=False)
    scorchy_hold_fruit_4 = forms.CharField(initial="", required=False)