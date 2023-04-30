class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        """Returns context[title] for classes with inline value"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
