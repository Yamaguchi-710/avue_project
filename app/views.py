from django.views.generic import View
from django.shortcuts import render
from. import function
from .forms import CalcPlusForm


class IndexView(View):
    # template_name = 'app/index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, "app/top.html")



class Project_avue(View):
    forms = {
            "forms":CalcPlusForm()
        }
    
    def get(self, request, *args, **kwargs):
        params = self.forms
        
        list_param = [170,2,30]
               
        list_route = function.make("avue", list_param)
        function.print_prj(list_route,"avue")    
        return render(request, "app/avue.html", params)
       
    def post(self, request, *args, **kwargs):
        params = self.forms
        params['forms'] = CalcPlusForm(request.POST)
        
        list_param = [int(request.POST["val1"]), int(request.POST["val2"]), int(request.POST["val3"])]
        
        list_route = function.make("avue", list_param)
        function.print_prj(list_route,"avue")    
        return render(request, "app/avue.html", params)
        


class Project_private(View):
    def get(self, request, *args, **kwargs):
        list_route = function.make("private")
        function.print_prj(list_route,"private")    
        return render(request, "app/private.html")
