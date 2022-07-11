from orm_converter.tortoise_to_django import ConvertedModel
from tortoise import Tortoise, fields
from tortoise.models import Model
from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование категории')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано ?')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Новость"  # единственное число
        verbose_name_plural = "Новости"  # множественное число
        ordering = ['-created_at', '-title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('view_news', kwargs={'pk': self.pk})


class Violations(models.Model):
    """Основная модель Описывающая все поля для Нарушения"""
    location = models.CharField(max_length=255, verbose_name='Площадка')
    work_shift = models.CharField(max_length=255, verbose_name='Смена', default='')
    function = models.CharField(max_length=255, verbose_name='Должность', default='')
    name = models.CharField(max_length=255, verbose_name='ФИО', default='')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateField(auto_now=True, verbose_name='Обновлено')
    main_category = models.CharField(max_length=255, verbose_name='Основная категория', default='')
    general_contractor = models.CharField(max_length=255, verbose_name='Подрядчик', default='')
    category = models.CharField(max_length=255, verbose_name='Категория', default='')
    act_required = models.BooleanField(default=False, verbose_name='Требуется Акт?')
    description = models.TextField(blank=True, verbose_name='Описание', default='')
    comment = models.CharField(max_length=255, verbose_name='Устранение', default='')
    elimination_time = models.CharField(max_length=255, verbose_name='Время на устранение', default='Немедленно')
    incident_level = models.CharField(max_length=255, verbose_name='Уровень происшествия', default='')
    violation_category = models.CharField(max_length=255, verbose_name='Категория нарушения', default='')

    coordinates = models.CharField(max_length=255, verbose_name='Координаты', default='', blank=True)
    latitude = models.CharField(max_length=255, verbose_name='Широта', default='', blank=True)
    longitude = models.CharField(max_length=255, verbose_name='Долгота', default='', blank=True)
    json_file_path = models.CharField(max_length=255, verbose_name='json_file_path', default='', blank=True)
    json_full_name = models.CharField(max_length=255, verbose_name='json_full_name', default='', blank=True)
    photo_file_path = models.CharField(max_length=255, verbose_name='photo_file_path', default='', blank=True)
    photo_full_name = models.CharField(max_length=255, verbose_name='photo_full_name', default='', blank=True)

    violation_id = models.CharField(max_length=255, verbose_name='violation_id', blank=False, unique=True)

    report_folder_id = models.CharField(max_length=255, verbose_name='report_folder_id', default='', blank=True)
    parent_id = models.CharField(max_length=255, verbose_name='parent_id', default='', blank=True)
    file_id = models.CharField(max_length=255, verbose_name='file_id', default='', blank=True)
    json_folder_id = models.CharField(max_length=255, verbose_name='json_folder_id', default='', blank=True)
    photo_folder_id = models.CharField(max_length=255, verbose_name='photo_folder_id', default='', blank=True)

    title = models.CharField(max_length=100, verbose_name='Заголовок')

    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?')

    day = models.PositiveSmallIntegerField(verbose_name='день')
    month = models.PositiveSmallIntegerField(verbose_name='месяц')
    year = models.PositiveSmallIntegerField(verbose_name='год')
    now = models.DateField(verbose_name='дата', blank=False)

    user_fullname = models.CharField(max_length=255, verbose_name='Имя пользователя', default='', blank=True)
    user_id = models.CharField(max_length=255, verbose_name='ID пользователя', default='', blank=True)


    class Meta:
        verbose_name = "Нарушение"  # единственное число
        verbose_name_plural = "Нарушения"  # множественное число
        ordering = ['-created_at', '-title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('view_news', kwargs={'pk': self.pk})


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    class Meta:
        verbose_name = "Категория"  # единственное число
        verbose_name_plural = "Категории"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('category', kwargs={'category_id': self.pk})


class User(Model, ConvertedModel):
    tg_id = fields.BigIntField(unique=True, description="Telegram User ID")
    chat_id = fields.BigIntField(unique=False, description="Telegram Chat ID")
    first_name = fields.CharField(max_length=64, description="Telegram Firstname")

    def __str__(self) -> str:
        return f"{self.first_name} - {self.tg_id}"

    class Meta:
        table = "user"


def register_models() -> None:
    Tortoise.init_models(
        models_paths=["apps.core.models"],
        app_label="core",
        _init_relations=False,
    )
