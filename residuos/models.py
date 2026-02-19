from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class TipoResiduo(models.TextChoices):
    PAPEL = 'PAPEL', 'Papel'
    PLASTICO = 'PLASTICO', 'Plástico'
    VIDRO = 'VIDRO', 'Vidro'
    METAL = 'METAL', 'Metal'
    ORGANICO = 'ORGANICO', 'Orgânico'
    OUTROS = 'OUTROS', 'Outros'




class RegistroColeta(models.Model):

    morador = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    tipo_residuo = models.CharField(
        max_length=20,
        choices=TipoResiduo.choices
    )

    quantidade = models.FloatField()

    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.morador.username} - {self.tipo_residuo} - {self.quantidade}kg"

    def clean(self):
        if self.morador.profile.tipo != 'MORADOR':
            raise ValidationError("Apenas moradores podem registrar resíduos.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile = self.morador.profile
        profile.pontos_participacao += int(self.quantidade)
        profile.save()
