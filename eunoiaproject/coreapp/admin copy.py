from django.contrib import admin

# Register your models here.
from .models import Profile,Notification
from .models import Product,Feature,UserStory,Activity,Idea, FeatureSequence, Sprint,BrainStorm, IdeaNote, IdeaNoteAction,ActivitySequence


admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(UserStory)
admin.site.register(Activity)
admin.site.register(Sprint)
admin.site.register(Idea)
admin.site.register(FeatureSequence)
admin.site.register(BrainStorm)
admin.site.register(IdeaNote)
admin.site.register(IdeaNoteAction)
admin.site.register(ActivitySequence)