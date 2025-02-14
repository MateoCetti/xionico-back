from django.db.models import Sum

from rest_framework import serializers

from ventas.models import (
    Cliente,
    Empresa,
    Producto,
    Telefono,
    Vendedor,
    VentaCabecera,
    VentaDetalle,
)


class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ["id", "numero"]


class VentaDetalleSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(
        source="producto.nombre"
    )  # Solo lectura opcional

    class Meta:
        model = VentaDetalle
        fields = [
            "producto",
            "cantidad",
            "unidad_medida",
            "producto_nombre",
        ]  # Producto como ID


class VentaCabeceraSerializer(serializers.ModelSerializer):
    monto_total = serializers.SerializerMethodField()
    vendedor_nombre = serializers.SerializerMethodField()
    cliente_nombre = serializers.SerializerMethodField()
    cantidad_productos = serializers.SerializerMethodField()
    detalles = VentaDetalleSerializer(
        many=True, write_only=True
    )  # Se envía en POST pero no se muestra en GET

    class Meta:
        model = VentaCabecera
        fields = [
            "id",
            "fecha",
            "vendedor",
            "vendedor_nombre",
            "cliente",
            "cliente_nombre",
            "gps_latitud",
            "gps_longitud",
            "monto_total",
            "cantidad_productos",
            "detalles",
        ]

    def get_monto_total(self, obj):
        return sum(
            detalle.producto.precio * detalle.cantidad for detalle in obj.detalles.all()
        )

    def get_vendedor_nombre(self, obj):
        return obj.vendedor.nombre

    def get_cliente_nombre(self, obj):
        return obj.cliente.nombre

    def get_cantidad_productos(self, obj):
        return sum(detalle.cantidad for detalle in obj.detalles.all())

    def create(self, validated_data):
        detalles_data = validated_data.pop(
            "detalles"
        )  # Extraer los detalles de la data
        venta = VentaCabecera.objects.create(**validated_data)  # Crear la cabecera

        # Crear los detalles en batch
        detalles = [
            VentaDetalle(cabezera=venta, **detalle) for detalle in detalles_data
        ]
        VentaDetalle.objects.bulk_create(detalles)

        return venta


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    tiene_ventas = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = "__all__"

    def get_tiene_ventas(self, obj):
        return obj.cliente.exists()


class VendedorSerializer(serializers.ModelSerializer):
    telefonos = TelefonoSerializer(many=True)  # Esto está bien
    empresa = serializers.PrimaryKeyRelatedField(
        queryset=Empresa.objects.all(), write_only=True
    )
    empresa_info = EmpresaSerializer(source="empresa", read_only=True)

    def validate(self, data):
        print("🔍 Datos Recibidos en validate():", data)  # 📌 Imprime los datos antes de validación
        return data
    
    class Meta:
        model = Vendedor
        fields = ["id", "nombre", "apellido", "empresa", "empresa_info", "gps_latitud", "gps_longitud", "email", "telefonos"]

    def create(self, validated_data):
        print("✅ Datos Validados (antes del pop):", validated_data)
        telefonos_data = validated_data.pop("telefonos", [])  # Extraemos los teléfonos
        print("hola")
        vendedor = Vendedor.objects.create(**validated_data)  # Creamos el vendedor

        # Creamos los teléfonos y les asignamos el vendedor automáticamente
        for telefono_data in telefonos_data:
            Telefono.objects.create(vendedor=vendedor, **telefono_data)

        return vendedor
    
    def update(self, instance, validated_data):
        # Actualizamos los campos del vendedor
        print("🔄 Actualizando Vendedor...")
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('email', instance.email)
        instance.gps_latitud = validated_data.get('gps_latitud', instance.gps_latitud)
        instance.gps_longitud = validated_data.get('gps_longitud', instance.gps_longitud)

        # Actualizamos la relación de la empresa
        instance.empresa = validated_data.get('empresa', instance.empresa)

        # Guardamos los cambios en el vendedor
        instance.save()

        # Ahora manejamos los teléfonos
        telefonos_data = validated_data.get('telefonos', None)
        if telefonos_data is not None:
            # Primero, eliminamos los teléfonos existentes asociados a este vendedor
            instance.telefonos.all().delete()

            # Luego, creamos los nuevos teléfonos
            for telefono_data in telefonos_data:
                Telefono.objects.create(vendedor=instance, **telefono_data)

        return instance



class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
