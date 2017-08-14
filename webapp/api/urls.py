from django.conf.urls import url
import api.views


urlpatterns = [
    url(r'^timeseries', api.views.time_series, name="api_time_series"),
]
