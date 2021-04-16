from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect

class Index(View):
    TEMPLATE = 'documentation.html'
    def get(self, request):
        return redirect('docs:index')