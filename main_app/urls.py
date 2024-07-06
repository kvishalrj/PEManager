from django.urls import include, path

from main_app.EditResultView import EditResultView

from . import hod_views, manager_views, projectEngineer_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'), # type: ignore
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("manager/add", hod_views.add_manager, name='add_manager'),
    path("track/add", hod_views.add_track, name='add_track'),
    path("send_projectEngineer_notification/", hod_views.send_projectEngineer_notification,
         name='send_projectEngineer_notification'),
    path("send_manager_notification/", hod_views.send_manager_notification,
         name='send_manager_notification'),
    path("admin_notify_projectEngineer", hod_views.admin_notify_projectEngineer,
         name='admin_notify_projectEngineer'),
    path("admin_notify_manager", hod_views.admin_notify_manager,
         name='admin_notify_manager'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("projectEngineer/view/feedback/", hod_views.projectEngineer_feedback_message,
         name="projectEngineer_feedback_message",),
    path("manager/view/feedback/", hod_views.manager_feedback_message,
         name="manager_feedback_message",),
    path("projectEngineer/view/leave/", hod_views.view_projectEngineer_leave, # type: ignore
         name="view_projectEngineer_leave",),
    path("manager/view/leave/", hod_views.view_manager_leave, name="view_manager_leave",), # type: ignore
    path("attendance/view/", hod_views.admin_view_attendance, name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance, name='get_admin_attendance'), # type: ignore
    path("projectEngineer/add/", hod_views.add_projectEngineer, name='add_projectEngineer'),
    path("task/add/", hod_views.add_task, name='add_task'),
    path("manager/manage/", hod_views.manage_manager, name='manage_manager'),
    path("projectEngineer/manage/", hod_views.manage_projectEngineer, name='manage_projectEngineer'),
    path("track/manage/", hod_views.manage_track, name='manage_track'),
    path("task/manage/", hod_views.manage_task, name='manage_task'),
    path("manager/edit/<int:manager_id>", hod_views.edit_Manager, name='edit_manager'),
    path("manager/delete/<int:manager_id>",
         hod_views.delete_manager, name='delete_manager'),

    path("track/delete/<int:track_id>",
         hod_views.delete_track, name='delete_track'),

    path("task/delete/<int:task_id>",
         hod_views.delete_task, name='delete_task'),

    path("projectEngineer/delete/<int:projectEngineer_id>",
         hod_views.delete_projectEngineer, name='delete_projectEngineer'),
    path("projectEngineer/edit/<int:projectEngineer_id>",
         hod_views.edit_projectEngineer, name='edit_projectEngineer'),
    path("track/edit/<int:track_id>",
         hod_views.edit_track, name='edit_track'),
    path("task/edit/<int:task_id>",
         hod_views.edit_task, name='edit_task'),


    # Manager
    path("manager/home/", manager_views.manager_home, name='manager_home'),
    path("manager/task/manage/", manager_views.manage_task, name='manager_manage_task'),
    path("manager/task/edit/<int:task_id>", manager_views.edit_task, name='manager_edit_task'),

    path('manager/projectEngineer/manage/', manager_views.manage_projectEngineer, name='manager_manage_projectEngineer'),
    path("manager/projectEngineer/add/", manager_views.add_projectEngineer,name='manager_add_projectEngineer'),
    path("manager/projectEngineer/delete/<int:projectEngineer_id>", manager_views.delete_projectEngineer, name='manager_delete_projectEngineer'),
    path("manager/projectEngineer/edit/<int:projectEngineer_id>", manager_views.edit_projectEngineer, name='manager_edit_projectEngineer'),
    path("manager_notify_projectEngineer", manager_views.manager_notify_projectEngineer,
         name='manager_notify_projectEngineer'),
    path("manager_send_projectEngineer_notification/", manager_views.manager_send_projectEngineer_notification,name='manager_send_projectEngineer_notification'),
    path("manager/projectEngineer/view/leave/", manager_views.manager_view_projectEngineer_leave, name="manager_view_projectEngineer_leave",), # type: ignore
    path("manager/projectEngineer/view/feedback/", manager_views.manager_projectEngineer_feedback_message, name="manager_projectEngineer_feedback_message",), # type: ignore


    path("manager/apply/leave/", manager_views.manager_apply_leave,
         name='manager_apply_leave'),
    path("manager/feedback/", manager_views.manager_feedback, name='manager_feedback'),
    path("manager/view/profile/", manager_views.manager_view_profile,
         name='manager_view_profile'),
    path("manager/attendance/take/", manager_views.manager_take_attendance,
         name='manager_take_attendance'),
    path("manager/attendance/update/", manager_views.manager_update_attendance,
         name='manager_update_attendance'),
    path("manager/get_projectEngineers/", manager_views.get_projectEngineers, name='get_projectEngineers'), # type: ignore
    path("manager/attendance/fetch/", manager_views.get_projectEngineer_attendance, name='get_projectEngineer_attendance'), # type: ignore
    path("manager/attendance/save/", manager_views.save_attendance, name='save_attendance'), # type: ignore
    path("manager/attendance/update/", manager_views.update_attendance, name='update_attendance'), # type: ignore
    path("manager/fcmtoken/", manager_views.manager_fcmtoken, name='manager_fcmtoken'),
    path("manager/view/notification/", manager_views.manager_view_notification,
         name="manager_view_notification"),
    path("manager/result/add/", manager_views.manager_add_result, name='manager_add_result'),
    path("manager/result/edit/", EditResultView.as_view(),
         name='edit_projectEngineer_result'),
    path('manager/result/fetch/', manager_views.fetch_projectEngineer_result,
         name='fetch_projectEngineer_result'),



    # ProjectEngineer
    path("projectEngineer/home/", projectEngineer_views.projectEngineer_home, name='projectEngineer_home'),
    path("projectEngineer/view/attendance/", projectEngineer_views.projectEngineer_view_attendance, name='projectEngineer_view_attendance'), # type: ignore
    path("projectEngineer/apply/leave/", projectEngineer_views.projectEngineer_apply_leave,
         name='projectEngineer_apply_leave'),
    path("projectEngineer/feedback/", projectEngineer_views.projectEngineer_feedback,
         name='projectEngineer_feedback'),
    path("projectEngineer/view/profile/", projectEngineer_views.projectEngineer_view_profile,
         name='projectEngineer_view_profile'),
    path("projectEngineer/fcmtoken/", projectEngineer_views.projectEngineer_fcmtoken,
         name='projectEngineer_fcmtoken'),
    path("projectEngineer/view/notification/", projectEngineer_views.projectEngineer_view_notification,
         name="projectEngineer_view_notification"),
    path('projectEngineer/view/result/', projectEngineer_views.projectEngineer_view_result,
         name='projectEngineer_view_result'),

]
