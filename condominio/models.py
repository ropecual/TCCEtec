from django.db import models


class Condominio(models.Model):
    nome = models.CharField(max_length=150)
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return self.nome


class Bloco(models.Model):
    nome = models.CharField(max_length=50)
    condominio = models.ForeignKey(
        Condominio,
        on_delete=models.CASCADE,
        related_name="blocos"
    )

    def __str__(self):
        return f"{self.nome} - {self.condominio.nome}"


class UnidadeHabitacional(models.Model):
    numero = models.CharField(max_length=10)
    bloco = models.ForeignKey(
        Bloco,
        on_delete=models.CASCADE,
        related_name="unidades"
    )

    def __str__(self):
        return f"Apto {self.numero} - {self.bloco.nome}"
