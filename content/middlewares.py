from django.http import Http404
from django.urls import resolve, Resolver404
from django.shortcuts import redirect


class Custom404Middleware:
    
    def __init__(self,get_response) -> None:
        self.get_response = get_response

    def __call__(self,request):
        try:
            resolve(request.path_info)
        except Resolver404:
            return redirect('404')
        
        response = self.get_response(request)
        return response