from django.conf.urls import url
import api.views


urlpatterns = [
    url(r'^gen/find', api.views.gen_find, name="api_gen_find"),
    url(r'^timeseries', api.views.time_series, name="api_time_series"),
]
