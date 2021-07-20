from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import ThreadManager


class User(AbstractUser):
    pass


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Persona'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField(User)

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'


class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models. ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'From <Thead = {self.thread}>'