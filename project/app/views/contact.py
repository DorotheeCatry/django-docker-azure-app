from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .models import ContactMessage

def contact_view(request):
    """
    Handles contact form submissions.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, "insurance_app/contact_form.html")

def contact_view_user(request):
    """
    Handles contact form submissions for logged-in users.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact_form')
    return render(request, "insurance_app/contact_form_user.html")

@staff_member_required
def message_list_view(request):
    """
    Displays a list of contact messages for staff members.
    """
    messages = ContactMessage.objects.all().order_by('-submitted_at')
    return render(request, "insurance_app/messages_list.html", {"messages": messages})

@csrf_exempt
def solve_message(request, message_id):
    """
    Handles the deletion of a contact message.
    """
    if request.method == 'POST':
        try:
            contact_message = ContactMessage.objects.get(id=message_id)
            contact_message.delete()
            return JsonResponse({'success': True})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)