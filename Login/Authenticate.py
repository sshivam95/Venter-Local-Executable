# from django.shortcuts import HttpResponseRedirect, redirect, render
# from django.conf import settings
# from django.urls import reverse
#
#
# class AuthRequiredMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#
#         response = self.get_response(request)
#         #
#         # print(request.META['HTTP_HOST'])
#         if not request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('registration:login'))
#         # Code to be executed for each request/response after
#         # the view is called.
#
#         return response