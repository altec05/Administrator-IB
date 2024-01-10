"""
URL configuration for Certs_UFK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.conf import settings
from .views import *
from django.contrib.auth import views

from django.urls import re_path
from django.views.static import serve

admin.site.site_header = 'ИС "Администратор ИБ"'
admin.site.index_title = 'Панель администрирования'
admin.site.site_title = 'Администратор ИБ'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/certs/cerificate/', red_certs, name='certs'),
    path('admin/', red_to_admin, name='to_admin'),
    path('_nested_admin/', include('nested_admin.urls')),
    path('', include('workers.urls')),
    path('', include('certs.urls')),
    path('', include('licenses.urls')),
    path('', include('applications.urls')),
    path('', include('changes.urls')),
    # path('', admin_index, name='admin_index'),
    path('lists/workers/', pick_worker, name='pick_worker'),
    # path('lists/workers/by_worker/', lists_by_worker, name='by_worker'),
    path(r'lists/workers/by_worker/<worker_id>/', lists_by_worker, name='by_worker'),
    # path('', index),
    path('', index, name='home'),
    path('logout/', logout_user, name='logout'),
    path("password_reset/", password_reset, name="password_reset"),
    # # path('', include('django.contrib.auth.urls')),
    # path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path('login/', login_user, name='login'),
    path('password_change/done/', index, name='password_change_done'),
    path('accounts/profile', profile_view, name='profile'),
    # # path('acts-of-install', show_acts)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#
# if settings.DEBUG:
#   urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_ROOT, document_root= settings.MEDIA_ROOT)
#
# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]