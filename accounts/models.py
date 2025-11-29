# accounts/models.py

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. Custom User Model
class User(AbstractUser):
    """
    Custom User model to allow future flexibility. 
    It inherits standard fields like username, email, password, etc.
    We'll primarily use the built-in email field.
    """
    is_seller = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True) # Default role is Client

    def __str__(self):
        return self.email or self.username

    def save(self, *args, **kwargs):
        # Ensure username is set to email if not provided (or better, make email unique and use it for login)
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


# 2. User Profile (One-to-One with User)
class UserProfile(models.Model):
    """
    Holds extra profile information not directly on the User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    profile_image = models.ImageField(
        upload_to='profiles/images/', 
        default='profiles/images/default_avatar.png', 
        blank=True
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# 3. Signals for automatic profile creation and group assignment
@receiver(post_save, sender=User)
def create_user_profile_and_assign_group(sender, instance, created, **kwargs):
    if created:
        # Create a UserProfile when a new User is created
        UserProfile.objects.create(user=instance)

        # Assign User to Client/Seller Group
        if instance.is_seller:
            group, _ = Group.objects.get_or_create(name='Seller')
            instance.groups.add(group)
        elif instance.is_client:
            group, _ = Group.objects.get_or_create(name='Client')
            instance.groups.add(group)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the profile when the User is saved
    instance.profile.save()