from django.contrib import messages


class MessageMixin(object):
    fields = ('name', )
    
    @property
    def success_msg(self):
        return NotImplemented
    
    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_msg)
        return super(MessageMixin, self).delete(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(MessageMixin, self).form_valid(form)
