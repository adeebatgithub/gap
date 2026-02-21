class RedirectToDetail:
    param_key = "back_to"
    param_val = "detail"
    detail_url = None

    def get_detail_url(self):
        if self.detail_url is None:
            raise NotImplementedError("detail_url must be defined.")
        return self.detail_url

    def get_success_url(self):
        if self.request.GET.get(self.param_key) == self.param_val:
            return self.get_detail_url()
        return super().get_success_url()
