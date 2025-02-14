from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    nombre = models.CharField(max_length=250)


class Cliente(models.Model):
    codigo = models.CharField(max_length=250)
    nombre = models.CharField(max_length=250)
    direccion = models.CharField(max_length=250)
    categoria = models.CharField(max_length=250)


class Vendedor(models.Model):
    nombre = models.CharField(max_length=250)
    apellido = models.CharField(max_length=250)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="empresa"
    )
    gps_latitud = models.FloatField()
    gps_longitud = models.FloatField()
    email = models.CharField(max_length=250)


class Telefono(models.Model):
    numero = models.CharField(max_length=12)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="telefonos")


class VentaCabecera(models.Model):
    fecha = models.DateField()
    # empresa = models.CharField(max_length=250) # El vendedor esta linkeado a una empresa
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name="vendedor"
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="cliente"
    )
    gps_latitud = models.FloatField()
    gps_longitud = models.FloatField()

    def __str__(self):
        return f"Venta {self.id} - ({self.fecha})"


class Producto(models.Model):
    codigo = models.CharField(max_length=250)
    nombre = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class VentaDetalle(models.Model):
    cabezera = models.ForeignKey(
        VentaCabecera, on_delete=models.CASCADE, related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="producto"
    )
    cantidad = models.IntegerField()
    unidad_medida = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cantidad} {self.unidad_medida} de {self.producto.nombre}"


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="usuarios"
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.nombre}"
