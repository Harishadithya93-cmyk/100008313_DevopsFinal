from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("health/", views.health),
    path("notes", views.notes_collection),
    path("notes/<int:note_id>", views.note_detail),
]