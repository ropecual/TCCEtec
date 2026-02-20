from django import forms
from .models import Condominio, Bloco, UnidadeHabitacional


class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = "__all__"

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cep": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "bairro": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(attrs={"class": "form-control text-uppercase"}),
        }




class BlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = "__all__"

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Bloco A"
            }),
            "condominio": forms.Select(attrs={
                "class": "form-select"
            }),
        }



class UnidadeHabitacionalForm(forms.ModelForm):
    class Meta:
        model = UnidadeHabitacional
        fields = "__all__"

        widgets = {
            "numero": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: 101"
            }),
            "bloco": forms.Select(attrs={
                "class": "form-select"
            }),
        }