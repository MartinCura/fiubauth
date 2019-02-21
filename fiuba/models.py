from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.utils.translation import ugettext as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ## Roles could be extracted as classes that inherit from Profile later on
    STUDENT = 'ST'
    PROFESSOR = 'PR'
    ASSISTANT = 'AS'
    NONPROFESSOR = 'NO'
    ROLE_CHOICES = (
        (STUDENT, "estudiante"), #'Student'),
        (PROFESSOR, "profesor"), #'Professor'),
        (ASSISTANT, "ayudante"), #'Assistant'),
        (NONPROFESSOR, "no docente"), #'Non-professor'),
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
