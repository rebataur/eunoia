import datetime
from random import randint 
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string


from django.contrib.auth.models import User

from .tokens import account_activation_token
from .models import Profile
from .forms import SignUpForm


from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q

from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth
from django.db.models import Avg, Count, Min, Sum

# from .models import
from .tokens import account_activation_token
from .models import Profile, Idea, Product, Feature, FeatureSequence, Activity, BrainStorm, IdeaNote,IdeaNoteAction,ActivitySequence
from .forms import IdeaForm, MyRadioForm, FeatureForm, ActivityForm, BrainStormForm, ShortActivityForm,OpportunityForm


def index(request):
    num =   randint(0,15)
    context = {'chaos_num':num}

    return render(request, "eunoiaapp/index.html", context)

@login_required
def home(request):
    # print(request.headers)
    global_context = get_global_menu_context(request.user)
    print(global_context)
    context = {
        'global_context' : global_context
    }
    return render(request, "eunoiaapp/home.html", context)


@login_required
def kanban(request,action,id):
    global_context = get_global_menu_context(request.user)    
    context = {
        "action" : action,
        "idea_id" : id,
        'global_context' : global_context
    }
    if action == 'all' and request.method == 'GET':
        context['ideas'] = Idea.objects.filter(created_by=global_context['profile_instance'])

    elif action == 'idea_kanban' and request.method == 'GET':
        context['idea'] = Idea.objects.get(pk=id)
        context['todos'] = Activity.objects.filter(related_to_idea=id,status='TODO',created_by=global_context['profile_instance'])
        context['inprogress'] = Activity.objects.filter(related_to_idea=id,status='IN_PROGRESS',created_by=global_context['profile_instance'])
        context['done'] = Activity.objects.filter(related_to_idea=id,status='DONE',created_by=global_context['profile_instance'])

        context['todo_seq'] = ActivitySequence.objects.filter(type='TODO').order_by('order')
        context['inprogress_seq'] = ActivitySequence.objects.filter(type='IN_PROGRESS').order_by('order')
        context['done_seq'] = ActivitySequence.objects.filter(type='DONE').order_by('order')

    elif action == 'idea_add_todo' and request.method == 'GET':
        context['todo_form'] = ShortActivityForm()

    elif action == 'idea_add_todo' and request.method == 'POST':
        form = ShortActivityForm(request.POST)
        if form.is_valid():
            activity_instance = form.save(commit=False)
            activity_instance.created_by = global_context['profile_instance']
            activity_instance.status = 'TODO'
            activity_instance.complexity = 'UNKNOWN'
            activity_instance.related_to_idea = Idea.objects.get(pk=id)
            activity_instance.save()
            print(activity_instance.id)
            ActivitySequence.objects.create(activity_id = activity_instance.id,order=activity_instance.id, type='TODO')
        return redirect('/home/kanban/idea_kanban/{}'.format(id))

  
    elif action == 'edit_activity' and request.method == 'GET':
        context['todo_form'] = ShortActivityForm()
        activity = Activity.objects.get(pk=id)
        id = activity.related_to_idea.id
        context['idea_id'] = id

    elif action == 'edit_activity' and request.method == 'POST':
        pass

    elif action == 'reorder_activity' and request.method == 'POST':
        orders = json.loads(request.POST['order'])
        print(orders)
        for activity_type in orders:
            for activity_arr in activity_type:
                print(activity_arr)

                ActivitySequence.objects.filter(activity_id = activity_arr[0]).update(order=activity_arr[1],type=activity_arr[2])
                activity = Activity.objects.get(pk = activity_arr[0])
                activity.status=activity_arr[2]
                activity.save()
  
    return render(request, "eunoiaapp/kanban.html", context)

@login_required
def idea(request,action,id):
    global_context = get_global_menu_context(request.user)    
    context = {
        "username": request.user,
        "action" : action,
        "idea_id" : id,
        "radio_form" : MyRadioForm(),
        "global_context" : global_context
    }
    if action == 'all':
        context['ideas'] = Idea.objects.filter(created_by=global_context['profile_instance'])
    elif action == 'new_idea' and request.method == 'POST':
        form = IdeaForm(request.POST)
        print('FOrm ', form.errors)
        if form.is_valid():
            idea_instance = form.save(commit=False)
            idea_instance.created_by = global_context['profile_instance']
            idea_instance.save()
            return redirect('/home/idea/all/0')
    elif action == 'new_ideafrombrainstorming' and request.method == 'POST':
        form = IdeaForm(request.POST)
        print('FOrm ', form.errors)
        if form.is_valid():
            idea_instance = form.save(commit=False)
            idea_instance.created_by = global_context['profile_instance']
            idea_instance.brainstorming = BrainStorm.objects.get(pk=id)
            idea_instance.save()
            return redirect('/home/idea/all/0')
    elif action == 'new_idea' and request.method == 'GET' and id <= 0:
        # In case of new
        context['form'] = IdeaForm()     
    # In case of edit
    elif action == 'existing_idea' and request.method == 'GET' and id > 0:
        idea = Idea.objects.get(pk=id)
        context['idea_instance'] = idea
        context['form'] = IdeaForm(instance=idea)
        context['ideanotes'] = IdeaNote.objects.filter(belongs_to_brainstorm=idea.brainstorming,created_by=global_context['profile_instance'])
    elif action == 'new_ideafrombrainstorming' and request.method == 'GET' and id >0:
        context['form'] = IdeaForm()    
        context['ideanotes'] = IdeaNote.objects.filter(belongs_to_brainstorm=id,created_by=global_context['profile_instance'])
    elif action == 'existing_idea' and request.method == 'POST' and id > 0:
        idea_instance = Idea.objects.get(pk=id)      
        form = IdeaForm(request.POST, instance=idea_instance)
        if form.is_valid():            
            form.save()
            # if productize, create a product out of it
            idea = Idea.objects.get(pk=id)
            if idea.is_productized():
                product = Product(idea = idea, name = idea.idea_name, owner = global_context['profile_instance'] )   
                product.save()       
            return redirect('/home/idea/all/0')
    


  
    return render(request, "eunoiaapp/idea.html", context)


@login_required
def brainstorm(request,action,id):
    global_context = get_global_menu_context(request.user)    
    context = {
        "action" : action,
        "idea_id" : id,
        "global_context" : global_context
    }
    if action == 'all':
        context['brainstorms'] = BrainStorm.objects.filter(created_by=global_context['profile_instance'])
    elif action == 'new_brainstorm' and request.method == 'POST':
        form = BrainStormForm(request.POST)
        print('FOrm ', form.errors)
        if form.is_valid():
            brainstorm_instance = form.save(commit=False)
            brainstorm_instance.created_by = global_context['profile_instance']
            brainstorm_instance.save()
            return redirect('/home/brainstorm/all/0')
    elif action == 'new_brainstorm' and request.method == 'GET' and id <= 0:
        # In case of new
        context['form'] = BrainStormForm()     
    # In case of edit
    elif action == 'ideanote' and request.method == 'GET' and id > 0:
        context['brainstorm'] = BrainStorm.objects.get(pk=id)
        context['ideanotes'] = IdeaNote.objects.filter(belongs_to_brainstorm=id,created_by=global_context['profile_instance']).exclude(title__exact='',description__exact='').select_related()
    elif action == 'new_ideanote' and request.method == 'GET' and id > 0:
        brainstorm = BrainStorm.objects.get(pk=id)
        context['brainstorm'] = brainstorm  
        blank_ideanote = IdeaNote.objects.filter(belongs_to_brainstorm=id,created_by=global_context['profile_instance'],title__exact='',description__exact='')
        ideanote = None
        if blank_ideanote.count() == 0:
            ideanote = IdeaNote.objects.create(belongs_to_brainstorm=brainstorm,created_by=global_context['profile_instance'],title='',description='')
        else:
            ideanote = blank_ideanote[0]
        print('********',ideanote)
        context['new_ideanote'] = ideanote
        context['ideanotes'] = IdeaNote.objects.filter(belongs_to_brainstorm=id,created_by=global_context['profile_instance']).exclude(title__exact='',description__exact='')
    elif action == 'update_ideanote' and request.method == 'POST':
       
        title = request.POST['title'] if 'title' in request.POST else ''
        description = request.POST['cnt'] if 'cnt' in request.POST else ''
     
        ideanote = IdeaNote.objects.get(pk=id)
        if len(title.strip()) == 0 and len(description.strip()) == 0:
            print('Nothing to update')
            return HttpResponse()
        elif title and len(title.strip())>0:
            ideanote.title = title.strip()
            ideanote.save()
        elif description and len(description.strip())>0:
            ideanote.description = description.strip()
            ideanote.save()
        return HttpResponse()
    elif action == 'delete_ideanote' and request.method == 'POST':
        IdeaNote.objects.get(pk=id).delete()
        return HttpResponse()
    elif action == 'fav_ideanote' or action == 'like_ideanote' or action == 'strength_ideanote' or action == 'marketneed_ideanote' and request.method == 'POST':
        ideanote = IdeaNote.objects.get(pk=id)
        idea_note_action = IdeaNoteAction.objects.filter(belongs_to_ideanote=ideanote,created_by=global_context['profile_instance'],action=action)
        undone = False
        if idea_note_action.exists():
            undone = True
            idea_note_action.delete()
        else:
            idea_note_action = IdeaNoteAction.objects.create(belongs_to_ideanote=ideanote,created_by=global_context['profile_instance'],action=action)
        action_counts = ideanote.all_counts()
        print(ideanote.all_counts(),'7777777777777')
        if action == 'fav_ideanote' and undone:
            return HttpResponse('💛') 
        elif action =='fav_ideanote':
            return HttpResponse('❤️') 
        elif action =='like_ideanote':
            return HttpResponse('👍<span class="badge" data-badge="{}"></span>'.format(action_counts['like_count']))
        elif action =='strength_ideanote':
            return HttpResponse('💪<span class="badge" data-badge="{}"></span>'.format(action_counts['strength_count']))
        elif action =='marketneed_ideanote':
            return HttpResponse('🎯<span class="badge" data-badge="{}"></span>'.format(action_counts['marketneed_count']))
    
    return render(request, "eunoiaapp/brainstorm.html", context)


#     # Get global menu context
def get_global_menu_context(user):
    menu_context = {}
    profile_instance = Profile.objects.get(user__username=user)
    menu_context['profile_instance'] = profile_instance
    menu_context["username"]: user
    menu_context["profile_pic_url"]: profile_instance.profile_pic.url 
    menu_context['notifications_count'] = 8
    menu_context['products'] = Product.objects.filter(owner=profile_instance).values('id','name')
    
    print(menu_context)

    return menu_context

# ======================== END OF BIZ FUNCTIONALITY======================

def notify(request):
    if request.method == 'POST':
        print( request.POST)
       
        form = OpportunityForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            if is_invalid_email(request.POST.get('email')):
                return HttpResponse("<h4>Thanks for subscribing. We promise we won't spam, only important updates</h4>")
            form.save()
            return HttpResponse('<h4>Thanks !, we will notify you as soon as we release.</h4>')
        else:
            return HttpResponse('<h4>Oh ! Something went wrong please try again')
            
def is_invalid_email(email):
    invalid_words = ['rebataur','no-reply','noreply']
    for invalid_word in invalid_words:
        if invalid_word in email:
            return True
    return False
    
def account_activation_sent(request):
    return render(request, "registration/account_activation_sent.html")


def error_404(request, exception):
    data = {}
    return render(request, "registration/account_activation_sent.html", data)


def error_500(request):
    data = {}
    return render(request, "registration/account_activation_sent.html", data)


class ProductView(View):
    template_name = 'eunoiaapp/producttest.html'     
    def get(self, request, *args, **kwargs):  
        global_context = get_global_menu_context(request.user)   
        print(args)  
        print(kwargs)
        print()
        product_id = kwargs['product_id']
        submenu = kwargs['submenu']
        action = request.GET['action'] if 'action' in request.GET else None
        product = Product.objects.get(pk=product_id)
        print('ACTION', action)
        context = {
            "submenu" : submenu,
            'product_menu_checked' : 'checked',  
            "product_name_checked" : product.name,
            "product" : product,   
            'global_context'  : global_context,
            'product_id':product_id,
            'action' : action
        }  
            
        if submenu =='overview'  and request.method == 'GET':
            pass

        elif submenu == 'feature':           
            if action == None:
                context['features'] = Feature.objects.filter(product=product_id,created_by=global_context['profile_instance'])
                context['features_sequence'] = FeatureSequence.objects.filter().order_by('order')
            elif action == 'new_feature':
                context['features'] = Feature.objects.filter(product=product_id,created_by=global_context['profile_instance'])
                context['features_sequence'] = FeatureSequence.objects.filter().order_by('order')
                print('*******************',action)
                context['form'] = FeatureForm() 
                context['feature_id'] = 0
            elif action == 'existing_feature':
                feature_id = request.GET['feature_id'] 
                context['feature_id'] = feature_id
                feature = Feature.objects.get(pk=feature_id)
                activities = Activity.objects.filter(related_to_feature=feature,created_by=global_context['profile_instance'])

                context['activities'] =  Activity.objects.filter(related_to_feature=feature,created_by=global_context['profile_instance'])

                context['activities_seq'] = ActivitySequence.objects.filter().order_by('order')
                print('-------------------------------')
                print(context['activities'], context['activities_seq'] )
                context['form'] = FeatureForm(instance=feature) 
            
            elif action == 'new_activity':
                print('----------------------------------^^^^^^^^^^^^^^^')
                feature_id = request.GET['feature_id'] 
                feature = Feature.objects.get(pk=feature_id)
                context['feature_id'] = feature_id
                context['feature'] = feature
                context['form'] = ActivityForm()    
            elif action == 'existing_activity':
                activity_id = int(request.GET['activity_id']) 
                activity = Activity.objects.get(pk=activity_id)
                feature = activity.related_to_feature
                context['activity_id'] = activity_id
                context['feature'] = feature
                context['form'] = ActivityForm(instance=activity)    

        elif submenu == 'featurekanban':
            print('----------------featurekanban------------------^^^^^^^^^^^^^^^')
            context['features'] = Feature.objects.filter(product=product_id,created_by=global_context['profile_instance']).order_by
            context['features_sequence'] = FeatureSequence.objects.filter().order_by('order')
            
            context['todos'] = Feature.objects.filter(product=product_id,status='TODO',created_by=global_context['profile_instance'])
            context['inprogress'] = Feature.objects.filter(product=product_id,status='IN_PROGRESS',created_by=global_context['profile_instance'])
            context['done'] = Feature.objects.filter(product=product_id,status='DONE',created_by=global_context['profile_instance'])
            context['todo_seq'] = FeatureSequence.objects.filter(type='TODO').order_by('order')
            context['inprogress_seq'] = FeatureSequence.objects.filter(type='IN_PROGRESS').order_by('order')
            context['done_seq'] = FeatureSequence.objects.filter(type='DONE').order_by('order')
            print(context['inprogress'])
            print(context['inprogress_seq'])

        elif submenu == 'activitykanban':
            print('------------------activitykanban----------------^^^^^^^^^^^^^^^')
            feature_id = request.GET['feature_id'] 
            feature = Feature.objects.get(pk=feature_id)
            context['feature_id'] = feature_id
            context['activities'] = Activity.objects.filter(related_to_feature=feature,created_by=global_context['profile_instance']).order_by
            context['activities_sequence'] = ActivitySequence.objects.all().order_by('order')
            
            context['todos'] = Activity.objects.filter(related_to_feature=feature,status='TODO',created_by=global_context['profile_instance'])
            context['inprogress'] = Activity.objects.filter(related_to_feature=feature,status='IN_PROGRESS',created_by=global_context['profile_instance'])
            context['done'] = Activity.objects.filter(related_to_feature=feature,status='DONE',created_by=global_context['profile_instance'])
            context['todo_seq'] = ActivitySequence.objects.filter(type='TODO').order_by('order')
            context['inprogress_seq'] = ActivitySequence.objects.filter(type='IN_PROGRESS').order_by('order')
            context['done_seq'] = ActivitySequence.objects.filter(type='DONE').order_by('order')
          
            print(  context['activities'],  context['activities_sequence'])
          
            if action == 'feature_update_todo':
                print('---feature_update_todo----')
                activity_id = request.GET['activity_id'] if 'activity_id' in request.GET else None
                activity = Activity.objects.get(pk=activity_id) if activity_id is not None else Activity()
                feature = Feature.objects.get(pk=feature_id)
                context['feature'] = feature
                context['form'] = ActivityForm(instance=activity)
            

        return render(request, "eunoiaapp/product/{}.html".format(submenu), context)

    def post(self, request, *args, **kwargs):
        global_context = get_global_menu_context(request.user)     
        print(kwargs)
        product_id = kwargs['product_id']
        submenu = kwargs['submenu']
        print('***************', request.GET)
        action = request.GET['action'] if 'action' in request.GET else None
        print('POST ........')
        print(request.method,product_id,submenu,action,id)
        product = Product.objects.get(pk=product_id)
        context = {
            "action" : action,
            "submenu" : submenu,
            "idea_id" : id,
            "radio_form" : MyRadioForm(),
            'product_menu_checked' : 'checked',  
            "product_name_checked" : product.name,
            "product" : product,   
            'global_context'  : global_context,
            'product_id':product_id
        }  
        if action == 'new_feature':
            form = FeatureForm(request.POST)
            if form.is_valid():
                feature_instance = form.save(commit=False)
                feature_instance.product = Product.objects.get(pk=product_id)
                feature_instance.created_by = global_context['profile_instance']
                feature_instance.save()
                FeatureSequence(feature_id=feature_instance.id, order=feature_instance.id,type='TODO').save()                
                return redirect('/home/product/{}/feature'.format(product_id))
        elif action == 'existing_feature':
            feature_id = request.GET['feature_id']
            feature = Feature.objects.get(pk=feature_id)
            form = FeatureForm(request.POST,instance=feature)
            if form.is_valid():
                form.save()
                return redirect('/home/product/{}/feature'.format(product_id))
        elif action == 'reorder_feature':
            orders = json.loads(request.POST['order'])
            for order in orders:
                FeatureSequence.objects.filter(feature_id=order[0]).update(order=order[1])
        elif action == 'new_activity':
            print("*************** NEW ACTIVITY ******************")
            feature_id = int(request.GET.get('feature_id'))
            feature = Feature.objects.get(pk=feature_id)
            form = ActivityForm(request.POST)
            print(form.is_valid(),form.errors)
            if form.is_valid():
                activity_instance = form.save(commit=False)
                activity_instance.related_to_feature = feature
                activity_instance.created_by = global_context['profile_instance']
                activity_instance.save()
                ActivitySequence.objects.create(activity_id = activity_instance.id,order=activity_instance.id, type='TODO')
                return redirect('/home/product/{}/feature?action=existing_feature&feature_id={}'.format(product_id,feature_id))
            else:
                context['feature_id'] = feature_id
                context['form'] = form
                context['feature'] = feature
        elif action == 'existing_activity':
            print("*************** NEW ACTIVITY ******************")
            activity_id = int(request.GET.get('activity_id'))
            activity = Activity.objects.get(pk=activity_id)
            form = ActivityForm(request.POST,instance=activity)
            print(form.is_valid(),form.errors)
            if form.is_valid():
                form.save()
                return redirect('/home/product/{}/feature?action=existing_feature&feature_id={}'.format(product_id,activity_id))
            else:
                context['feature_id'] = feature_id
                context['form'] = form
                context['feature'] = feature
        elif action == 'change_feature_status':
            orders = json.loads(request.POST['order'])
            print(orders)
            for feature_type in orders:
                for feature_arr in feature_type:
                    print(feature_arr)

                    FeatureSequence.objects.filter(feature_id = feature_arr[0]).update(order=feature_arr[1],type=feature_arr[2])
                    feature = Feature.objects.get(pk = feature_arr[0])
                    feature.status=feature_arr[2]
                    feature.save()
        elif action == 'feature_add_todo':
            form = ActivityForm(request.POST)
            feature_id = request.GET['feature_id']
            
            if form.is_valid():              
                activity_instance = form.save(commit=False)
                activity_instance.created_by = global_context['profile_instance']
                activity_instance.status = 'TODO'
                # activity_instance.complexity = 'UNKNOWN'
                activity_instance.related_to_feature = Feature.objects.get(pk=feature_id)
                activity_instance.save()
                print(activity_instance.id)
                ActivitySequence.objects.create(activity_id = activity_instance.id,order=activity_instance.id, type='TODO')
            return redirect('/home/product/{}/kanban'.format(product_id))

        elif action == 'feature_update_todo':
            form = ActivityForm(request.POST)
            feature_id = request.GET['feature_id']
            if 'activity_id' in request.GET:
                activity_id = request.GET['activity_id']
                instance = get_object_or_404(Activity, id=activity_id)
                form = ActivityForm(request.POST or None, instance=instance)
                if form.is_valid():
                    form.save()
            return redirect('/home/product/{}/activitykanban?feature_id={}'.format(product_id,feature_id))

        return render(request, "eunoiaapp/product/{}.html".format(submenu), context)






















# ======================== END OF BIZ FUNCTIONALITY======================



######################################################
######################################################
######################################################

#                  Authentication

######################################################
######################################################
######################################################
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = "Activate Your MySite Account"
                message = render_to_string(
                    "registration/account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        "token": account_activation_token.make_token(user),
                    },
                )
                print("=============")
                print(user.pk)
                # print(urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'))
                print(message)
                print(user.email)

                # user.email_user(subject, message)

                # ----------------
                email = EmailMessage(subject, message, to=[user.email])
                email.send()
                return redirect("account_activation_sent/")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)
        print(token)
        print(account_activation_token.check_token(user, token))
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            print(user)
            login(request, user)
            return redirect("/")
        else:
            print("invalid")
            return render(request, "registration/account_activation_invalid.html")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


def account_activation_sent(request):
    return render(request, "registration/account_activation_sent.html")


def error_404(request, exception):
    data = {}
    return render(request, "registration/account_activation_sent.html", data)


def error_500(request):
    data = {}
    return render(request, "registration/account_activation_sent.html", data)
