from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator


# Create your views here.


async def simple_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello from "Core" app!')


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']

    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    return render(request, 'test.html', context={'page_obj': page_obj})
