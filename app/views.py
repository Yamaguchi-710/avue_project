from django.views.generic import View
from django.shortcuts import render
from. import function


class IndexView(View):
    # template_name = 'app/index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, "app/top.html")

class Project_avue(View):    
    def get(self, request, *args, **kwargs):
        list_route = function.make("avue")
        function.print_prj(list_route,"avue")    
        return render(request, "app/avue.html")
        
class Project_private(View):    
    def get(self, request, *args, **kwargs):
        list_route = function.make("private")
        function.print_prj(list_route,"private")    
        return render(request, "app/private.html")
