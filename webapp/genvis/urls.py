from django.conf.urls import url
import genvis.views


urlpatterns = [
    url(r'^test', genvis.views.TestView.as_view(), name="test"),
    url(r'^ideogram', genvis.views.IdeogramView.as_view(), name="ideogram"),
    url(r'^multigene', genvis.views.MultigeneView.as_view(), name="multigene"),
    url(r'^PCAscatterplot', genvis.views.PCAscatterplotView.as_view(), name="PCAscatterplot"),
]
