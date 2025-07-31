from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import StaffProfile
from .forms import StaffUserForm, StaffProfileForm
from django.contrib.auth.decorators import user_passes_test
from decorators import admin_required

@admin_required
def staff_list(request):
    staff_profiles = StaffProfile.objects.all()
    return render(request, 'staff/staff_list.html', {'staff_profiles': staff_profiles})

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
            return redirect('staff_list')
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
            return redirect('staff_list')
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
    return redirect('staff_list')
