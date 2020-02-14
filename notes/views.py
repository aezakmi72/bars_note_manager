from django.http import Http404, JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import NoteSerializer, CategorySerializer
from .models import Note, Category


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'notes/index.html'

class NoteDetail(View):
    def get(self, request, pk):
        object = get_object_or_404(Note, pk=pk)
        if object.published or (request.user.is_authenticated and request.user == object.creator):
            return render(request, 'notes/detail.html', {'note': object})
        else:
            raise PermissionDenied()

class ApiNoteDetail(APIView):
    def get(self, request, pk):
        object = get_object_or_404(Note, pk=pk)        
        if not object.published and object.creator != request.user:
            raise PermissionDenied()
        serializer = NoteSerializer(object)
        return JsonResponse(serializer.data, safe=False)
    

    def delete(self, request, pk):
        object = get_object_or_404(Note, pk=pk)
        if not object.published and object.creator != request.user:
            raise PermissionDenied()
        object.delete()
        return HttpResponse(status=204)    
    def put(self, request, pk):        
        object = get_object_or_404(Note, pk=pk)
        if not object.published and object.creator != request.user:
            raise PermissionDenied()
        serializer = NoteSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse(serializer.errors, status=400)


class GetNoteList(ListAPIView):    
    serializer_class = NoteSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise PermissionDenied()         
        query_list = Note.objects.filter(creator=self.request.user)
        dtcreate = self.request.query_params.get('dtcreate', None)
        title = self.request.query_params.get('title', None)        
        category = self.request.query_params.get('category', None)
        bookmark = self.request.query_params.get('bookmark', None)                
        sort_by = self.request.query_params.get('sort_by', None)
        # filters
        if dtcreate:            
            query_list = query_list.filter(dtcreate__date=dtcreate)
        if title:
            query_list = query_list.filter(title__startswith=title)
        if category and category != '0':
            query_list = query_list.filter(category=category)        
        if bookmark and bookmark != '0':
            bookmark = bookmark == 'True'
            query_list = query_list.filter(bookmark=bookmark)
        # sort
        if sort_by == 'category':
            query_list = query_list.order_by('category')
        elif sort_by == 'bookmark':
            query_list = query_list.order_by('bookmark')
        return query_list


def api_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        raise Http404

class CreateNote(APIView):    
    def post(self, request):
        data = request.data        
        data['creator'] = request.user.id
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
