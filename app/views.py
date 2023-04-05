from django.views.generic import View
from django.shortcuts import render
from. import function


class IndexView(View):
    # template_name = 'app/index.html'
    
    def get(self, request, *args, **kwargs):
        list_route = function.make()
        function.print_prj(list_route)    
        return render(request, "app/index.html")


# class IndexView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "app/index.html")
