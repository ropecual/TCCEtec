from django import forms
from .models import RegistroColeta


class RegistroColetaForm(forms.ModelForm):

    class Meta:
        model = RegistroColeta
        fields = ["tipo_residuo", "quantidade"]

        widgets = {
            "tipo_residuo": forms.Select(attrs={
                "class": "form-select"
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0.01",
                "placeholder": "Ex: 2.5"
            }),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get("quantidade")

        if quantidade is None or quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")

        return quantidade