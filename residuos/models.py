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
        on_delete=models.CASCADE,
        related_name='registros'
    )

    tipo_residuo = models.CharField(
        max_length=20,
        choices=TipoResiduo.choices
    )

    quantidade = models.FloatField()

    data = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.morador_id:
            return f"{self.morador.username} - {self.tipo_residuo} - {self.quantidade}kg"
        return f"Registro - {self.tipo_residuo}"

    def clean(self):
        """
        Validação defensiva.
        Evita erro quando o morador ainda não foi atribuído.
        """
        if not self.morador_id:
            return

        if self.morador.profile.tipo != 'MORADOR':
            raise ValidationError("Apenas moradores podem registrar resíduos.")

        if self.quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior que zero.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.morador_id:
            profile = self.morador.profile
            profile.pontos_participacao += int(self.quantidade)
            profile.save()
