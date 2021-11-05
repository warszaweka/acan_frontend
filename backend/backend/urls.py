from django.contrib.admin import site
from django.urls import include, path
from graphene_django.views import GraphQLView
from django.conf import settings

urlpatterns = [
    path('admin/', site.urls),
    path('graphql', GraphQLView.as_view(graphiql=True if settings.DEBUG else False)),
    path('acan/', include('acan.urls')),
]
