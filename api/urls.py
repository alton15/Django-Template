from django.urls import path

from api.sample import example

urlpatterns = [
    path('json_api', example.JsonAPI.as_view()),
    path('upload_form_data', example.FormDataAPI.as_view()),
]
