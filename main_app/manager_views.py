import json
import requests

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

from .forms import *
from .models import *


def manager_home(request):
    manager = get_object_or_404(Manager, admin=request.user)
    total_projectEngineers = ProjectEngineer.objects.all().count()
    total_leave = LeaveReportManager.objects.filter(manager=manager).count()
    tasks = Task.objects.filter(manager=manager)
    total_task = tasks.count()
    attendance_list = Attendance.objects.filter(task__in=tasks)
    total_attendance = attendance_list.count()
    attendance_list = []
    task_list = []
    for task in tasks:
        attendance_count = Attendance.objects.filter(task=task).count()
        task_list.append(task.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'Manager Panel - ' + str(manager.admin.last_name) + ' (' + str(manager.track) + ')',
        'total_projectEngineers': total_projectEngineers,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_task': total_task,
        'task_list': task_list,
        'attendance_list': attendance_list
    }
    return render(request, 'manager_template/home_content.html', context)


def add_projectEngineer(request):
    projectEngineer_form = ProjectEngineerForm(request.POST or None, request.FILES or None)
    context = {'form': projectEngineer_form, 'page_title': 'Add Project Engineer'}
    
    if request.method == 'POST':
        if projectEngineer_form.is_valid():
            first_name = projectEngineer_form.cleaned_data.get('first_name')
            last_name = projectEngineer_form.cleaned_data.get('last_name')
            address = projectEngineer_form.cleaned_data.get('address')
            email = projectEngineer_form.cleaned_data.get('email')
            gender = projectEngineer_form.cleaned_data.get('gender')
            password = projectEngineer_form.cleaned_data.get('password')
            track = projectEngineer_form.cleaned_data.get('track')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            
            try:
                user = CustomUser.objects.create_user(email=email, password=password, user_type=3,first_name=first_name, last_name=last_name, profile_pic=passport_url) # type: ignore
                user.gender = gender
                user.address = address
                user.save()

                # Track can be set after profile is created
                user.projectEngineer.track = track
                user.projectEngineer.save()
                
                messages.success(request, "Successfully Added")
                return redirect(reverse('manager_add_projectEngineer'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")
    
    return render(request, 'manager_template/add_projectEngineer_template.html', context)

def manage_projectEngineer(request):
    projectEngineers = CustomUser.objects.filter(user_type=3)
    context = {
        'projectEngineers': projectEngineers,
        'page_title': 'Manage Project Engineers'
    }
    return render(request, "manager_template/manage_projectEngineer.html", context)

def edit_projectEngineer(request, projectEngineer_id):
    projectEngineer = get_object_or_404(ProjectEngineer, id=projectEngineer_id)
    form = ProjectEngineerForm(request.POST or None, instance=projectEngineer)
    context = {
        'form': form,
        'projectEngineer_id': projectEngineer_id,
        'page_title': 'Edit Project Engineer'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            track = form.cleaned_data.get('track')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=projectEngineer.admin.id) # type: ignore
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url # type: ignore
                user.username = username
                user.email = email # type: ignore
                if password != None:
                    user.set_password(password)
                user.first_name = first_name # type: ignore
                user.last_name = last_name # type: ignore
                user.gender = gender # type: ignore
                user.address = address # type: ignore
                projectEngineer.track = track
                user.save()
                projectEngineer.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('manager_edit_projectEngineer', args=[projectEngineer_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "manager_template/edit_projectEngineer_template.html", context)

def delete_projectEngineer(request, projectEngineer_id):
    projectEngineer = get_object_or_404(CustomUser, projectEngineer__id=projectEngineer_id)
    projectEngineer.delete()
    messages.success(request, "Project Engineer deleted successfully!")
    return redirect(reverse('manager_manage_projectEngineer'))

def manager_notify_projectEngineer(request):
    projectEngineer = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Project Engineers",
        'projectEngineers': projectEngineer
    }
    return render(request, "manager_template/projectEngineer_notification.html", context)



def manager_take_attendance(request):
    manager = get_object_or_404(Manager, admin=request.user)
    tasks = Task.objects.filter(manager=manager)
    context = {
        'tasks': tasks,
        'page_title': 'Take Attendance'
    }

    return render(request, 'manager_template/manager_take_attendance.html', context)


@csrf_exempt
def get_projectEngineers(request):
    task_id = request.POST.get('task')
    try:
        task = get_object_or_404(Task, id=task_id)
        projectEngineers = ProjectEngineer.objects.filter(
            track_id=task.track.id) # type: ignore
        projectEngineer_data = []
        for projectEngineer in projectEngineers:
            data = {
                    "id": projectEngineer.id, # type: ignore
                    "name": projectEngineer.admin.last_name + " " + projectEngineer.admin.first_name
                    }
            projectEngineer_data.append(data)
        return JsonResponse(json.dumps(projectEngineer_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def projectEngineer_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackProjectEngineer.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Project Engineer Feedback Messages'
        }
        return render(request, 'manager_template/projectEngineer_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackProjectEngineer, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def manager_send_projectEngineer_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    projectEngineer = get_object_or_404(ProjectEngineer, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Project Engineer Management System",
                'body': message,
                'click_action': reverse('projectEngineer_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': projectEngineer.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationProjectEngineer(projectEngineer=projectEngineer, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def manager_view_projectEngineer_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportProjectEngineer.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Project Engineers'
        }
        return render(request, "manager_template/projectEngineer_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportProjectEngineer, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def manager_projectEngineer_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackProjectEngineer.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Project Engineer Feedback Messages'
        }
        return render(request, 'manager_template/projectEngineer_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackProjectEngineer, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)
     

@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        projectEngineer_data = request.POST.get('projectEngineer_ids')
        date = request.POST.get('date')
        task_id = request.POST.get('task')
        
        if not projectEngineer_data or not date or not task_id:
            return JsonResponse({'status': 'error', 'message': 'Missing required data'})
        
        projectEngineers = json.loads(projectEngineer_data)
        try:
            task = get_object_or_404(Task, id=task_id)
            attendance = Attendance(task=task, date=date)
            attendance.save()

            for projectEngineer_dict in projectEngineers:
                projectEngineer = get_object_or_404(ProjectEngineer, id=projectEngineer_dict.get('id'))
                attendance_report = AttendanceReport(
                    projectEngineer=projectEngineer,
                    attendance=attendance,
                    status=projectEngineer_dict.get('status')
                )
                attendance_report.save()
                
            return JsonResponse({'status': 'OK'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def manager_update_attendance(request):
    manager = get_object_or_404(Manager, admin=request.user)
    tasks = Task.objects.filter(manager=manager)
    context = {
        'tasks': tasks,
        'page_title': 'Update Attendance'
    }

    return render(request, 'manager_template/manager_update_attendance.html', context)


@csrf_exempt
def get_projectEngineer_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        projectEngineer_data = []
        for attendance in attendance_data:
            data = {"id": attendance.projectEngineer.admin.id, # type: ignore
                    "name": attendance.projectEngineer.admin.last_name + " " + attendance.projectEngineer.admin.first_name,
                    "status": attendance.status}
            projectEngineer_data.append(data)
        return JsonResponse(json.dumps(projectEngineer_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    projectEngineer_data = request.POST.get('projectEngineer_ids')
    date = request.POST.get('date')
    projectEngineers = json.loads(projectEngineer_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for projectEngineer_dict in projectEngineers:
            projectEngineer = get_object_or_404(
                ProjectEngineer, admin_id=projectEngineer_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, projectEngineer=projectEngineer, attendance=attendance)
            attendance_report.status = projectEngineer_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def manager_apply_leave(request):
    form = LeaveReportManagerForm(request.POST or None)
    manager = get_object_or_404(Manager, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportManager.objects.filter(manager=manager),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.manager = manager
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('manager_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "manager_template/manager_apply_leave.html", context)


def manager_feedback(request):
    form = FeedbackManagerForm(request.POST or None)
    manager = get_object_or_404(Manager, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackManager.objects.filter(manager=manager),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.manager = manager
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('manager_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "manager_template/manager_feedback.html", context)


def manager_view_profile(request):
    manager = get_object_or_404(Manager, admin=request.user)
    form = ManagerEditForm(request.POST or None, request.FILES or None,instance=manager)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = manager.admin
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
                manager.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('manager_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "manager_template/manager_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "manager_template/manager_view_profile.html", context)

    return render(request, "manager_template/manager_view_profile.html", context)


@csrf_exempt
def manager_fcmtoken(request):
    token = request.POST.get('token')
    try:
        manager_user = get_object_or_404(CustomUser, id=request.user.id)
        manager_user.fcm_token = token
        manager_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def manager_view_notification(request):
    manager = get_object_or_404(Manager, admin=request.user)
    notifications = NotificationManager.objects.filter(manager=manager)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "manager_template/manager_view_notification.html", context)


def manager_add_result(request):
    manager = get_object_or_404(Manager, admin=request.user)
    tasks = Manager.objects.filter(admin=manager.admin)
    context = {
        'page_title': 'Result Upload',
        'tasks': tasks
    }
    if request.method == 'POST':
        try:
            projectEngineer_id = request.POST.get('projectEngineer_list')
            task_id = request.POST.get('task')
            weekly = request.POST.get('weekly')
            monthly = request.POST.get('monthly')
            projectEngineer = get_object_or_404(ProjectEngineer, id=projectEngineer_id)
            task = get_object_or_404(Task, id=task_id)
            try:
                data = ProjectEngineerResult.objects.get(
                    projectEngineer=projectEngineer, task=task)
                data.monthly = monthly # type: ignore
                data.weekly = weekly # type: ignore
                data.save()
                messages.success(request, "Scores Updated")
            except:
                result = ProjectEngineerResult(projectEngineer=projectEngineer, task=task, weekly=weekly, monthly=monthly)
                result.save()
                messages.success(request, "Scores Saved")
        except Exception as e:
            messages.warning(request, "Error Occured While Processing Form")
    return render(request, "manager_template/manager_add_result.html", context)


@csrf_exempt
def fetch_projectEngineer_result(request):
    try:
        task_id = request.POST.get('task')
        projectEngineer_id = request.POST.get('projectEngineer')
        projectEngineer = get_object_or_404(ProjectEngineer, id=projectEngineer_id)
        task = get_object_or_404(Task, id=task_id)
        result = ProjectEngineerResult.objects.get(projectEngineer=projectEngineer, task=task)
        result_data = {
            'monthly': result.monthly, # type: ignore
            'weekly': result.weekly # type: ignore
        }
        return HttpResponse(json.dumps(result_data))
    except Exception as e:
        return HttpResponse('False')
