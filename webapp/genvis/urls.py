from django.conf.urls import url
import genvis.views


urlpatterns = [
    url(r'^test', genvis.views.TestView.as_view(), name="test"),
]
