from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('contas/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('produtos/', include('produtos.urls')),
    path('estoque/', include('estoque.urls')),
    path('pdv/', include('vendas.urls')),
]
