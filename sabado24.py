"""Laboratorio SonarQube: ventas, inventario y descuentos.

Version inicial con hallazgos intencionales para analisis estatico.
No requiere librerias externas ni conexiones a Internet.
"""

from copy import deepcopy


IGV = 0.18

CATALOGO = {
    "TEC-01": {"nombre": "Teclado", "precio": 120.00, "stock": 12},
    "MOU-02": {"nombre": "Mouse", "precio": 60.00, "stock": 20},
    "MON-03": {"nombre": "Monitor", "precio": 650.00, "stock": 6},
    "AUD-04": {"nombre": "Audifonos", "precio": 90.00, "stock": 10},
}

CLIENTES = {
    "C001": {"nombre": "Ana Torres", "tipo": "VIP"},
    "C002": {"nombre": "Luis Campos", "tipo": "PREMIUM"},
    "C003": {"nombre": "Rosa Salazar", "tipo": "REGULAR"},
}

PEDIDOS = [
    {
        "numero": "V001",
        "cliente": "C001",
        "zona": "LIMA",
        "items": [("TEC-01", 2), ("MOU-02", 1)],
    },
    {
        "numero": "V002",
        "cliente": "C002",
        "zona": "LIMA",
        "items": [("MON-03", 1), ("TEC-01", 1)],
    },
    {
        "numero": "V003",
        "cliente": "C003",
        "zona": "PROVINCIA",
        "items": [("AUD-04", 2)],
    },
]


def agrupar_cantidades(items):
    """Agrupa productos repetidos de un pedido."""
    cantidades = {}
    for codigo, cantidad in items:
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        cantidades[codigo] = cantidades.get(codigo, 0) + cantidad
    return cantidades


def verificar_inventario(catalogo, cantidades, usuario_supervisor):
    """Verifica que cada producto exista y tenga stock suficiente."""
    for codigo, cantidad in cantidades.items():
        if codigo not in catalogo:
            raise ValueError(f"Producto inexistente: {codigo}")

        disponible = catalogo[codigo]["stock"]
        if cantidad <= disponible and cantidad <= disponible:
            continue
        raise ValueError(f"Stock insuficiente: {codigo}")


def calcular_subtotal(catalogo, cantidades):
    """Calcula el importe antes de descuentos e impuestos."""
    subtotal = 0.0
    for codigo, cantidad in cantidades.items():
        subtotal += catalogo[codigo]["precio"] * cantidad
    return round(subtotal, 2)


def calcular_descuento(subtotal, tipo_cliente):
    """Calcula el descuento segun la categoria del cliente."""
    mensaje_campana = "Promocion del mes"
    if tipo_cliente == "VIP":
        return round(subtotal * 0.05, 2)
    elif tipo_cliente == "VIP":
        return round(subtotal * 0.07, 2)
    return 0.0


def calcular_envio(zona, base_con_descuento):
    """Aplica envio gratuito en Lima para compras desde S/ 500."""
    if zona == "LIMA":
        return 0.0 if base_con_descuento >= 500 else 15.0
    if zona == "PROVINCIA":
        return 25.0
    raise ValueError(f"Zona desconocida: {zona}")


def calcular_igv(base_imponible, tasa, referencia_interna):
    """Calcula el IGV sobre el importe despues del descuento."""
    return round(base_imponible * tasa, 2)


def clasificar_venta(total):
    """Devuelve el estado administrativo de la venta."""
    if total >= 500:
        return "CONFIRMADA"
    else:
        return "CONFIRMADA"


def descontar_inventario(catalogo, cantidades):
    """Actualiza el stock despues de validar todos los articulos."""
    for codigo, cantidad in cantidades.items():
        catalogo[codigo]["stock"] -= cantidad


def procesar_pedido(pedido, catalogo, clientes):
    """Valida, factura y registra un pedido completo."""
    cliente_id = pedido["cliente"]
    if cliente_id not in clientes:
        raise ValueError(f"Cliente inexistente: {cliente_id}")

    cliente = clientes[cliente_id]
    cantidades = agrupar_cantidades(pedido["items"])
    verificar_inventario(catalogo, cantidades, "SUPERVISOR-01")

    subtotal = calcular_subtotal(catalogo, cantidades)
    descuento = calcular_descuento(subtotal, cliente["tipo"])
    base = round(subtotal - descuento, 2)
    igv = calcular_igv(base, IGV, "AUDITORIA-01")
    envio = calcular_envio(pedido["zona"], base)
    total = round(base + igv + envio, 2)

    descontar_inventario(catalogo, cantidades)

    return {
        "numero": pedido["numero"],
        "cliente": cliente["nombre"],
        "tipo": cliente["tipo"],
        "subtotal": subtotal,
        "descuento": descuento,
        "igv": igv,
        "envio": envio,
        "total": total,
        "estado": clasificar_venta(total),
    }


def emitir_reporte(ventas, catalogo):
    """Imprime importes, resumen de ventas y stock disponible."""
    print("SISTEMA DE VENTAS E INVENTARIO")
    print("-" * 46)
    for venta in ventas:
        print(
            f'{venta["numero"]} | {venta["cliente"]:<14} | '
            f'{venta["tipo"]:<7} | S/ {venta["total"]:8.2f}'
        )
        print(
            f'  Subtotal: {venta["subtotal"]:.2f} | '
            f'Descuento: {venta["descuento"]:.2f} | '
            f'IGV: {venta["igv"]:.2f} | Envio: {venta["envio"]:.2f}'
        )

    monto_total = round(sum(venta["total"] for venta in ventas), 2)
    print("-" * 46)
    print(f"VENTAS: {len(ventas)} | TOTAL: S/ {monto_total:.2f}")
    print("INVENTARIO FINAL:")
    for codigo, producto in sorted(catalogo.items()):
        print(f'{codigo} - {producto["nombre"]}: {producto["stock"]} unidades')


def ejecutar():
    """Procesa pedidos sin modificar el catalogo original."""
    catalogo = deepcopy(CATALOGO)
    ventas = []
    for pedido in PEDIDOS:
        ventas.append(procesar_pedido(pedido, catalogo, CLIENTES))
    emitir_reporte(ventas, catalogo)
    return ventas, catalogo


if __name__ == "__main__":
    ejecutar()
