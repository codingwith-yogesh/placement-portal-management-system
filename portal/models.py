from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    branch = models.CharField(
        max_length=100,
        blank=True
    )

    passing_year = models.IntegerField(
        null=True,
        blank=True
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username
    
    
# company model to store company information
class Company(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    website = models.URLField(
        blank=True
    )

    location = models.CharField(
        max_length=100
    )

    description = models.TextField()

    def __str__(self):
        return self.company_name
    
# job model to store job information
class Job(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    description = models.TextField()

    package = models.IntegerField()

    minimum_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    deadline = models.DateField()

    def __str__(self):
        return self.title
    
# application model to store application information
class Application(models.Model):

    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Review', 'Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected')
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student} - {self.job}"