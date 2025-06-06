from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
               path("UserLogin.html", views.UserLogin, name="UserLogin"),	      
               path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
               path("Register.html", views.Register, name="Register"),
               path("RegisterAction", views.RegisterAction, name="RegisterAction"),
               path("LoadModel", views.LoadModel, name="LoadModel"),
	       path("Suggestion", views.Suggestion, name="Suggestion"),
	       path("SuggestionAction", views.SuggestionAction, name="SuggestionAction"),	
	       
]
