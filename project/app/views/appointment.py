from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import AppointmentForm
from .models import Appointment, Availability
from django.http import JsonResponse

@login_required
def book_appointment(request):
    """
    Handles appointment booking.
    """
    today = timezone.now().date()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Your appointment has been booked successfully!')
            return redirect('book_appointment')
    else:
        form = AppointmentForm()

    upcoming_appointments = Appointment.objects.filter(
        user=request.user, date__gte=today
    ).order_by('date')

    past_appointments = Appointment.objects.filter(
        user=request.user, date__lt=today
    ).order_by('-date')

    return render(request, 'insurance_app/book_appointment.html', {
        'today': today,
        'form': form,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    })

def get_available_times(request):
    """
    Retrieves available time slots for a given date.
    """
    if date := request.GET.get('date'):
        try:
            availability = Availability.objects.get(date=date)
            return JsonResponse({"times": availability.time_slots})
        except Availability.DoesNotExist:
            return JsonResponse({"times": []})
    return JsonResponse({"times": []})