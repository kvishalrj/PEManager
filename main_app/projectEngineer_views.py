import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def projectEngineer_home(request):
    projectEngineer = get_object_or_404(ProjectEngineer, admin=request.user)
    total_task = Task.objects.filter(track=projectEngineer.track).count()
    total_attendance = AttendanceReport.objects.filter(projectEngineer=projectEngineer).count()
    total_present = AttendanceReport.objects.filter(projectEngineer=projectEngineer, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    task_name = []
    data_present = []
    data_absent = []
    tasks = Task.objects.filter(track=projectEngineer.track)
    for task in tasks:
        attendance = Attendance.objects.filter(task=task)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, projectEngineer=projectEngineer).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, projectEngineer=projectEngineer).count()
        task_name.append(task.name)
        data_present.append(present_count)
        data_absent.append(absent_count)
    context = {
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_task': total_task,
        'tasks': tasks,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': task_name,
        'page_title': 'ProjectEngineer Homepage'

    }
    return render(request, 'projectEngineer_template/home_content.html', context)


@ csrf_exempt
def projectEngineer_view_attendance(request):
    projectEngineer = get_object_or_404(ProjectEngineer, admin=request.user)
    if request.method != 'POST':
        track = get_object_or_404(Track, id=projectEngineer.track.id) # type: ignore
        context = {
            'tasks': Task.objects.filter(track=track),
            'page_title': 'View Attendance'
        }
        return render(request, 'projectEngineer_template/projectEngineer_view_attendance.html', context)
    else:
        task_id = request.POST.get('task')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            task = get_object_or_404(Task, id=task_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), task=task)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, projectEngineer=projectEngineer)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def projectEngineer_apply_leave(request):
    form = LeaveReportProjectEngineerForm(request.POST or None)
    projectEngineer = get_object_or_404(ProjectEngineer, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportProjectEngineer.objects.filter(projectEngineer=projectEngineer),
        'page_title': 'Apply for leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.projectEngineer = projectEngineer
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('projectEngineer_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "projectEngineer_template/projectEngineer_apply_leave.html", context)


def projectEngineer_feedback(request):
    form = FeedbackProjectEngineerForm(request.POST or None)
    projectEngineer = get_object_or_404(ProjectEngineer, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackProjectEngineer.objects.filter(projectEngineer=projectEngineer),
        'page_title': 'ProjectEngineer Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.projectEngineer = projectEngineer
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('projectEngineer_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "projectEngineer_template/projectEngineer_feedback.html", context)


def projectEngineer_view_profile(request):
    projectEngineer = get_object_or_404(ProjectEngineer, admin=request.user)
    form = ProjectEngineerEditForm(request.POST or None, request.FILES or None,
                           instance=projectEngineer)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = projectEngineer.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url # type: ignore
                admin.first_name = first_name # type: ignore
                admin.last_name = last_name # type: ignore
                admin.address = address # type: ignore
                admin.gender = gender # type: ignore
                admin.save()
                projectEngineer.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('projectEngineer_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "projectEngineer_template/projectEngineer_view_profile.html", context)


@csrf_exempt
def projectEngineer_fcmtoken(request):
    token = request.POST.get('token')
    projectEngineer_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        projectEngineer_user.fcm_token = token
        projectEngineer_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def projectEngineer_view_notification(request):
    projectEngineer = get_object_or_404(ProjectEngineer, admin=request.user)
    notifications = NotificationProjectEngineer.objects.filter(projectEngineer=projectEngineer)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "projectEngineer_template/projectEngineer_view_notification.html", context)


def projectEngineer_view_result(request):
    projectEngineer = get_object_or_404(ProjectEngineer, admin=request.user)
    results = ProjectEngineerResult.objects.filter(projectEngineer=projectEngineer)
    context = {
        'results': results,
        'page_title': "View Results"
    }
    return render(request, "projectEngineer_template/projectEngineer_view_result.html", context)
