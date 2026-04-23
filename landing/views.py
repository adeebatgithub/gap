from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "landing/home_v1.html"

    def get_template_names(self):
        if v := self.request.GET.get("ver"):
            return f"landing/home_{v}.html"
        return super().get_template_names()
