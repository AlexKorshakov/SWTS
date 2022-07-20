from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from apps.core.web.utils import MyMixin
from loader import logger

# from .models import News
from .models import Violations, MainCategory


# Create your views here.


async def simple_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello from "Core" app!')


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']

    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    return render(request, 'test.html', context={'page_obj': page_obj})


# class HomeNews(MyMixin, ListView):
#     """Просмотр всех новостей"""
#     model = News  # основная модель
#     template_name = 'home_news_list.html'  # страница
#     context_object_name = 'news'  # страница
#     mixin_prop = 'hello world'  # переопределение поля миксины MyMixin
#     paginate_by = 10  # количество записей на странице
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         """Дополнение данных перед отправкой на рендер"""
#         context = super(HomeNews, self).get_context_data(**kwargs)
#         context['title'] = self.get_upper('Главная страница')
#         context['mixin_prop'] = self.get_prop()
#         # logger.info(f"{context=}")
#         return context
#
#     def get_queryset(self):
#         return News.objects.filter(is_published=True).select_related('category')


class HomeViolations(MyMixin, ListView):
    """Просмотр всех новостей"""
    model = Violations  # основная модель
    template_name = 'home_violations_list.html'  # страница
    context_object_name = 'violations'  # объект
    mixin_prop = 'hello world'  # переопределение поля миксины MyMixin
    paginate_by = 16  # количество записей на странице

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super(HomeViolations, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        # return Violations.objects.filter(is_published=False).select_related('category')
        return Violations.objects.select_related('category')


class ViewViolations(DetailView):
    """Просмотр определённой новости"""
    model = Violations
    template_name = 'violations/violations_detail.html'
    context_object_name = 'violations_item'


class NewsByMainCategory(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(MainCategory.objects.get(pk=self.kwargs['category_id']))
        logger.info(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')
