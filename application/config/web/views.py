from django.views.generic import DetailView

from apps.core.web.models import Violations


class ViewGreetings(DetailView):
    """Просмотр определённой новости"""

    model = Violations
    template_name = 'greetings.html'
    # context_object_name = 'violations_item'
