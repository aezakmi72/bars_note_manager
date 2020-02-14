from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls', namespace='notes')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', lambda request: redirect('notes:index', permanent=True)),
]
