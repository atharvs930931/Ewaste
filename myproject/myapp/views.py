from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import EWaste
from django.db.models import Count
import json
from datetime import date
from .models import EWaste
from django.shortcuts import render
from .models import EWaste
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncWeek, TruncDate




@login_required
def submit_ewaste(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        weight = request.POST.get('weight')
        location = request.POST.get('location')
        photo = request.FILES.get('photo')
        pickup_date = request.POST.get('pickup_date')
        pickup_time_slot = request.POST.get('pickup_time_slot')

        # ✅ Basic validation
        if not all([category, condition, weight, location, photo, pickup_date, pickup_time_slot]):
            messages.error(request, "All fields are required")
            return redirect('submit_ewaste')

        # ✅ Past date block
        if pickup_date < str(date.today()):
            messages.error(request, "Past date not allowed")
            return redirect('submit_ewaste')

        # ✅ Slot limit check (max 5 per slot)
        booking_count = EWaste.objects.filter(
            pickup_date=pickup_date,
            pickup_time_slot=pickup_time_slot
        ).count()

        if booking_count >= 5:
            messages.error(request, "This time slot is fully booked. Please select another.")
            return redirect('submit_ewaste')

        # ✅ Save to DB
        EWaste.objects.create(
            user=request.user,
            category=category,
            condition=condition,
            weight=weight,
            location=location,
            photo=photo,
            pickup_date=pickup_date,
            pickup_time_slot=pickup_time_slot
        )

        messages.success(request, "Pickup Scheduled Successfully!")
        return redirect('submit_ewaste')

    return render(request, 'submit_ewaste.html', {
        'today': date.today().isoformat()
    })

def home(request):
    return render(request, 'index.html')


def about_page(request):
    return render(request, 'about_us.html')



def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # empty role check
        if not role:
            messages.error(request, "Please select a role")
            return redirect('register')

        # duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # save role in profile
        UserProfile.objects.create(
            user=user,
            role=role
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')   # 👈 LOGIN PAGE ला जाईल

    return render(request, 'register.html')




def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')   # 👈 dropdown मधून येतो

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)

                # role mismatch
                if profile.role != role:
                    messages.error(request, "Please select correct role")
                    return redirect('login')

                login(request, user)


                # ✅ ROLE BASED REDIRECT
                if role == 'user':
                    return redirect('submit_ewaste')      # page अजून तयार नाही
                elif role == 'recycler':
                    return redirect('accept_ewaste')      # page अजून तयार नाही
                elif role == 'admin':
                    return redirect('admin_portal')       # page अजून तयार नाही

            except UserProfile.DoesNotExist:
                messages.error(request, "User role not found")
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')




@login_required
def status_tracking(request):
    ewaste_list = EWaste.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'status_tracking.html', {
        'ewaste_list': ewaste_list
    })




def logout_view(request):
    logout(request)
    return redirect('home')




@login_required
def submit_ewaste(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        weight = request.POST.get('weight')
        location = request.POST.get('location')
        photo = request.FILES.get('photo')
        pickup_date = request.POST.get('pickup_date')
        pickup_time_slot = request.POST.get('pickup_time_slot')

        # ✅ Basic validation
        if not all([category, condition, weight, location, photo, pickup_date, pickup_time_slot]):
            messages.error(request, "All fields are required")
            return redirect('submit_ewaste')

        # ✅ Past date block
        if pickup_date < str(date.today()):
            messages.error(request, "Past date not allowed")
            return redirect('submit_ewaste')

        # ✅ Slot limit check (max 5 per slot)
        booking_count = EWaste.objects.filter(
            pickup_date=pickup_date,
            pickup_time_slot=pickup_time_slot
        ).count()

        if booking_count >= 5:
            messages.error(request, "This time slot is fully booked. Please select another.")
            return redirect('submit_ewaste')

        # ✅ Save to DB
        EWaste.objects.create(
            user=request.user,
            category=category,
            condition=condition,
            weight=weight,
            location=location,
            photo=photo,
            pickup_date=pickup_date,
            pickup_time_slot=pickup_time_slot
        )

        messages.success(request, "Pickup Scheduled Successfully!")
        return redirect('submit_ewaste')

    return render(request, 'submit_ewaste.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import EWaste

@login_required
def accept_ewaste(request):
    # Only recycler access
    profile = request.user.userprofile
    if profile.role != 'recycler':
        return HttpResponse("Unauthorized", status=403)

    # 🔁 Handle Status Update
    if request.method == "POST":
        ewaste_id = request.POST.get("ewaste_id")
        action = request.POST.get("action")

        ewaste = get_object_or_404(EWaste, id=ewaste_id)

        # Optional: prevent other recycler editing
        # if ewaste.recycler and ewaste.recycler != request.user:
        #     return HttpResponse("Not allowed", status=403)

        if action == "accept":
            ewaste.status = "accepted"

        elif action == "picked":
            ewaste.status = "picked"

        elif action == "complete":
            ewaste.status = "completed"

        ewaste.save()
        return redirect("accept_ewaste")

    # 📦 Fetch Data by Status
    pending_requests = EWaste.objects.filter(status='pending')
    accepted_requests = EWaste.objects.filter(status='accepted')
    picked_requests = EWaste.objects.filter(status='picked')
    completed_requests = EWaste.objects.filter(status='completed')

    context = {
        'pending': pending_requests,
        'accepted': accepted_requests,
        'picked': picked_requests,
        'completed': completed_requests,
    }

    return render(request, 'accept_ewaste.html', context)


@login_required
def accept_request(request, ewaste_id):
    profile = request.user.userprofile
    if profile.role != 'recycler':
        return HttpResponse("Unauthorized", status=403)

    ewaste = EWaste.objects.get(id=ewaste_id)
    ewaste.status = 'accepted'
    ewaste.recycler = request.user
    ewaste.save()

    messages.success(request, "E-Waste accepted successfully")
    return redirect('accept_ewaste')








def dashboard(request):

    total_requests = EWaste.objects.count()
    accepted = EWaste.objects.filter(status='accepted').count()
    pending = EWaste.objects.filter(status='pending').count()
    completed = EWaste.objects.filter(status='completed').count()

    labels = ['Mobile','Laptop','TV','Battery','Other']

    data = [
        EWaste.objects.filter(category='mobile').count(),
        EWaste.objects.filter(category='laptop').count(),
        EWaste.objects.filter(category='tv').count(),
        EWaste.objects.filter(category='battery').count(),
        EWaste.objects.filter(category='other').count(),
    ]

    context = {
        'total_requests': total_requests,
        'accepted': accepted,
        'pending': pending,
        'completed': completed,
        'labels': json.dumps(labels),
        'data': json.dumps(data)
    }

    return render(request,'dashboard.html',context)









def reports(request):

    data = {
        'submitted':0,
        'accepted':0,
        'picked':0,
        'completed':0
    }

    month = request.GET.get('month')
    week = request.GET.get('week')
    day = request.GET.get('day')

    if month:
        year, month = month.split('-')

        data['submitted'] = EWaste.objects.filter(created_at__year=year, created_at__month=month).count()
        data['accepted'] = EWaste.objects.filter(status='accepted', created_at__year=year, created_at__month=month).count()
        data['picked'] = EWaste.objects.filter(status='picked', created_at__year=year, created_at__month=month).count()
        data['completed'] = EWaste.objects.filter(status='completed', created_at__year=year, created_at__month=month).count()

    elif week:
        year, week = week.split('-W')

        data['submitted'] = EWaste.objects.filter(created_at__week=week).count()
        data['accepted'] = EWaste.objects.filter(status='accepted', created_at__week=week).count()
        data['picked'] = EWaste.objects.filter(status='picked', created_at__week=week).count()
        data['completed'] = EWaste.objects.filter(status='completed', created_at__week=week).count()

    elif day:
        data['submitted'] = EWaste.objects.filter(created_at__date=day).count()
        data['accepted'] = EWaste.objects.filter(status='accepted', created_at__date=day).count()
        data['picked'] = EWaste.objects.filter(status='picked', created_at__date=day).count()
        data['completed'] = EWaste.objects.filter(status='completed', created_at__date=day).count()

    return render(request,'reports.html',{
        'data':data
    })


def admin_portal(request):
    return HttpResponse("Admin Portal under development")