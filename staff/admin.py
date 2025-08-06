from django.contrib import admin
from staff.models import StaffProfile, Shift, Position, SalaryLog, WorkLog

admin.site.register(StaffProfile)
admin.site.register(Shift)
admin.site.register(Position)
admin.site.register(SalaryLog)
admin.site.register(WorkLog)