from django.contrib import admin
from django.core.paginator import Paginator

from .models import User, Violations, Status, MainCategory, Location, WorkShift, Category, EliminationTime, \
    GeneralContractor, IncidentLevel, ViolationCategory, ActRequired

# Register your models here.
# To get django model: models.<ModelName>


admin.site.site_title = 'Управление Нарушениями'
admin.site.site_header = 'Управление Нарушениями'


@admin.register(Violations)
class ViolationsAdmin(admin.ModelAdmin):
    list_display: tuple = (
        'id', 'location', 'created_at', 'main_category', 'description', 'status', 'is_finished',
        'general_contractor', 'category', 'incident_level', 'coordinates', 'file_id', 'user_id',
    )

    list_filter = (
        'created_at', 'status', 'main_category', 'incident_level', 'location', 'user_id',
    )

    list_display_links: tuple = (
        'id', 'location', 'created_at', 'main_category', 'description',
        'general_contractor', 'category', 'incident_level', 'coordinates', 'file_id', 'user_id',
    )
    # Поле поиска, это список, в списке находятся поля, на которых основан поиск
    search_fields = ['description', 'title']

    # столбец, который можно редактировать в списке
    list_editable = (
        'is_finished', 'category', 'incident_level',
    )

    list_select_related = ["location", 'general_contractor', ]

    filter_horizontal = ('location', 'general_contractor', 'category',)

    # Показывать как переключатель на странице сведений
    radio_fields = {"main_category": admin.HORIZONTAL}

    # в списке стиль номера данных, отображаемых после нечеткого поиска.
    show_full_result_count = True

    list_max_show_all = 50
    list_per_page = 20
    actions_on_top = True
    save_on_top = True
    paginator = Paginator


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(EliminationTime)
class EliminationTimeAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(GeneralContractor)
class GeneralContractorAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(IncidentLevel)
class IncidentLevelAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(ViolationCategory)
class ViolationCategorylAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(ActRequired)
class ActRequiredlAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(Status)
class StatuslAdmin(admin.ModelAdmin):
    list_display: tuple = ('id', 'title')
    list_display_links: tuple = ('id', 'title')
    search_fields: tuple = ('title',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
