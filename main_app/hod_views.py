import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *


def admin_home(request):
    total_manager = Manager.objects.all().count()
    total_projectEngineers = ProjectEngineer.objects.all().count()
    tasks = Task.objects.all()
    total_task = tasks.count()
    total_track = Track.objects.all().count()
    attendance_list = Attendance.objects.filter(task__in=tasks)
    total_attendance = attendance_list.count()
    attendance_list = []
    task_list = []
    for task in tasks:
        attendance_count = Attendance.objects.filter(task=task).count()
        task_list.append(task.name[:7])
        attendance_list.append(attendance_count)

    # Total tasks and projectEngineers in Each Track
    track_all = Track.objects.all()
    track_name_list = []
    task_count_list = []
    projectEngineer_count_list_in_track = []

    for track in track_all:
        tasks = Task.objects.filter(track_id=track.id).count() # type: ignore
        projectEngineers = ProjectEngineer.objects.filter(track_id=track.id).count() # type: ignore
        track_name_list.append(track.name)
        task_count_list.append(tasks)
        projectEngineer_count_list_in_track.append(projectEngineers)
    
    task_all = Task.objects.all()
    task_list = []
    projectEngineer_count_list_in_task = []
    for task in task_all:
        track = Track.objects.get(id=task.track.id) # type: ignore
        projectEngineer_count = ProjectEngineer.objects.filter(track_id=track.id).count() # type: ignore
        task_list.append(task.name)
        projectEngineer_count_list_in_task.append(projectEngineer_count)


    # For ProjectEngineers
    projectEngineer_attendance_present_list=[]
    projectEngineer_attendance_leave_list=[]
    projectEngineer_name_list=[]

    projectEngineers = ProjectEngineer.objects.all()
    for projectEngineer in projectEngineers:
        
        attendance = AttendanceReport.objects.filter(projectEngineer_id=projectEngineer.id, status=True).count() # type: ignore
        absent = AttendanceReport.objects.filter(projectEngineer_id=projectEngineer.id, status=False).count() # type: ignore
        leave = LeaveReportProjectEngineer.objects.filter(projectEngineer_id=projectEngineer.id, status=1).count() # type: ignore
        projectEngineer_attendance_present_list.append(attendance)
        projectEngineer_attendance_leave_list.append(leave+absent)
        projectEngineer_name_list.append(projectEngineer.admin.first_name)

    context = {
        'page_title': "Administrative Dashboard",
        'total_projectEngineers': total_projectEngineers,
        'total_manager': total_manager,
        'total_track': total_track,
        'total_task': total_task,
        'task_list': task_list,
        'attendance_list': attendance_list,
        'projectEngineer_attendance_present_list': projectEngineer_attendance_present_list,
        'projectEngineer_attendance_leave_list': projectEngineer_attendance_leave_list,
        "projectEngineer_name_list": projectEngineer_name_list,
        "projectEngineer_count_list_in_task": projectEngineer_count_list_in_task,
        "projectEngineer_count_list_in_track": projectEngineer_count_list_in_track,
        "track_name_list": track_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)


def add_manager(request):
    manager_form = ManagerForm(request.POST or None, request.FILES or None)
    context = {'form': manager_form, 'page_title': 'Add Manager'}

    if request.method == 'POST':
        if manager_form.is_valid():
            first_name = manager_form.cleaned_data.get('first_name')
            last_name = manager_form.cleaned_data.get('last_name')
            address = manager_form.cleaned_data.get('address')
            email = manager_form.cleaned_data.get('email')
            gender = manager_form.cleaned_data.get('gender')
            password = manager_form.cleaned_data.get('password')
            track = manager_form.cleaned_data.get('track')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url) # type: ignore
                user.gender = gender
                user.address = address
                user.save()

                # Track can be set after profile is created
                user.manager.track = track
                user.manager.save()

                messages.success(request, "Successfully Added")
                return redirect(reverse('add_manager'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Please fulfill all requirements")

    return render(request, 'hod_template/add_manager_template.html', context)


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
                return redirect(reverse('add_projectEngineer'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")
    
    return render(request, 'hod_template/add_projectEngineer_template.html', context)


def add_track(request):
    form = TrackForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Track'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                track = Track()
                track.name = name # type: ignore
                track.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_track'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_track_template.html', context)


def add_task(request):
    form = TaskForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Task'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            track = form.cleaned_data.get('track')
            manager = form.cleaned_data.get('manager')
            try:
                task = Task()
                task.name = name # type: ignore
                task.manager = manager # type: ignore
                task.track = track # type: ignore
                task.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_task'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod_template/add_task_template.html', context)


def manage_manager(request):
    allManager = CustomUser.objects.filter(user_type=2)
    context = {
        'allManager': allManager,
        'page_title': 'Manage Manager'
    }
    return render(request, "hod_template/manage_manager.html", context)


def manage_projectEngineer(request):
    projectEngineers = CustomUser.objects.filter(user_type=3)
    context = {
        'projectEngineers': projectEngineers,
        'page_title': 'Manage Project Engineers'
    }
    return render(request, "hod_template/manage_projectEngineer.html", context)


def manage_track(request):
    tracks = Track.objects.all()
    context = {
        'tracks': tracks,
        'page_title': 'Manage Tracks'
    }
    return render(request, "hod_template/manage_track.html", context)


def manage_task(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
        'page_title': 'Manage Tasks'
    }
    return render(request, "hod_template/manage_task.html", context)


def edit_Manager(request, manager_id):
    manager = get_object_or_404(Manager, id=manager_id)
    form = ManagerForm(request.POST or None, instance=manager)
    context = {
        'form': form,
        'manager_id': manager_id,
        'page_title': 'Edit Manager'
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
                user = CustomUser.objects.get(id=manager.admin.id) # type: ignore
                user.username = username
                user.email = email # type: ignore
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url # type: ignore
                user.first_name = first_name # type: ignore
                user.last_name = last_name # type: ignore
                user.gender = gender # type: ignore
                user.address = address # type: ignore
                manager.track = track
                user.save()
                manager.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_manager', args=[manager_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=manager_id)
        manager = Manager.objects.get(id=user.id) # type: ignore
        return render(request, "hod_template/edit_manager_template.html", context)


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
                return redirect(reverse('edit_projectEngineer', args=[projectEngineer_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_projectEngineer_template.html", context)


def edit_track(request, track_id):
    instance = get_object_or_404(Track, id=track_id)
    form = TrackForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'track_id': track_id,
        'page_title': 'Edit Track'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                track = Track.objects.get(id=track_id)
                track.name = name # type: ignore
                track.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_track_template.html', context)


def edit_task(request, task_id):
    instance = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'task_id': task_id,
        'page_title': 'Edit Task'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            track = form.cleaned_data.get('track')
            manager = form.cleaned_data.get('manager')
            try:
                task = Task.objects.get(id=task_id)
                task.name = name # type: ignore
                task.manager = manager # type: ignore
                task.track = track # type: ignore
                task.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_task', args=[task_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'hod_template/edit_task_template.html', context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def projectEngineer_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackProjectEngineer.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Project Engineer Feedback Messages'
        }
        return render(request, 'hod_template/projectEngineer_feedback_template.html', context)
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
def manager_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackManager.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Manager Feedback Messages'
        }
        return render(request, 'hod_template/manager_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackManager, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_manager_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportManager.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Manager'
        }
        return render(request, "hod_template/manager_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportManager, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_projectEngineer_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportProjectEngineer.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Project Engineers'
        }
        return render(request, "hod_template/projectEngineer_leave_view.html", context)
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


def admin_view_attendance(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
        'page_title': 'View Attendance'
    }
    print("attendance")
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def get_admin_attendance(request):
    task_id = request.POST.get('task')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        task = get_object_or_404(Task, id=task_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status":  str(report.status),
                "name": str(report.projectEngineer)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url # type: ignore
                custom_user.first_name = first_name # type: ignore
                custom_user.last_name = last_name # type: ignore
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_manager(request):
    manager = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Manager",
        'allManager': manager
    }
    return render(request, "hod_template/manager_notification.html", context)


def admin_notify_projectEngineer(request):
    projectEngineer = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Project Engineers",
        'projectEngineers': projectEngineer
    }
    return render(request, "hod_template/projectEngineer_notification.html", context)


@csrf_exempt
def send_projectEngineer_notification(request):
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
def send_manager_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    manager = get_object_or_404(Manager, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Project Engineer Management System",
                'body': message,
                'click_action': reverse('manager_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': manager.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationManager(manager=manager, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_manager(request, manager_id):
    manager = get_object_or_404(CustomUser, manager__id=manager_id)
    manager.delete()
    messages.success(request, "Manager deleted successfully!")
    return redirect(reverse('manage_manager'))


def delete_projectEngineer(request, projectEngineer_id):
    projectEngineer = get_object_or_404(CustomUser, projectEngineer__id=projectEngineer_id)
    projectEngineer.delete()
    messages.success(request, "Project Engineer deleted successfully!")
    return redirect(reverse('manage_projectEngineer'))


def delete_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    try:
        track.delete()
        messages.success(request, "Track deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some projectEngineers are assigned to this track already. Kindly change the affected projectEngineer track and try again")
    return redirect(reverse('manage_track'))


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect(reverse('manage_task'))



