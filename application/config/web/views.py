from apps.core.web.models import Violations
from django.views.generic import DetailView


class ViewGreetings(DetailView):
    """Просмотр определённой новости"""

    model = Violations
    template_name = 'greetings.html'
    # context_object_name = 'violations_item'
