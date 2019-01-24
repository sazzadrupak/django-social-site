from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin

# Register your models here.
from . import models


# class NormalUserInline(admin.StackedInline):
    # model = models.NormalUser


class NormalUserAdmin(admin.ModelAdmin):
    pass
    # inlines = [NormalUserInline]

    # def get_inline_instances(self, request, obj=None):
        # if not obj:
            # return list()
        # return super(NormalUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(models.NormalUser, NormalUserAdmin)
# pbkdf2_sha256$120000$jFJgwnF3XClr$OFkbrwp3jLxVUTP+BeDnfiK4eJCh6VJWwPsFZxfoOno= # admin

# pbkdf2_sha256$120000$hUVo8GMq9747$VfHRJrwNxrNETKSzY1E5rlnMlUvBrD2/nr53md1lzw4= # common