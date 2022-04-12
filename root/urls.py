from django.urls import path, include
from django.conf import settings #add this
from django.conf.urls.static import static #add this
from . import views



urlpatterns = [
    path('',views.displayHome,name='startPage'),
    path('index/',views.displayIndex,name='index'),
    path('ind/',views.displayNew,name='in'),
    path('signup/',views.displaySignup,name='signup'),
    # path('adminLogin/',views.displayAdminLogin,name='admin login'),
    # path('userLogin/',views.displayUserLogin,name='user login'),
    path('workerLogin/',views.displayWorkerLogin,name='worker login'),
    path('validateAL/',views.validateAL,name='AL validation'),
    path('validateUL/',views.validateUL,name='UL validation'),
    path('validateWL/',views.validateWL,name='WL validation'),
    path('validateWL/debit/',views.debitCredits,name='debit'),
    path('validateWL/detect/',views.detectAndDebit,name='detect'),
    path('upload/',views.test,name="test"),
    path('enrollNew/',views.registerNew,name="enrollNew"),
] 
