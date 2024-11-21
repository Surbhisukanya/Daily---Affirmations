from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class Affirmation(models.Model):
    affirmation = models.TextField()
    category = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    email = models.EmailField()
    password = models.CharField(max_length=128, null=True, blank=True)  # Made nullable

    def set_password(self, raw_password):
        """Encrypt the password before saving it"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Verify if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Ensure password is hashed before saving
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
