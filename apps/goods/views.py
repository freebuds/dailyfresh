from django.shortcuts import render
from django.views.generic import View
# Create your views here.

# 127.0.0.1
class Index(View):
    def get(self, request):
        return render(request, 'index.html')