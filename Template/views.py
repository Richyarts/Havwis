from django.shortcuts import render, redirect
from django.views import View

#home view
class HomeView(View):
  def __init__(self):
    self.template_name = "v_1_0/activity/home/home.html"
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)