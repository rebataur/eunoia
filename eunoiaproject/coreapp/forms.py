import datetime


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db.models import Q
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from django.forms import ModelChoiceField
from .models import Profile, Idea, Feature, Activity, BrainStorm,Opportunity
from .models import IDEA_STATUS, FEATURES_PRIORITIES,ACTIVITY_COMPLEXITY,FEATURE_COMPLEXITY,ACTIVITY_STATUS,ACTIVITY_TYPE



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required a valid email address."
    )
    # birth_date = forms.DateField(help_text="Required. Format: YYYY-MM-DD")
    # company_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            # "company_name",
            "password1",
            "password2",
        )


CATEGORIES = (
    ("IST", "Indian Standard Time"),
    ("CET", "Central European Time"),
    ("GMT", "Greenwich Meridian Time"),
    ("UTC", "Coordinated Universal Time"),
)


class ProfileForm(forms.ModelForm):
    time_zone = forms.ChoiceField(
        initial="CAR",
        label="Time Zone",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=CATEGORIES,
    )

    class Meta:
        model = Profile
        fields = ("address", "city", "country", "zip_code", "bio", "profile_pic")



   
class BrainStormForm(forms.ModelForm):
    topic = forms.CharField(label='Topic',
                                  
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Short Topic/theme to brainstorm on"}))

    class Meta:
        model = BrainStorm
        fields = ('topic',)
class IdeaForm(forms.ModelForm):
    idea_name = forms.CharField(label='Idea Name',
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Please provide a temporary product name"}))
    intended_persona = forms.CharField(label='Intended Persona',
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Individuals such as, businesses like, startups who want to"}))
    my_strength = forms.BooleanField(label='My Strength',required=False,
                       widget=forms.CheckboxInput(attrs={'input_type':'checkbox','class': 'checkbox','placeholder':"A placeholder name of the product to identify"}))
    core_concept = forms.CharField(label='Core Concept',
                       widget=forms.Textarea(attrs={'input_type':'textarea','rows':3,'class': 'form-input','placeholder':"Provide fundamental ideas, think from first principles(think from scratch)"}))
  
    status = forms.ChoiceField(label='Status',choices=IDEA_STATUS,
                       widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))

  
    class Meta:
        model = Idea
        fields = ('intended_persona','idea_name','core_concept','my_strength','status')



class FeatureForm(forms.ModelForm):
    ability_to = forms.CharField(label='Ability To',
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Ability provided by Feature"}))
    ability_for = forms.CharField(label='For Persona',
                       max_length=30,                       
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"for which user"}))

    description = forms.CharField(label='Description of feature',
                       required=True,  
                       widget=forms.Textarea(attrs={'input_type':'textarea','rows':3,'class': 'form-input','placeholder':"Provide fundamental ideas, think from first principles(think from scratch)"}))
  
    priority = forms.ChoiceField(label='Priority',choices=FEATURES_PRIORITIES,
                       widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))

    # tag = forms.CharField(label='Tag', required=False,
    #                    widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Feature Tags(comma separated) eg auth,ux,pricing,payments"}))
    outcome = forms.CharField(label='Outcome for User',required=True,                 
                       widget=forms.Textarea(attrs={'input_type':'textarea','rows':3,'class': 'form-input','placeholder':"What outcome shoule be expeceted if this feature is completed"}))
    value = forms.CharField(label='Value to User',
                     
                       widget=forms.Textarea(attrs={'input_type':'textarea','rows':3,'class': 'form-input','placeholder':"Justify How this will be valuable to user"}))
    complexity = forms.ChoiceField(label='Complexity',choices=FEATURE_COMPLEXITY,
                       widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))
 
  
    class Meta:
        model = Feature
        fields = ('ability_to','ability_for','description','outcome','value','complexity','priority',)

  
    
class ActivityForm(forms.ModelForm):
    outcome = forms.CharField(label='Outcome', 
                       max_length=120,                       
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Title of Feature"}))
    complexity = forms.ChoiceField(label='Complexity',choices=ACTIVITY_COMPLEXITY,
                       widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))
 
    type = forms.ChoiceField(label='Type',choices=ACTIVITY_TYPE,widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))

    description = forms.CharField(label='Description',                     
                       widget=forms.Textarea(attrs={'input_type':'textarea','class': 'form-input','placeholder':"Describe activity and steps", 'rows':3, 'cols':20}))
  
    note = forms.CharField(label='Note', required=False,                
                       widget=forms.Textarea(attrs={'input_type':'textarea','class': 'form-input','placeholder':"Special Notes", 'rows':3, 'cols':5}))
  

    class Meta:
        model = Activity
        fields = ('outcome','complexity','type','description','note')

class ShortActivityForm(forms.ModelForm):
    outcome = forms.CharField(label='Outcome', required=False,
                       max_length=120,                       
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Title of Feature"}))
    
    complexity = forms.ChoiceField(label='Complexity',choices=ACTIVITY_COMPLEXITY,
                       widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))
 

    class Meta:
        model = Activity
        fields = ('outcome',)



    # type = models.CharField(max_length=30, choices=ACTIVITY_TYPE, null=True)
    # complexity = models.CharField(max_length=30, choices=ACTIVITY_COMPLEXITY, null=True)
    # created_by = models.ForeignKey('landingninja.Profile',on_delete=models.DO_NOTHING,null=True,related_name='created_by_set')
    # assigned_to = models.ForeignKey('landingninja.Profile',on_delete=models.DO_NOTHING,null=True,related_name='assignedto_by_set')
    # status = models.CharField(max_length=30, choices=ACTIVITY_STATUS, null=True) 
    # depends_on = models.ForeignKey('Activity', on_delete=models.CASCADE,null=True) 

    # outcome = models.CharField(max_length=120)
    # description = models.CharField(max_length=1024, null=True)
    # note = models.CharField(max_length=1024,blank=True)

    # belongs_to_sprint = models.ForeignKey('Sprint',on_delete=models.DO_NOTHING,null=True)


# class GenderField(forms.ChoiceField):
#       def __init__(self, *args, **kwargs):
#             super(GenderField, self).__init__(*args, **kwargs)
#             self.error_messages = {"required":"Please select a gender, it's required"}
#             self.choices = ((None,'Select gender'),('M','Male'),('F','Female'))

from .widgets import BootstrapDateTimePickerInput
class MyRadioForm(forms.Form):
    radio_btn = forms.ChoiceField(label='My Radio',choices=IDEA_STATUS,
        widget=BootstrapDateTimePickerInput(attrs={'lbl':'This is a label'})
    )
    status = forms.ChoiceField(label='Status',choices=IDEA_STATUS,
                       widget=forms.RadioSelect(attrs={'input_type':'radio','class': 'form-radio'}))


class OpportunityForm(forms.ModelForm):
    email = forms.CharField(label='Email',
                       max_length=30,                       
                       widget=forms.TextInput(attrs={'input_type':'text','class': 'form-input','placeholder':"Email"}))
    
  
    class Meta:
        model = Opportunity
        fields = ( 'email',)