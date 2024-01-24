from django.urls import path
from . import views
from .views import SelectTestRangeView



app_name    = "dictionary"
urlpatterns = [ 
    path('', views.Menu, name="Menu"),
    path('serch/', views.index, name="index"),
    path('select_test_range/', SelectTestRangeView.as_view(), name='select_test_range'),
    path('test/<int:start>/<int:end>/', views.example_test, name="example_test"),
    path('answer/', views.answer, name="answer"),
    path('result/', views.result, name='result'),
    path('quiz_done/<int:score>/', views.quiz_done, name="quiz_done"),
]