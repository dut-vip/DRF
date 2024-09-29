from django.shortcuts import render, get_object_or_404, redirect
import datetime
from .models import MyModel
from django.http import HttpResponse
from django.views.decorators.http import (
    require_http_methods, require_GET, require_POST, require_safe,
)
from django.views.decorators.gzip import gzip_page
from django.views.decorators.cache import (
    cache_control, never_cache,
)
from asgiref.sync import sync_to_async
import asyncio
from django.shortcuts import render
from .models import Section, Story
def story_list_view(request):
    section = Section.objects.first()
    story_list = Story.objects.all()
    return render(request, 'story_list.html', {'section': section, 'story_list': story_list})
def index(request):
    return render(request, 'index.html')
# Hàm trả về thời gian hiện tại
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

# Hàm trả về phản hồi với mã trạng thái 201
def my_view(request):
    return HttpResponse(status=201)

# Hàm hiển thị chi tiết câu chuyện
def story_detail_view(request, story_id):
    obj = get_object_or_404(MyModel, pk=story_id)
    return render(request, "myapp/story_detail.html", {"story": obj})

# Hàm chuyển hướng
def redirect_view(request):
    return redirect('current_datetime')

# Hàm xử lý lỗi 404
def my_custom_page_not_found_view(request, exception):
    return HttpResponse("Page not found", status=404)

# Hàm xử lý lỗi 500
def my_custom_error_view(request):
    return HttpResponse("Server error", status=500)

# Hàm xử lý yêu cầu GET hoặc POST
@require_http_methods(["GET", "POST"])
@gzip_page
@cache_control(no_cache=True)
async def my_async_view(request):
    await asyncio.sleep(1)  # Giả lập tác vụ mất thời gian
    return HttpResponse("Hello from async view!")

# Hàm chỉ xử lý yêu cầu GET
@require_GET
async def safe_view(request):
    return HttpResponse("This is a safe async view.")

# Hàm không được cache
@never_cache
async def non_cache_view(request):
    return HttpResponse("This page is never cached.")

# Hàm đồng bộ sử dụng sync_to_async
def sync_function():
    return "This is a sync function."

async def async_view_using_sync_function(request):
    result = await sync_to_async(sync_function)()
    return HttpResponse(result)
