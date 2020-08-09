from django.db import models


class Cupom(models.Model):

    STATUS = (
        ('Ativo', 'Ativo'),
        ('Expirado', 'Expirado'),
        ('Utilizado', 'Utilizado'),
    )

    codigo = models.CharField(max_length=255, primary_key=True)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    dataExpiracao = models.DateField()
    dataUso = models.DateField(null=True, editable=False)
    situacao = models.CharField(
        max_length=30,
        choices=STATUS,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.codigo
