from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    TIPO_CHOICES = (
        ('MORADOR', 'Morador'),
        ('ADMIN', 'Administrador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='MORADOR')
    pontos_participacao = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"




@receiver(post_save, sender=User)
def criar_ou_atualizar_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
