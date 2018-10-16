from django.conf.urls import url
from rest_framework.authtoken import views as drf_views
from shop.api.views import Logout, ObtainExpiringAuthToken, InScheduledJob, AllJob, User, Excel

urlpatterns = [
    # url(r'^auth$', drf_views.obtain_auth_token, name='auth'),
    url(r'^auth$', ObtainExpiringAuthToken.as_view()),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^user$', User.as_view(), name='get_user_detail'),
    url(r'^inscheduledjob', InScheduledJob.as_view(), name='inscheduledjob'),
    url(r'^alljob', AllJob.as_view(), name='alljob'),
    #url(r'^downloadexcel', Excel.as_view(), name='downloadExcel'),
]
