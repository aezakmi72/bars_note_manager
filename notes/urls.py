from django.urls import path
from . import views


app_name = 'notes'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<uuid:pk>', views.NoteDetail.as_view(), name='note_detail'),
    path('api/notes', views.GetNoteList.as_view(), name='note_list'),
    path('api/notes/create', views.CreateNote.as_view(), name='create_note'),
    path('api/categories', views.api_categories, name='categories'),
    path('api/notes/<uuid:pk>', views.ApiNoteDetail.as_view(), name='api_note_detail'),
]