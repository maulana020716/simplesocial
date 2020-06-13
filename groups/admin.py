from django.contrib import admin
from . import models
# Register your models here.
class GroupMembersInLine(admin.TabularInLine):
    model = models.GroupMembers
admin.site.register(models.Group)
