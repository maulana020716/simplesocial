from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMembers

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('group:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMembers.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'warning already a member')
        else:
            messages.success(self.request,'You are now a member')
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('group:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:

            memberships = models.GroupMembers.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMembers.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            memberships.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
