from django.shortcuts import render
from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = "test.html"
