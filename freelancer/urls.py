from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from Account.views import (
    registration_view,
    logout_view,
    login_view,
)

from home.views import home, job_posting,list_jobs,list_all_jobs,job_detail,ai_jobs


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('job_posting/', job_posting, name="job_posting"),
    path('list_jobs/', list_jobs, name="list_jobs"),
    path('list_all_jobs/', list_all_jobs, name="list_all_jobs"),
    path('ai_jobs/', ai_jobs, name="ai_jobs"),
    path('job_detail/<int:job_id>/', job_detail, name="job_detail"),
    path('account/', include('Account.urls', namespace='account')),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', registration_view, name="register"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_changedone.html'),
    name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_resetdone.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_resetform.html'),
        name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_resetcomplete.html'),
        name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
