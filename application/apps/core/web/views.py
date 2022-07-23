import asyncio
import os
from pprint import pprint

from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from apps.core.web.utils import MyMixin, del_violations, get_id_registered_users, get_params
from loader import logger

from django.shortcuts import render, get_object_or_404, redirect

# from .models import News
from .models import Violations, MainCategory, Location, GeneralContractor, IncidentLevel

# Create your views here.
from ..bot.database.DataBase import run


def upload(request: HttpRequest):
    #  https://ru.stackoverflow.com/questions/1313580/Запуск-функции-при-нажатии-кнопки-django

    if request.method == 'POST':
        content = asyncio.run(get_id_registered_users())
        params = asyncio.run(get_params(content))
        logger.info(content)

        # user_chat_id = '373084462'
        # params: dict = {
        #     'all_files': True,
        #     'file_path': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{user_chat_id}/data_file/",
        #     'user_file': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{user_chat_id}/{user_chat_id}.json"
        # }

        for param in params:
            asyncio.run(run(params=param))
            logger.info(f'Данные загружены в БД')
        return redirect('home')


def upload_violations(request: HttpRequest):
    if request.method == 'POST':
        logger.info(f'запись обновлена')
        return redirect('home')


def delete_violations(request):
    violation_file_id = request.POST['violation_file_id']

    if request.method == 'POST':
        logger.info(violation_file_id)
        result = asyncio.run(del_violations(violation_file_id))
        if result:
            logger.info(f'запись {violation_file_id} удалена')
        return redirect('home')


async def simple_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello from "Core" app!')


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']

    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    return render(request, 'test.html', context={'page_obj': page_obj})


class HomeViolations(MyMixin, ListView):
    """Просмотр всех новостей"""
    model = Violations  # основная модель
    template_name = 'home_violations_list.html'  # страница
    context_object_name = 'violations'  # объект
    mixin_prop = 'hello world'  # переопределение поля миксины MyMixin
    paginate_by = 20  # количество записей на странице

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super(HomeViolations, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return Violations.objects.select_related('category')


class ViewViolations(DetailView):
    """Просмотр определённой новости"""
    model = Violations
    template_name = 'violations_detail.html'
    context_object_name = 'violations_item'


class ViolationsByMainCategory(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(MainCategory.objects.get(pk=self.kwargs['main_category_id']))
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            main_category_id=self.kwargs['main_category_id'],
            is_published=True
        ).prefetch_related('main_category')


class ViolationsByLocation(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Location.objects.get(pk=self.kwargs['location_id']))
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            location_id=self.kwargs['location_id'],
            is_published=True
        ).prefetch_related('location')


class ViolationsByGeneralContractor(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(GeneralContractor.objects.get(pk=self.kwargs['general_contractor_id']))
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            general_contractor_id=self.kwargs['general_contractor_id'],
            is_published=True
        ).prefetch_related('general_contractor')


class ViolationsByIncidentLevel(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(IncidentLevel.objects.get(pk=self.kwargs['incident_level_id']))
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            incident_level_id=self.kwargs['incident_level_id'],
            is_published=True
        ).prefetch_related('incident_level')
