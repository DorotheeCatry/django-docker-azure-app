from django.db import models

class Job(models.Model):
    """
    Represents a job listing in the application.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, default="Remote")
    experience = models.CharField(max_length=100, default="Not specified")
    job_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    """
    Represents a job application submitted by a candidate.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()

    def __str__(self):
        return self.name