from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('recycler', 'Recycler'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class EWaste(models.Model):

    CATEGORY_CHOICES = [
        ('mobile', 'Mobile'),
        ('laptop', 'Laptop'),
        ('tv', 'TV'),
        ('battery', 'Battery'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('working', 'Working'),
        ('broken', 'Broken'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('Picked', 'Picked'),
        ('completed', 'Completed'),
    ]

    TIME_SLOT_CHOICES = [
        ('10-12', '10 AM - 12 PM'),
        ('12-2', '12 PM - 2 PM'),
        ('2-4', '2 PM - 4 PM'),
        ('4-6', '4 PM - 6 PM'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    recycler = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_requests'
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    weight = models.FloatField()
    photo = models.ImageField(upload_to='ewaste_photos/')
    location = models.CharField(max_length=255)

    # ✅ NEW FIELDS (Pickup Scheduling)
    pickup_date = models.DateField(null=True, blank=True)
    pickup_time_slot = models.CharField(
        max_length=20,
        choices=TIME_SLOT_CHOICES,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.status}"