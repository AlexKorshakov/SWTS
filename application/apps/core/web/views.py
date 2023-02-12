import asyncio

#
# # Create your views here.
from apps.core.database.DataBase import upload_from_local
from apps.core.web.utils import (MyMixin, delete_violations_from_all_repo,
                                 get_id_registered_users, get_params,
                                 update_violations_from_all_repo)
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView
from loader import logger

#
from .forms import (UserLoginForm, UsrRegisterForm, ViolationsAddForm,
                    ViolationsForm)
from .models import (ActsPrescriptions, GeneralContractor, IncidentLevel,
                     MainCategory, MainLocation, NormativeDocuments, Status,
                     Violations)


def upload_too_db_from_local_storage(request: HttpRequest):
    """Загрузка записей из local storage в database

    :return: redirect('home')
    """
    #  https://ru.stackoverflow.com/questions/1313580/Запуск-функции-при-нажатии-кнопки-django

    if request.method == 'POST':
        id_registered: list = asyncio.run(get_id_registered_users())
        logger.debug(id_registered)
        params: list = asyncio.run(get_params(id_registered_users=id_registered))

        for param in params:
            asyncio.run(upload_from_local(params=param))
            logger.info(f'Данные загружены в БД')
        return redirect('home')


def add_violations(request: HttpRequest):
    """Добавление данных в базу данных, в локальный репозиторий, в Google Drive"""
    form = None

    print(f'{request = }')

    violation = Violations()
    # print(f"violation")

    if request.method == 'GET':
        form = ViolationsAddForm(instance=violation)

    context = {
        'form': form,
    }

    return render(request, 'add_violations.html', context=context)


def statistic(request: HttpRequest):
    """Добавление данных в базу данных, в локальный репозиторий, в Google Drive"""

    return render(
        request, 'statistic.html',
    )


def update_violations(request: HttpRequest):
    """Обновление данных в базе данных, в локальном репозитории, в Google Drive

    :param request:
    :return: redirect('greetings') if False or redirect('home') if True

    {'act_required': '2',
    'category': '22',
    'comment': 'Комментарий',
    'coordinates': '',
    'created_at_day': '1',
    'created_at_month': '1',
    'created_at_year': '2022',
    'csrfmiddlewaretoken': 'u0BB1mbVeAaaDZWOtp09iwrZffCrTrJWEXO4UpUcOjeSvBf4FSk6EtDCxMHTPwAc',
    'description': 'Описание',
    'elimination_time': '3',
    'function': 'Должность',
    'general_contractor': '66',
    'incident_level': '1',
    'is_finished': 'on',
    'is_published': 'on',
    'json': '',
    'latitude': '',
    'main_location': '18',
    'longitude': '',
    'main_category': '4',
    'name': 'Имя пользователя',
    'photo': '',
    'status': '2',
    'title': 'какой то текст',
    'user_id': 'user_id',
    'violation': '<tr',
    'violation_category': '3',
    'work_shift': '1'}
    """

    file_id = request.POST['file_id']
    logger.debug(f"file_id = {request.POST['file_id']}")

    if file_id:
        logger.debug(f"file_id: {file_id = }")
        result = asyncio.run(update_violations_from_all_repo(data_from_form=request.POST))
        if result:
            logger.info(f'Данные записи {file_id} обновлены')
            return redirect('home')

    return redirect('greetings')


class PostEdit(CreateView):
    """Просмотр категории"""
    model = Violations
    form_class = ViolationsForm
    template_name = 'update_violations.html'
    context_object_name = 'violations'
    slug = None

    def get_context_data(self, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        print(f"get_context_data")
        print(f"{kwargs = }")

        context = super(PostEdit, self).get_context_data(**kwargs)
        print(f"{context = }")
        if 'slug' in self.kwargs:
            print(f"slug {self.kwargs.get('slug', None)}")

        return context

    def get_queryset(self):
        print(f"get_queryset")
        return Violations.objects.get(pk=self.violations_id)

    def get_object(self, queryset=None):
        print(f"get_object")
        self.slug = self.kwargs.get('slug', None)
        return queryset.get(slug=self.slug)


def post_edit(request: HttpRequest, violations_id):
    form = None

    if violations_id:
        violation = Violations.objects.get(pk=violations_id)
        # print(f"violation with pk {violation}")
    else:
        violation = Violations()
        # print(f"violation")

    if request.method == 'POST':
        # print("request.method == 'POST'")

        form = ViolationsForm(instance=violation)

        if form.is_bound:
            print(f"form is_bound ")

        if form.is_valid():
            print(f"form is_valid ")

    context = {
        'form': form,
    }

    return render(request, 'update_violations.html', context=context)


def delete_violations(request: HttpRequest):
    """Удаление записи по violation_file_id из базы данных, локального репозитория, Google Drive

    """
    violation_file_id = request.POST['violation_file_id']

    if request.method == 'POST':
        logger.debug(violation_file_id)
        result = asyncio.run(delete_violations_from_all_repo(violation_file_id))
        if result:
            logger.info(f'запись {violation_file_id} удалена')
        return redirect('home')


def register(request: HttpRequest):
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

    return render(request, 'register.html', {'form': form})


def user_login(request: HttpRequest):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request: HttpRequest):
    logout(request)
    return redirect("login")


async def simple_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello from "Core" app!')


def test(request: HttpRequest):
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


class ViolationsByMainLocation(MyMixin, ListView):
    """Просмотр категории"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(MainLocation.objects.get(pk=self.kwargs['main_location_id']))
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            main_location_id=self.kwargs['main_location_id'],
            is_published=True
        ).prefetch_related('main_location')


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


class ViolationsByWeek(MyMixin, ListView):
    """Просмотр по номеру недели"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)
        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            week_id=self.kwargs['week_id'],
            is_published=True
        )
# .prefetch_related('week')

# class ViolationsByIsPublished(MyMixin, ListView):
#     """Просмотр по номеру недели"""
#     model = Violations
#     template_name = 'home_violations_list.html'
#     context_object_name = 'violations'
#     paginate_by = 20
#     allow_empty = False
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         """Дополнение данных перед отправкой на рендер"""
#         context = super().get_context_data(**kwargs)
#
#         logger.debug(f"{context=}")
#         return context
#
#     def get_queryset(self):
#         return Violations.objects.filter(
#             week=self.kwargs['is_published'],
#             is_published=True
#         )


class ViolationsByFinished(MyMixin, ListView):
    """Просмотр по номеру недели"""
    model = Violations
    template_name = 'home_violations_list.html'
    context_object_name = 'violations'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)

        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            finished_id=self.kwargs['finished_id'],
            is_published=True
        ).prefetch_related('finished')


class HomeRegisterActsPrescriptions(MyMixin, ListView):
    """Просмотр реестра актов предписаний"""
    model = ActsPrescriptions
    template_name = 'register_acts_prescriptions.html'
    context_object_name = 'acts'
    paginate_by = 50
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super(HomeRegisterActsPrescriptions, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Реестр Актов')
        context['mixin_prop'] = self.get_prop()
        return context

    # def get_queryset(self):
    #     return ActsPrescriptions.objects.select_related('acts')


class HomeRegisterNormativeDocuments(MyMixin, ListView):
    """Просмотр реестра актов предписаний"""
    model = NormativeDocuments
    template_name = 'register_normative_documents.html'
    context_object_name = 'normative_docs'
    # paginate_by = 50
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super(HomeRegisterNormativeDocuments, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Реестр Нормативной документации')
        # context['mixin_prop'] = self.get_prop()
        return context

    # def get_queryset(self):
    #     return ActsPrescriptions.objects.select_related('acts')


class HomeRegisterUnclosedPoints(MyMixin, ListView):
    """Просмотр не закрытых пунктов актов предписаний"""
    model = Violations
    template_name = 'register_of_unclosed_points.html'
    context_object_name = 'unclosed_points'
    paginate_by = 20
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнение данных перед отправкой на рендер"""
        context = super().get_context_data(**kwargs)

        logger.debug(f"{context=}")
        return context

    def get_queryset(self):
        return Violations.objects.filter(
            status=2,
            is_published=True,
        ).prefetch_related('finished')
