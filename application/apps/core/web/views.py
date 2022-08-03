import asyncio
import os
from pprint import pprint

from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout

from apps.core.web.utils import MyMixin, del_violations, get_id_registered_users, get_params
from loader import logger

from .forms import UsrRegisterForm, UserLoginForm

# from .models import News
from .models import Violations, MainCategory, Location, GeneralContractor, IncidentLevel, Status

# Create your views here.
from ..bot.database.DataBase import upload_from_local


def upload(request: HttpRequest):
    #  https://ru.stackoverflow.com/questions/1313580/Запуск-функции-при-нажатии-кнопки-django

    if request.method == 'POST':
        content: list = asyncio.run(get_id_registered_users())
        params: list = asyncio.run(get_params(content))
        logger.debug(content)

        for param in params:
            asyncio.run(upload_from_local(params=param))
            logger.info(f'Данные загружены в БД')
        return redirect('home')


def update_violations(request: HttpRequest):
    if request.method == 'POST':
        logger.info(f'запись обновлена')
        return redirect('home')


def delete_violations(request):
    violation_file_id = request.POST['violation_file_id']

    if request.method == 'POST':
        logger.debug(violation_file_id)
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


class ViolationsByStatus(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Status.objects.get(pk=self.kwargs['status_id']))
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            status_id=self.kwargs['status_id'],
            is_published=True
        ).prefetch_related('status')


def register(request):
    if request.method == 'POST':
        form = UsrRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect("home")
        else:
            messages.error(request, 'Ошибка регистрации')

    else:
        form = UsrRegisterForm()

    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()

    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("login")
