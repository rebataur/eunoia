from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from django.contrib.postgres.fields import JSONField
from django.db import models

import json
from random import randint
from datetime import datetime

# Create your models here.

USER_TYPE = (
    ("FOUNDER", "Founder"),
    ("CEO", "CEO"),
    ("PO", "Product Owner"),
    ('SCRUM_MASTER','Scrum Master'),
    ('DEVELOPER','Developer')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        default="/media/profile_pics/placeholder_profile_pic.png",
    )
    tenant_id = models.CharField(max_length=30, blank=True)

    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zip_code = models.IntegerField(blank=True, default=0, null=True)
    
    company_name = models.CharField(max_length=30)

    role = models.CharField(max_length=30, choices=USER_TYPE)
    employee_id = models.CharField(max_length=30)
   

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, tenant_id="TENANT-{}".format(instance.id))
    instance.profile.save()

IDEA_STATUS = (
    ('INCUBATING','Incubating'),
    ('PRODUCTIZE','Productize'),
    ('ATTIC','Attic'),
)

class BrainStorm(models.Model):
    created_by = models.ForeignKey('Profile',on_delete=models.DO_NOTHING)
    topic = models.CharField(max_length=1024)    
    created_on = models.DateField(auto_now=True)


class IdeaNote(models.Model):
    belongs_to_brainstorm = models.ForeignKey('BrainStorm',on_delete=models.CASCADE)
    created_by = models.ForeignKey('Profile',on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=1024)  
    description = models.CharField(max_length=1024)      
    created_on = models.DateField(default=datetime.now)    
    arhive = models.BooleanField(  default=False,blank=True,null=True)
    updated_on = models.DateField(default=datetime.now)

    def all_counts(self):
        # fav_count = IdeaNoteAction.objects.filter(belongs_to_ideanote=self.id,action='fav_ideanote').count()
        strength_count = IdeaNoteAction.objects.filter(belongs_to_ideanote=self.id,action='strength_ideanote').count()
        like_count = IdeaNoteAction.objects.filter(belongs_to_ideanote=self.id,action='like_ideanote').count()
        marketneed_count = IdeaNoteAction.objects.filter(belongs_to_ideanote=self.id,action='marketneed_ideanote').count()
        return {'strength_count':strength_count,'like_count':like_count,'marketneed_count':marketneed_count}
    def is_fav(self):
        return IdeaNoteAction.objects.filter(belongs_to_ideanote=self.id,action='fav_ideanote').exists()

    def rnum(self):
        return randint(-2,2)

class IdeaNoteAction(models.Model):
    belongs_to_ideanote = models.ForeignKey('IdeaNote',on_delete=models.CASCADE)
    created_by = models.ForeignKey('Profile',on_delete=models.DO_NOTHING)
    action = models.CharField(max_length=30)
        
    def is_fav(self,profile_instance_id):
        return self.action == 'fav_ideanote'
    def is_strength(self,profile_instance_id):
        return self.action == 'strength_ideanote'
    def is_like(self,profile_instance_id):
        return self.action == 'like_ideanote'
    def is_marketneed(self,profile_instance_id):
        return self.action == 'marketneed_ideanote'

IDEA_STATUS = (
    ('INCUBATING','Incubating'),
    ('PRODUCTIZE','Productize'),
    ('ATTIC','Attic'),
)   
class Idea(models.Model):
    created_by = models.ForeignKey('Profile',on_delete=models.DO_NOTHING)
    brainstorming = models.ForeignKey('BrainStorm',on_delete=models.DO_NOTHING,null=True)
    idea_name = models.CharField(max_length=30)
    intended_persona = models.CharField(max_length=1024)
    core_concept = models.CharField(max_length=1024*10)
    my_strength = models.BooleanField(  default=False,blank=True,null=True)
    status = models.CharField(max_length=30,choices=IDEA_STATUS,default='INCUBATING')
    # updated_on = models.DateField(default=datetime.now)
    created_on = models.DateField(default=datetime.now)

    def is_productized(self):
        return True if self.status == 'PRODUCTIZE' else False

class Product(models.Model):
    owner = models.ForeignKey('Profile',on_delete=models.DO_NOTHING,null=True)
    idea = models.ForeignKey('Idea',on_delete=models.DO_NOTHING,null=True)
    name = models.CharField(max_length=1024)
    overview = models.CharField(max_length=1024)
    epic = models.CharField(max_length=1024)


FEATURES_PRIORITIES = (
    ('MUST_HAVE' , 'Must Have'),
    ('SHOULD_HAVE' , 'Should Have'),
    ('COULD_HAVE' , 'Could Have'),
    ('WOULD_HAVE', 'Would Have')  

)
# BIG IDEA OUTCOME DRIVEN
FEATURE_COMPLEXITY = (
    ('HIGH','High'),
    ('MEDIUM','Medium'),
    ('LOW','Low'),
    ('VERY_LOW','Very Low'),    
    ('UNKNOWN','Unknown'),

)
FEATURE_STATUS = (
    ('TODO', 'Todo'),
    ('IN_PROGRESS','In Progress'),
    ('DONE','Done'),
    ('POSTPONED','Postponed'),
    ('WAITING_ON','WAITING_ON')
)
class Feature(models.Model):
    product = models.ForeignKey('Product',on_delete=models.DO_NOTHING)
    ability_for = models.CharField(max_length=30)
    ability_to = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024*10)
    priority = models.CharField(max_length=30,choices=FEATURES_PRIORITIES)
    tag = models.CharField(max_length=1024,blank=True,null=True)
    outcome = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)
    complexity = models.CharField(max_length=30, choices=FEATURE_COMPLEXITY, null=True)
    status = models.CharField(max_length=30, choices=FEATURE_STATUS, default='TODO') 
    created_by = models.ForeignKey('Profile',on_delete=models.DO_NOTHING,null=True,related_name='feature_created_by_set')
    def rnum(self):
        return randint(-1,1)
class FeatureSequence(models.Model):
    feature_id =  models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=20)



class UserStory(models.Model):
    feature = models.ForeignKey('Feature',on_delete=models.CASCADE)
    template = models.CharField(max_length=1024,default='In order to <receive benefit> as a <role>, I can <goal/desire>')

ACTIVITY_TYPE = (
    ('BUSINESS','Business'),
    ('TECHNICAL','Technical'),
    ('INFRASTRUCTURE','Infrastructure')
)
ACTIVITY_COMPLEXITY = (
    ('HIGH','High'),
    ('MEDIUM','Medium'),
    ('LOW','Low'),
    ('VERY_LOW','Very Low'),    
    ('UNKNOWN','Unknown'),

)
ACTIVITY_STATUS = (
    ('TODO', 'Todo'),
    ('IN_PROGRESS','In Progress'),
    ('DONE','Done'),
    ('POSTPONED','Postponed'),
    ('WAITING_ON','Waiting On')
)
class Activity(models.Model):
    user_story = models.ForeignKey('UserStory',  on_delete=models.DO_NOTHING, null=True)
    related_to_feature = models.ForeignKey('Feature', on_delete=models.DO_NOTHING, null=True)
    related_to_idea = models.ForeignKey('Idea', on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=30, choices=ACTIVITY_TYPE, null=True)
    complexity = models.CharField(max_length=30, choices=ACTIVITY_COMPLEXITY, null=True)
    created_by = models.ForeignKey('Profile',on_delete=models.DO_NOTHING,null=True,related_name='created_by_set')
    assigned_to = models.ForeignKey('Profile',on_delete=models.DO_NOTHING,null=True,related_name='assignedto_by_set')
    status = models.CharField(max_length=30, choices=ACTIVITY_STATUS, null=True,default='TODO') 
    depends_on = models.ForeignKey('Activity', on_delete=models.CASCADE,null=True) 

    outcome = models.CharField(max_length=120)
    description = models.CharField(max_length=1024, null=True)
    note = models.CharField(max_length=1024,null=True)

    belongs_to_sprint = models.ForeignKey('Sprint',on_delete=models.DO_NOTHING,null=True)

    created_on = models.DateField(default=datetime.now)

    def rnum(self):
        return randint(-2,2)


class ActivitySequence(models.Model):
    activity_id =  models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=20)

class Sprint(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    




class Notification(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)



class Opportunity(models.Model):
    email = models.CharField(max_length=30)
    date_received = models.DateField(default=datetime.now)

    def __str__(self):
        return self.email + ' - ' + str(self.date_received)