"""coreapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'coreapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    # Brainstorm
    path('home/brainstorm/<action>/<int:id>',views.brainstorm, name='brainstorm'),
    # Ideas
    path('home/idea/<action>/<int:id>',views.idea, name='idea'),

    # kanban
    path('home/kanban/<action>/<int:id>',views.kanban, name='kanban'),

    # Product
    path('home/product/<int:product_id>/<submenu>',login_required(views.ProductView.as_view()), name='product'),
    # path('home/product/<int:product_id>/<submenu>/<action>/<int:id>',views.product, name='product'),
  
    # path('home/product_admin',views.product_admin, name='product_admin')

    path('notify/',views.notify, name='notify'),
    path('signup/', views.signup, name='signup'),

    path('signup/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
