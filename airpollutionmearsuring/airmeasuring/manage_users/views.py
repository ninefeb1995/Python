from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from api.serializers import UserSerialization
from django.contrib.auth.models import User
from django.contrib import messages


class UserListView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, template_name='manage_users/index.html')


class UserDetailView(LoginRequiredMixin, View):

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get("_method", '').lower()
        if method == "put":
            return self.put(*args, **kwargs)
        if method == "delete":
            return self.delete(*args, **kwargs)
        return super(UserDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        instance = User.objects.get(pk=pk)
        check_type_of_user = request.POST.get('iCheck')
        copy_post = request.POST.copy()
        if check_type_of_user == 'admin':
            copy_post['is_superuser'] = 'true'
            copy_post['is_staff'] = 'false'
        else:
            copy_post['is_superuser'] = 'false'
            copy_post['is_staff'] = 'true'
        serialized = UserSerialization(data=copy_post, instance=instance)
        if serialized.is_valid():
            serialized.save()
            messages.success(request, 'Updating {} is successful'.format(instance.username))
        else:
            messages.error(request, 'Updating is failed')
        return HttpResponseRedirect(reverse('manage_users:user_list'))

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        messages.success(request, 'Deleting {} is successful'.format(user.username))
        return HttpResponseRedirect(reverse('manage_users:user_list'))


class UserNewView(LoginRequiredMixin, View):

    def post(self, request):
        check_type_of_user = request.POST.get('iCheck')
        copy_post = request.POST.copy()
        if check_type_of_user == 'admin':
            copy_post['is_superuser'] = 'true'
            copy_post['is_staff'] = 'false'
        else:
            copy_post['is_superuser'] = 'false'
            copy_post['is_staff'] = 'true'
        serialized = UserSerialization(data=copy_post)
        if serialized.is_valid():
            serialized.save()
            messages.success(request, 'Creating {} is successful'.format(copy_post.get('username')))
        else:
            messages.error(request, 'Creating is failed')
        return HttpResponseRedirect(reverse('manage_users:user_list'))


