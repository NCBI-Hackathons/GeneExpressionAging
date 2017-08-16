from django.shortcuts import render
from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = "test.html"

class IdeogramView(TemplateView):
    template_name = "ideogram.html"

class MultigeneView(TemplateView):
    template_name = "multigene.html"
