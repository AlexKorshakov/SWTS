from tortoise import Tortoise, fields
from django.db import models
from django.urls import reverse


class Violations(models.Model):
    """Основная модель Описывающая все поля для Нарушения"""

    location = models.ForeignKey(to='Location', on_delete=models.PROTECT, verbose_name='Закрепленный участок',
                                 default='')
    main_location = models.ForeignKey(to='MainLocation', on_delete=models.PROTECT, verbose_name='Площадка', default='')
    sub_location = models.ForeignKey(to='SubLocation', on_delete=models.PROTECT, verbose_name='Под площадка / участок',
                                     default='')
    function = models.CharField(max_length=255, verbose_name='Должность', default='')
    name = models.CharField(max_length=255, verbose_name='ФИО', default='')
    work_shift = models.ForeignKey(to='WorkShift', on_delete=models.PROTECT, verbose_name='Смена', default='')

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateField(auto_now=True, verbose_name='Обновлено')

    main_category = models.ForeignKey(to='MainCategory', on_delete=models.PROTECT, verbose_name='Основная категория',
                                      default='')

    status = models.ForeignKey(to='Status', on_delete=models.PROTECT, verbose_name='Статус', default=1)

    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?')
    is_finished = models.BooleanField(default=False, verbose_name='Устранено?')

    description = models.TextField(blank=True, verbose_name='Описание', default='')
    comment = models.CharField(max_length=255, verbose_name='Устранение', default='')

    general_contractor = models.ForeignKey(to='GeneralContractor', on_delete=models.PROTECT, verbose_name='Подрядчик',
                                           default='')

    category = models.ForeignKey(to='Category', on_delete=models.PROTECT, verbose_name='Категория', default='')
    normative_documents = models.ForeignKey(to='NormativeDocuments', on_delete=models.PROTECT,
                                            verbose_name='Нормативная документация', default='')

    violation_category = models.ForeignKey(to='ViolationCategory', on_delete=models.PROTECT,
                                           verbose_name='Категория нарушения', default='')

    incident_level = models.ForeignKey(to='IncidentLevel', on_delete=models.PROTECT,
                                       verbose_name='Уровень происшествия', default='')

    act_required = models.ForeignKey(to='ActRequired', on_delete=models.PROTECT, verbose_name='Требуется Акт?',
                                     default='')

    elimination_time = models.ForeignKey(to='EliminationTime', on_delete=models.PROTECT,
                                         verbose_name='Время на устранение', default='')

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    user_id = models.CharField(max_length=255, verbose_name='ID пользователя', default='', blank=True)
    file_id = models.CharField(max_length=255, verbose_name='file_id', default='', blank=True)

    photo = models.ImageField(upload_to=f'{user_id}/data_file/{str(file_id).split("___")[0]}/photo/',
                              verbose_name='Фото', blank=True)
    json = models.FileField(upload_to=f'{user_id}/data_file/{str(file_id).split("___")[0]}/json/',
                            verbose_name='Json', blank=True)

    day = models.PositiveSmallIntegerField(blank=True, verbose_name='День', default=1)
    month = models.PositiveSmallIntegerField(blank=True, verbose_name='Месяц', default=1)
    year = models.PositiveSmallIntegerField(blank=True, verbose_name='Год', default=2000)

    violation_id = models.CharField(max_length=255, verbose_name='violation_id', default='', blank=True)
    report_folder_id = models.CharField(max_length=255, verbose_name='report_folder_id', default='', blank=True)
    parent_id = models.CharField(max_length=255, verbose_name='parent_id', default='', blank=True)
    json_folder_id = models.CharField(max_length=255, verbose_name='json_folder_id', default='', blank=True)
    photo_folder_id = models.CharField(max_length=255, verbose_name='photo_folder_id', default='', blank=True)

    coordinates = models.CharField(max_length=255, verbose_name='Координаты', blank=True, null=True)
    latitude = models.CharField(max_length=255, verbose_name='Широта', blank=True, null=True)
    longitude = models.CharField(max_length=255, verbose_name='Долгота', blank=True, null=True)

    json_file_path = models.CharField(max_length=255, verbose_name='json_file_path', default='', blank=True)
    json_full_name = models.CharField(max_length=255, verbose_name='json_full_name', default='', blank=True)
    photo_file_path = models.CharField(max_length=255, verbose_name='photo_file_path', default='', blank=True)
    photo_full_name = models.CharField(max_length=255, verbose_name='photo_full_name', default='', blank=True)
    user_fullname = models.CharField(max_length=255, verbose_name='Имя пользователя', default='', blank=True)

    class Meta:
        verbose_name = "Нарушение"  # единственное число
        verbose_name_plural = "Нарушения"  # множественное число
        ordering = ['-created_at', '-title']  # порядок сортировки

    def __str__(self):
        return f'pk: {self.pk} file_id: {self.file_id} {self.title}'

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('view_violations', kwargs={'pk': self.pk})


class MainCategory(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Основная Категория')

    class Meta:
        verbose_name = "Основная Категория"  # единственное число
        verbose_name_plural = "Основные Категории"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('main_category', kwargs={'main_category_id': self.pk})


class Location(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Закрепленный участок')

    class Meta:
        verbose_name = "Закрепленный участок"  # единственное число
        verbose_name_plural = "Закрепленные участки"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('location', kwargs={'location_id': self.pk})


class SubLocation(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Под площадка / участок')

    class Meta:
        verbose_name = "Под площадка / участок"  # единственное число
        verbose_name_plural = "Под площадки / участки"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('sub_location', kwargs={'location_id': self.pk})


class MainLocation(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Площадка')

    class Meta:
        verbose_name = "Площадка"  # единственное число
        verbose_name_plural = "Площадки"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('main_location', kwargs={'main_location_id': self.pk})


class WorkShift(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Смена')

    class Meta:
        verbose_name = "Смена"  # единственное число
        verbose_name_plural = "Смены"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('work_shift', kwargs={'work_shift_id': self.pk})


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Наименование категории')

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


class NormativeDocuments(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Наименование подкатегории')
    normative = models.CharField(max_length=255, db_index=True, verbose_name='Наименование подкатегории')
    procedure = models.CharField(max_length=255, db_index=True, verbose_name='Наименование подкатегории')

    class Meta:
        verbose_name = "Нормативная документация"  # единственное число
        verbose_name_plural = "Нормативная документация"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('normative_documents', kwargs={'normative_documents_id': self.pk})


class EliminationTime(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Время на устранение')

    class Meta:
        verbose_name = "Время на устранение"  # единственное число
        verbose_name_plural = "Время на устранение"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('elimination_time', kwargs={'elimination_time_id': self.pk})


class GeneralContractor(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Подрядчик')

    class Meta:
        verbose_name = "Подрядчик"  # единственное число
        verbose_name_plural = "Подрядчики"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('general_contractor', kwargs={'general_contractor_id': self.pk})


class IncidentLevel(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Уровень происшествия')

    class Meta:
        verbose_name = "Уровень происшествия"  # единственное число
        verbose_name_plural = "Уровни происшествия"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('incident_level', kwargs={'incident_level_id': self.pk})


class ViolationCategory(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Категория нарушения')

    class Meta:
        verbose_name = "Категория нарушения"  # единственное число
        verbose_name_plural = "Категории нарушения"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('violation_category', kwargs={'violation_category_id': self.pk})


class ActRequired(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Требуется акт?')

    class Meta:
        verbose_name = "Требуется акт?"  # единственное число
        verbose_name_plural = "Требуются акты?"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('act_required', kwargs={'act_required_id': self.pk})


class Status(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Статус')

    class Meta:
        verbose_name = "Статус"  # единственное число
        verbose_name_plural = "Статусы"  # множественное число
        ordering = ['title']  # порядок сортировки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод, согласно конвекции, для создания ссылок на части экземпляра модели (класса)
        также, при наличии, позволяет переходить из админки на соответствующий раздел"""
        return reverse('status', kwargs={'status_id': self.pk})


class User(models.Model):
    tg_id = fields.BigIntField(unique=True, description="Telegram User ID")
    chat_id = fields.BigIntField(unique=False, description="Telegram Chat ID")
    first_name = fields.CharField(max_length=64, description="Telegram Firstname")

    def __str__(self) -> str:
        return f"{self.first_name} - {self.tg_id}"

    class Meta:
        verbose_name = "Пользователь"  # единственное число
        verbose_name_plural = "Пользователи"  # множественное число
        ordering = ['title']  # порядок сортировки


def register_models() -> None:
    Tortoise.init_models(
        models_paths=["apps.core.web.models"],
        app_label="core",
        _init_relations=False,
    )
