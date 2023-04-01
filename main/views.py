from django.views.generic.base import TemplateView

from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'main/index.html'
    title = 'Shop'
