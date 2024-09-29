from django.urls import path
from myapp.views import my_async_view, safe_view, non_cache_view, async_view_using_sync_function

urlpatterns = [
    path('', my_async_view, name='my_async_view'),
    path('safe/', safe_view, name='safe_view'),
    path('non-cache/', non_cache_view, name='non_cache_view'),
    path('async-sync/', async_view_using_sync_function, name='async_sync_view'),
]
