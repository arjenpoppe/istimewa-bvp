from django.db import models


# Create your models here.
class Permissions(models.Model):
    class Meta:
        permissions = (("input_datafile", "Can upload datafile"),
                       ("input_form", "Can submit form"),
                       ("view_forms", "Can view forms"),
                       ("generate_reports", "Can generate reports"),
                       ("manage_app", "Can manage application"),
                       ("view_logs", "Can view log files"),
                       ("edit_data", "Can edit data"),
                       ("export_data", "Can export data"),
                       ("view_dashboard", "Can view dashboard"),
                       ("prestatiemeting", "Can execute a prestatiemeting"))