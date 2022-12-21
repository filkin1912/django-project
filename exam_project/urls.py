from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('exam_project.accounts.urls')),
    path('', include('exam_project.games.urls')),
    path('dashboard/', include('exam_project.common.urls'))
]
