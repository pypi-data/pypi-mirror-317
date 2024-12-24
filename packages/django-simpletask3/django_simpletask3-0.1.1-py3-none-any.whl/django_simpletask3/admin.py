from django.contrib import admin
from django.contrib.auth import get_permission_codename


class SimpleTaskAdmin(admin.ModelAdmin):

    def has_django_simpletask3_execute_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("django_simpletask3_execute", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_django_simpletask3_reset_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("django_simpletask3_reset", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result
