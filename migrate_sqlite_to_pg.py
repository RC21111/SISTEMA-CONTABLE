import os
import django
import sqlite3
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeSoft.settings')
django.setup()

from codesoftapp.models import Periodo, Cuenta, Transaccion, ResumenCuentas, ManoDeObra, Utilidad, Capital

# Conectar a SQLite
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

print("Migrando Periodos...")
sqlite_cursor.execute("SELECT codigo, nombre FROM codesoftapp_periodo")
for codigo, nombre in sqlite_cursor.fetchall():
    Periodo.objects.create(codigo=codigo, nombre=nombre)

print("Migrando Cuentas...")
sqlite_cursor.execute("SELECT codigo, nombre FROM codesoftapp_cuenta")
for codigo, nombre in sqlite_cursor.fetchall():
    Cuenta.objects.create(codigo=codigo, nombre=nombre)

print("Migrando Transacciones...")
sqlite_cursor.execute("""
    SELECT periodo_id, codigo_id, fecha, descripcion, movimiento_debe, movimiento_haber
    FROM codesoftapp_transaccion
""")
for periodo_id, codigo_id, fecha, descripcion, movimiento_debe, movimiento_haber in sqlite_cursor.fetchall():
    # Buscar objetos relacionados
    periodo = Periodo.objects.get(codigo=periodo_id)
    cuenta = Cuenta.objects.get(codigo=codigo_id)
    Transaccion.objects.create(
        periodo=periodo,
        codigo=cuenta,
        fecha=fecha,
        descripcion=descripcion,
        movimiento_debe=Decimal(movimiento_debe),
        movimiento_haber=Decimal(movimiento_haber)
    )

print("Migrando ResumenCuentas...")
sqlite_cursor.execute("""
    SELECT periodo_id, cuenta_id, debe_total, haber_total, saldo
    FROM codesoftapp_resumencuentas
""")
for periodo_id, cuenta_id, debe_total, haber_total, saldo in sqlite_cursor.fetchall():
    periodo = Periodo.objects.get(codigo=periodo_id)
    cuenta = Cuenta.objects.get(codigo=cuenta_id)
    ResumenCuentas.objects.create(
        periodo=periodo,
        cuenta=cuenta,
        debe_total=Decimal(debe_total),
        haber_total=Decimal(haber_total),
        saldo=Decimal(saldo)
    )

print("Migrando ManoDeObra...")
sqlite_cursor.execute("""
    SELECT nombre_empleado, puesto_trabajo, pago_diario, septimo_dia, vacaciones, salario_cancelado, aguinaldo, iss, afp, insaforp, costo_real
    FROM codesoftapp_manodeobra
""")
for row in sqlite_cursor.fetchall():
    ManoDeObra.objects.create(
        nombre_empleado=row[0],
        puesto_trabajo=row[1],
        pago_diario=Decimal(row[2]),
        septimo_dia=Decimal(row[3]),
        vacaciones=Decimal(row[4]),
        salario_cancelado=Decimal(row[5]),
        aguinaldo=Decimal(row[6]),
        iss=Decimal(row[7]),
        afp=Decimal(row[8]),
        insaforp=Decimal(row[9]),
        costo_real=Decimal(row[10])
    )

print("Migrando Utilidades...")
sqlite_cursor.execute("SELECT periodo_id, valor_utilidad FROM codesoftapp_utilidad")
for periodo_id, valor_utilidad in sqlite_cursor.fetchall():
    periodo = Periodo.objects.get(codigo=periodo_id)
    Utilidad.objects.create(
        periodo=periodo,
        valor_utilidad=Decimal(valor_utilidad)
    )

print("Migrando Capitales...")
sqlite_cursor.execute("SELECT periodo_id, valor_capital FROM codesoftapp_capital")
for periodo_id, valor_capital in sqlite_cursor.fetchall():
    periodo = Periodo.objects.get(codigo=periodo_id)
    Capital.objects.create(
        periodo=periodo,
        valor_capital=Decimal(valor_capital)
    )

sqlite_conn.close()
print("¡Migración completada con éxito!")
