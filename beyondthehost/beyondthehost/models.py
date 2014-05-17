class OwnedMixin(object):
    def get_queryset(self):
        base_qs = super(OwnedMixin, self).get_queryset()
        return base_qs.filter(owner=self.request.user)
