from django.conf.urls import url
from actual_app import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'ajax/getnewloc$', views.elastic_search, name='elastic_search')
]