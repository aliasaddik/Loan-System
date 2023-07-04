from django.contrib import admin
from django.urls import path 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Loan.myapp.views.auth import CustomerRegisterApiView, LoginByTokenApiView, VerifyEmailView

 


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path("auth/", include("Loan.myapp.routes.auth")),
   path("customers/", include("Loan.myapp.routes.customers")),
   path("loans/", include("Loan.myapp.routes.loans")),
   path("installments/", include("Loan.myapp.routes.installments")),
   path("admin/", admin.site.urls),
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 