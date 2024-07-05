from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from .models import Task, Manager, ProjectEngineer, ProjectEngineerResult
from .forms import EditResultForm
from django.urls import reverse


class EditResultView(View):
    def get(self, request, *args, **kwargs):
        resultForm = EditResultForm()
        manager = get_object_or_404(Manager, admin=request.user)
        resultForm.fields['task'].queryset = Task.objects.filter(manager=manager)
        context = {
            'form': resultForm,
            'page_title': "Edit ProjectEngineer's Result"
        }
        return render(request, "manager_template/edit_projectEngineer_result.html", context)

    def post(self, request, *args, **kwargs):
        form = EditResultForm(request.POST)
        context = {'form': form, 'page_title': "Edit ProjectEngineer's Result"}
        if form.is_valid():
            try:
                projectEngineer = form.cleaned_data.get('projectEngineer')
                task = form.cleaned_data.get('task')
                weekly = form.cleaned_data.get('weekly')
                monthly = form.cleaned_data.get('monthly')
                # Validating
                result = ProjectEngineerResult.objects.get(projectEngineer=projectEngineer, task=task)
                result.monthly = monthly # type: ignore
                result.weekly = weekly # type: ignore
                result.save()
                messages.success(request, "Result Updated")
                return redirect(reverse('edit_projectEngineer_result'))
            except Exception as e:
                messages.warning(request, "Result Could Not Be Updated")
        else:
            messages.warning(request, "Result Could Not Be Updated")
        return render(request, "manager_template/edit_projectEngineer_result.html", context)
