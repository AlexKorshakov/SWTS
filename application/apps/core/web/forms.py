import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Violations, Location, WorkShift, MainCategory, Status, GeneralContractor, Category, IncidentLevel, \
    ActRequired, EliminationTime, ViolationCategory
from django.contrib.auth.models import User


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
        label='Площадка',
        queryset=Location.objects.all(), empty_label="***********",
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
        queryset=WorkShift.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    # created_at = forms.DateField(
    #     label='Дата регистрации',
    #     widget=forms.SelectDateWidget(attrs={'class': 'form-control'}),
    #     help_text="Введите дату",
    # )+
    # updated_at = models.DateField(auto_now=True, verbose_name='Обновлено')
    main_category = forms.ModelChoiceField(
        label='Основная Категория',
        queryset=MainCategory.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    violation_category = forms.ModelChoiceField(
        label='Категория нарушения',
        queryset=ViolationCategory.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    status = forms.ModelChoiceField(
        label='Статус',
        queryset=Status.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_published = forms.BooleanField(
        label='Опубликовано?',
        widget=forms.CheckboxInput(),
        help_text="Отметьте если требует публикации в реестре",
    )
    is_finished = forms.BooleanField(
        label='Устранено?',
        widget=forms.CheckboxInput(),
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
        queryset=GeneralContractor.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    incident_level = forms.ModelChoiceField(
        label='Уровень происшествия',
        queryset=IncidentLevel.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    act_required = forms.ModelChoiceField(
        label='Требуется оформление Акта-предписания?',
        queryset=ActRequired.objects.all(), empty_label="***********",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    elimination_time = forms.ModelChoiceField(
        label='Время на устранение',
        queryset=EliminationTime.objects.all(), empty_label="***********",
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
    day = forms.CharField(
        label='День',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="День",
        disabled=True
    )
    month = forms.CharField(
        label='Месяц',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Месяц",
        disabled=True
    )
    year = forms.CharField(
        label='Год',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="Год",
        disabled=True
    )
    violation_id = forms.CharField(
        label='violation_id',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="violation_id",
        disabled=True
    )
    report_folder_id = forms.CharField(
        label='report_folder_id',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="report_folder_id",
        disabled=True
    )
    parent_id =+ forms.CharField(
        label='parent_id',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="parent_id",
        disabled=True
    )
    json_folder_id = forms.CharField(
        label='json_folder_id',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="json_folder_id",
        disabled=True
    )
    photo_folder_id = forms.CharField(
        label='photo_folder_id',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="photo_folder_id",
        disabled=True
    )
    # coordinates = models.CharField(max_length=255, verbose_name='Координаты', blank=True, null=True)
    # latitude = models.CharField(max_length=255, verbose_name='Широта', blank=True, null=True)
    # longitude = models.CharField(max_length=255, verbose_name='Долгота', blank=True, null=True)
    json_file_path = forms.CharField(
        label='json_file_path',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="json_file_path",
        disabled=True
    )
    json_full_name = forms.CharField(
        label='json_full_name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="json_full_name",
        disabled=True
    )
    photo_file_path = forms.CharField(
        label='photo_file_path',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="photo_file_path",
        disabled=True
    )
    photo_full_name = forms.CharField(
        label='photo_full_name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="photo_full_name",
        disabled=True
    )
    user_fullname = forms.CharField(
        label='Имя пользователя как в telegram',
        widget=forms.TextInput(attrs={'class': 'form-control', 'cols': 10, 'rows': 3}),
        help_text="user_fullname",
        disabled=True
    )

    class Meta:
        model = Violations
        # fields = '__all__'
        # fields = ['location', 'name', 'work_shift', 'function'
        #           ]
        fields = [
            # 'created_at',
            'location', 'name', 'work_shift', 'function', 'user_fullname',  'main_category',
            'status', 'is_published', 'incident_level', 'act_required',
            'is_finished', 'description', 'comment', 'general_contractor', 'category', 'violation_category',
            'elimination_time', 'title', 'user_id', 'file_id', 'photo', 'json', 'day', 'month', 'year',
            'violation_id', 'report_folder_id', 'parent_id', 'photo_full_name',
            'json_folder_id', 'photo_folder_id', 'json_file_path', 'json_full_name', 'photo_file_path',
        ]
        fields_order = [
            "location", "name", 'work_shift', 'function', 'user_fullname', 'file_id'
        ]

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не может начинаться с цифры')
        return title
