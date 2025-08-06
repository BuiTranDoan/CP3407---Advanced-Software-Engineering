from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import StaffProfile, Shift, WorkLog, SalaryLog
from .forms import StaffUserForm, StaffProfileForm, ShiftForm, WorkLogForm
from django.contrib.auth.decorators import user_passes_test, login_required
from decorators import admin_required
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from datetime import datetime, date
from django.views.decorators.http import require_http_methods

def staff_home(request):
    return render(request, 'staff/staff_home.html')

@admin_required
def staff_list(request):
    staff_profiles = StaffProfile.objects.all()
    shifts = Shift.objects.all()
    return render(request, 'staff/staff_list.html', {'staff_profiles': staff_profiles, 'shifts': shifts})

@admin_required
def staff_add(request):
    if request.method == 'POST':
        user_form = StaffUserForm(request.POST)
        profile_form = StaffProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('staff')
    else:
        user_form = StaffUserForm()
        profile_form = StaffProfileForm()
    return render(request, 'staff/staff_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Add Staff'
    })

@admin_required
def staff_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(StaffProfile, user=user)

    if request.method == 'POST':
        user_form = StaffUserForm(request.POST, instance=user)
        profile_form = StaffProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile_form.save()
            return redirect('staff')
    else:
        user_form = StaffUserForm(instance=user)
        user_form.fields['password'].initial = ''
        profile_form = StaffProfileForm(instance=profile)

    return render(request, 'staff/staff_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Edit Staff'
    })

@admin_required
def staff_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('staff')

@login_required
def shift(request):
    shifts = Shift.objects.all()
    return render(request, 'staff/shift.html', {'shifts': shifts})

@admin_required
def shift_add(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shift')
    else:
        form = ShiftForm()
    return render(request, 'staff/shift_form.html', {'form': form, 'title': 'Add Shift'})

@admin_required
def shift_edit(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)

    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('shift')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'staff/shift_form.html', {'form': form, 'title': 'Edit Shift'})

@admin_required
def shift_delete(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    shift.delete()
    return redirect('shift')



# List all WorkLogs filtered by selected shift
def worklog_list(request):
    shift_id = request.GET.get('shift')
    shifts = Shift.objects.all().order_by('start_time')
    selected_shift = None
    staff_members = []
    logs = {}

    if shift_id:
        selected_shift = get_object_or_404(Shift, id=shift_id)
        staff_members = selected_shift.staff_members.all()
        logs = {
            staff.id: WorkLog.objects.filter(
                staff=staff, shift=selected_shift, date=date.today()
            ).first()
            for staff in staff_members
        }

    context = {
        'shifts': shifts,
        'selected_shift': selected_shift,
        'staff_members': staff_members,
        'logs': logs,
    }
    return render(request, 'staff/worklog_list.html', context)

# Clock in or update existing log
@require_http_methods(["POST"])
def clock_in(request, staff_id, shift_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    shift = get_object_or_404(Shift, id=shift_id)
    today = date.today()

    worklog, created = WorkLog.objects.get_or_create(
        staff=staff,
        shift=shift,
        date=today,
        defaults={'clock_in_time': timezone.now(), 'clock_out_time': timezone.now()}  # default same for now
    )

    if not created:
        worklog.clock_in_time = timezone.now()
        worklog.save()
        messages.success(request, "Clock-in updated.")
    else:
        messages.success(request, "Clock-in recorded.")

    return redirect(f"{reverse('worklog_list')}?shift={shift.id}")

# Clock out
@require_http_methods(["POST"])
def clock_out(request, staff_id, shift_id):
    staff = get_object_or_404(StaffProfile, id=staff_id)
    shift = get_object_or_404(Shift, id=shift_id)
    today = date.today()

    worklog = WorkLog.objects.filter(staff=staff, shift=shift, date=today).first()
    if worklog:
        worklog.clock_out_time = timezone.now()
        worklog.save()
        messages.success(request, "Clock-out recorded.")
    else:
        messages.error(request, "No clock-in record found!")

    return redirect(f"{reverse('worklog_list')}?shift={shift.id}")
