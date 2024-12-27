from django.urls import path

from . import views

urlpatterns = [
    # ex: /note/
    path("", views.index, name="index"),
    # ex: /note/5/
    path("<int:note_id>/", views.detail, name="detail"),
]
