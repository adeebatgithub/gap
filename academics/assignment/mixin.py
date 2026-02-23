from django.urls import reverse_lazy


class RedirectToFrom:
    def get_success_url(self):
        if self.request.GET.get("teacher"):
            return reverse_lazy("academics:teacher:detail", kwargs={"pk": self.request.GET.get("teacher")})

        elif self.request.GET.get("schoolclass"):
            return reverse_lazy("academics:schoolclass:detail", kwargs={"pk": self.request.GET.get("schoolclass")})

        return reverse_lazy("academics:dashboard")