"""
URL configuration for banktask project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .customer import urls as cust_url
from .casa import urls as casa_url
from .users import urls as user_url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Bank Task API",
        default_version='v1',
        description="API documentation for the Banking App",
    ),
    public=True,
    authentication_classes = [JWTAuthentication],
    permission_classes=(permissions.AllowAny,),
)
schema_view._swagger_schema = {
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter 'Bearer ' followed by your token in the text box below.",
        }
    },
    "security": [
        {"Bearer": []}
    ],
}

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include(cust_url)),
    path('api/', include(casa_url)),
    path('api/', include(user_url)),
]
