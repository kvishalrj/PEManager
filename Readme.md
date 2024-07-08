# PEManager💻

## Description

#### PEManager is a comprehensive project management system designed to facilitate the administration and organization of project engineers and managers within an organization. This system employs a three-layer architecture to ensure smooth interaction and role-specific functionalities for administrators, managers, and project engineers.

>## Tech Stack

- Frontend: HTML, CSS, JavaScript, Bootstrap, JQuery

- Backend: Django

- Database: PostgreSQL

- Templating: Jinja

- Programming Language: Python

>## Features

### Admin Layer

- Profile Management: Update profile details.

- User Management: Register managers and project engineers, edit profiles, and delete users.

- Notifications: Send individual notifications.

- Leave Management: Approve or deny leave applications.

- Feedback Handling: Check and reply to feedback from managers and project engineers.

- Task Management: Assign tasks, track progress, and manage tasks.

- Meeting Scheduling: Schedule meetings using a custom calendar.

- Availability Check: View the availability of registered individuals via their calendars.

#### Admin Layer screenshots
![](/images/1.png)
![](/images/2.png)
![](/images/3.png)
![](/images/4.png)

### Manager Layer

- Profile Management: Update profile details.

- Project Engineer Management: Add, edit, and delete project engineers.

- Notifications: Send notifications to project engineers.

- Leave Management: Approve or deny leave applications of project engineers.

- Feedback Handling: Check feedback from project engineers.

- Calendar Management: View and manage the calendar of any project engineer, including task assignment.

- Attendance and Results: Take attendance and provide results to project engineers.

#### Manager Layer screenshots
![](/images/5.png)
![](/images/6.png)
![](/images/7.png)

### Project Engineer Layer

- Profile Management: Update profile details.

- Calendar Management: Check and update their own calendar.

- Leave Management: Apply for leave.

- Feedback: Send feedback to managers or the admin.

- Attendance and Results: View attendance and results.

#### Project Engineer Layer Screenshots
![](/images/10.png)
![](/images/8.png)
![](/images/9.png)

>## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/kvishalrj/PEManager.git
cd PEManager
```

### 2. Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies:

```bash
pip install -r requirements.txt
```
    
### 4. Configure the database:

- Update the DATABASES setting in settings.py with your PostgreSQL database details or you can also use built in SQLite database.

### 5. Run migrations:

```bash
python manage.py migrate
```
    
### 6. Create a superuser:

```bash
python manage.py createsuperuser
```
    
### 7. Start the development server:

```bash
python manage.py runserver
```

>## Usage
- Access the login at http://127.0.0.1:8000 

- Each user (admin, manager, project engineer) can log in and access their respective dashboards and functionalities.

>## Contributing
We welcome contributions! 

Please fork the repository and submit a pull request for any improvements or fixes.

### For any questions or support, please contact kvishalrj2020@gmail.com.



