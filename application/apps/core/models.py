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
