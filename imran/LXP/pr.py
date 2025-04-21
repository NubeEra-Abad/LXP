import os
import subprocess

# Define project and app names
projects = [f"Project{i}" for i in range(1, 6)]
app_name = "app1"

for project in projects:
    # Create Django project
    subprocess.run(["django-admin", "startproject", project])

    # Change directory to project
    os.chdir(project)

    # Create Django app
    subprocess.run(["python", "manage.py", "startapp", app_name])

    # Modify settings.py to include the app
    settings_path = f"{project}/settings.py"
    with open(settings_path, "r") as f:
        settings = f.read()

    if f"'{app_name}'" not in settings:
        settings = settings.replace(
            "INSTALLED_APPS = [",
            f"INSTALLED_APPS = [\n    '{app_name}',"
        )

        with open(settings_path, "w") as f:
            f.write(settings)

    # Create templates directory
    templates_path = os.path.join(app_name, "templates", app_name)
    os.makedirs(templates_path, exist_ok=True)

    # Create index.html file
    index_html_path = os.path.join(templates_path, "index.html")
    with open(index_html_path, "w") as f:
        f.write("<h1>Welcome to the Home Page of {}</h1>".format(project))

    # Modify views.py
    views_path = os.path.join(app_name, "views.py")
    with open(views_path, "w") as f:
        f.write(f"""
from django.shortcuts import render

def home(request):
    return render(request, '{app_name}/index.html')
""")

    # Delete existing urls.py in project if it exists
    project_urls_path = os.path.join(project, "urls.py")
    if os.path.exists(project_urls_path):
        os.remove(project_urls_path)

    # Create new urls.py with only the required content for the app
    with open(project_urls_path, "w") as f:
        f.write(f"""
from django.urls import path
from {app_name}.views import home

urlpatterns = [
    path('', home, name='home'),
]
""")

    # Run migrations
    subprocess.run(["python", "manage.py", "migrate"])

    # Create requirements.txt
    requirements_path = os.path.join(os.getcwd(), "requirements.txt")
    with open(requirements_path, "w") as f:
        f.write("Django>=4.0\n")

    # Go back to the root directory
    os.chdir("..")

print("All 5 Django projects and apps created successfully with requirements.txt!")
