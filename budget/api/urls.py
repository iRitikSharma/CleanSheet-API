from django.urls import path , include
from rest_framework import routers
from .views import ImportView

router = routers.DefaultRouter()
router.register(r'budget',ImportView)

urlpatterns = [ 
    path('', include(router.urls)),    

]