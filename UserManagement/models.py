from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from CreateDataGenerationTask.models import Task as DataGenerationTask
from CreateDataAnnotationTask.models import Task as DataAnnotationTask


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to = 'assets/images',
        default = 'no-img.jpg',
        blank=True
    )
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='none@email.com')
    bio = models.TextField(default='')
    is_contributor = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    country = models.CharField(max_length=255, default='')
    field = models.CharField(max_length=255, default='')


    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)



class ContributorTask(models.Model):
    TaskID = models.IntegerField(null=False,blank=False)
    UserID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_data_annotation_task = models.BooleanField(default=False)
    is_data_generation_task = models.BooleanField(default=False)


