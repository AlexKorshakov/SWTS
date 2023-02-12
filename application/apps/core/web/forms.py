import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import (ActRequired, Category, EliminationTime, Finished,
                     GeneralContractor, IncidentLevel, Location, MainCategory,
                     NormativeDocuments, Status, SubLocation,
                     ViolationCategory, Violations, WorkShift)

EMPTY_LABEL: str = "***********"


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя:',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(label='Пароль:',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UsrRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя:',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label='имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(label='Пароль:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ViolationsForm(forms.ModelForm):
    """
    """
    location = forms.ModelChoiceField(
        label='Закрепленный участок',
        queryset=Location.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    main_location = forms.ModelChoiceField(
        label='Площадка',
        queryset=Location.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sub_location = forms.ModelChoiceField(
        label='Под площадка / участок',
        queryset=SubLocation.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    function = forms.CharField(
        label='Должность',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите должность",
    )
    name = forms.CharField(
        label='ФИО',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите ФИО",
    )
    work_shift = forms.ModelChoiceField(
        label='Смена',
        queryset=WorkShift.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    main_category = forms.ModelChoiceField(
        label='Основная Категория',
        queryset=MainCategory.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    violation_category = forms.ModelChoiceField(
        label='Категория нарушения',
        queryset=ViolationCategory.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ModelChoiceField(
        label='Статус',
        queryset=Status.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_published = forms.BooleanField(
        label='Опубликовано?',
        widget=forms.CheckboxInput(),
        help_text="Отметьте если требует публикации в реестре",
    )
    finished = forms.ModelChoiceField(
        label='Устранено?',
        queryset=Finished.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Отметьте если все мероприятия выполнены",
    )
    description = forms.CharField(
        label='Описание нарушения',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите описание нарушения",
    )
    comment = forms.CharField(
        label='Мероприятия по устранению',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите описание мероприятий по устранению",
    )
    general_contractor = forms.ModelChoiceField(
        label='Подрядчик',
        queryset=GeneralContractor.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    normative_documents = forms.ModelChoiceField(
        label='ПодКатегория',
        queryset=NormativeDocuments.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    incident_level = forms.ModelChoiceField(
        label='Уровень происшествия',
        queryset=IncidentLevel.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    act_required = forms.ModelChoiceField(
        label='Требуется оформление Акта-предписания?',
        queryset=ActRequired.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    elimination_time = forms.ModelChoiceField(
        label='Время на устранение',
        queryset=EliminationTime.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label='Краткое описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите короткое описание",
    )
    user_id = forms.CharField(
        label='ID пользователя',
        # widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="ID пользователя",
    )

    class Meta:
        model = Violations
        fields = [
            'name', 'function', 'work_shift', 'user_id', 'location', 'main_location', 'sub_location', 'main_category',
            'status', 'is_published', 'incident_level', 'finished', 'act_required', 'description', 'comment',
            'general_contractor', 'category', 'normative_documents', 'violation_category', 'elimination_time', 'title',
        ]
        # fields_order = [
        # ]

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не может начинаться с цифры')
        return title


class ViolationsAddForm(forms.ModelForm):
    """Форма при добавлении записи
    """
    location = forms.ModelChoiceField(
        label='Закрепленный участок',
        queryset=Location.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    main_location = forms.ModelChoiceField(
        label='Площадка',
        queryset=Location.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sub_location = forms.ModelChoiceField(
        label='Под площадка / участок',
        queryset=Location.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    function = forms.CharField(
        label='Должность',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите должность",
    )
    name = forms.CharField(
        label='ФИО',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите ФИО",
    )
    work_shift = forms.ModelChoiceField(
        label='Смена',
        queryset=WorkShift.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    main_category = forms.ModelChoiceField(
        label='Основная Категория',
        queryset=MainCategory.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    violation_category = forms.ModelChoiceField(
        label='Категория нарушения',
        queryset=ViolationCategory.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ModelChoiceField(
        label='Статус',
        queryset=Status.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_published = forms.BooleanField(
        label='Опубликовано?',
        widget=forms.CheckboxInput(),
        help_text="Отметьте если требует публикации в реестре",
    )
    finished = forms.ModelChoiceField(
        label='Устранено?',
        queryset=Finished.objects.all(), empty_label=EMPTY_LABEL,
        help_text="Отметьте если все мероприятия выполнены",
    )
    description = forms.CharField(
        label='Описание нарушения',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите описание нарушения",
    )
    comment = forms.CharField(
        label='Мероприятия по устранению',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите описание мероприятий по устранению",
    )
    general_contractor = forms.ModelChoiceField(
        label='Подрядчик',
        queryset=GeneralContractor.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ormative_documents = forms.ModelChoiceField(
        label='ПодКатегория',
        queryset=NormativeDocuments.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    incident_level = forms.ModelChoiceField(
        label='Уровень происшествия',
        queryset=IncidentLevel.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    act_required = forms.ModelChoiceField(
        label='Требуется оформление Акта-предписания?',
        queryset=ActRequired.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    elimination_time = forms.ModelChoiceField(
        label='Время на устранение',
        queryset=EliminationTime.objects.all(), empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label='Краткое описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите короткое описание",
    )
    user_id = forms.CharField(
        label='ID пользователя',
        # widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="ID пользователя",
    )
    file_id = forms.CharField(
        label='ID записи',
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Введите ID записи",
    )
    photo = forms.ImageField(
        label='Путь к фотофайлу',
        widget=forms.FileInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        localize=f'{user_id}/data_file/{str(file_id).split("___")[0]}/photo/',
        help_text="Выберите файл",
    )
    json = forms.FileField(
        label='Путь к данными нарушения',
        widget=forms.FileInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        localize=f'{user_id}/data_file/{str(file_id).split("___")[0]}/json/',
        help_text="Выберите файл",
    )
    violation_id = forms.CharField(
        label='violation_id',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="violation_id",
        disabled=True
    )
    coordinates = forms.CharField(
        label='Координаты',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="violation_id",
        # disabled=True
    )
    latitude = forms.CharField(
        label='Широта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="violation_id",
        # disabled=True
    )
    longitude = forms.CharField(
        label='Долгота',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="violation_id",
        # disabled=True
    )

    class Meta:
        model = Violations

        fields = [
            'name', 'function', 'work_shift', 'user_id',
            'location', 'main_location', 'sub_location', 'main_category',
            'status', 'is_published', 'incident_level', 'finished', 'act_required',
            'description', 'comment', 'general_contractor', 'category', 'normative_documents', 'violation_category',
            'elimination_time', 'title',
        ]
        # fields_order = []

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не может начинаться с цифры')
        return title
