from django import template
from django.db.models import Count, F
from django.core.cache import cache
from apps.core.web.models import MainCategory, MainLocation, GeneralContractor, IncidentLevel, Status, Week

register = template.Library()


@register.simple_tag(name='get_list_main_categories')
def get_main_categories():
    main_categories = MainCategory.objects.all()
    return main_categories


@register.inclusion_tag('list_main_categories.html')
def show_main_categories(arg1='hello', arg2='world'):
    main_categories = cache.get("main_categories")
    if not main_categories:
        main_categories = MainCategory.objects.annotate(
            cnt=Count('violations', filter=F('violations__is_published'))
        ).filter(cnt__gt=0)
        cache.set("main_categories", main_categories, 15)

    return {'main_categories': main_categories, 'arg1': arg1, 'arg2': arg2}


@register.inclusion_tag('list_main_locations.html')
def show_main_locations():
    main_locations = cache.get("main_locations")
    if not main_locations:
        main_locations = MainLocation.objects.annotate(
            cnt=Count('violations', filter=F('violations__is_published'))
        ).filter(cnt__gt=0)
        cache.set("main_locations", main_locations, 15)

    return {'main_locations': main_locations}


@register.inclusion_tag('list_general_contractors.html')
def show_general_contractor():
    general_contractors = cache.get("general_contractors")
    if not general_contractors:
        general_contractors = GeneralContractor.objects.annotate(
            cnt=Count('violations', filter=F('violations__is_published'))
        ).filter(cnt__gt=0)
        cache.set("general_contractors", general_contractors, 15)

    return {'general_contractors': general_contractors}


@register.inclusion_tag('list_incident_levels.html')
def show_incident_levels():
    incident_levels = cache.get("incident_levels")
    if not incident_levels:
        incident_levels = IncidentLevel.objects.annotate(
            cnt=Count('violations', filter=F('violations__is_published'))
        ).filter(cnt__gt=0)
        cache.set("incident_levels", incident_levels, 15)

    return {'incident_levels': incident_levels}


@register.inclusion_tag('list_statuses.html')
def show_statuses():
    statuses = cache.get("statuses")
    if not statuses:
        statuses = Status.objects.annotate(
            cnt=Count('violations', filter=F('violations__is_published'))
        ).filter(cnt__gt=0)
        cache.set("statuses", statuses, 15)

    return {'statuses': statuses}


@register.inclusion_tag('list_weeks.html')
def show_weeks():

    # weeks = Week.objects.all()
    # return weeks

    weeks = Week.objects.annotate(
        cnt=Count('violations', filter=F('violations__is_published'))
    ).filter(cnt__gt=0)

    return {'weeks': weeks}
