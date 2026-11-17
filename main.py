import logging
from modelos_base import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from excepciones import ErrorSoftwareFJ

def ejecutar_simulacion():
    print("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    clientes = []
    servicios = []
    reservas = []

    # 1. Registro válido de cliente 1
    try:
        c1 = Cliente("CLI-01", "Kevin Romero", "kevin.romero@unad.edu.co")
        clientes.append(c1)
        print(f"[OK] Operación 1: {c1.obtener_resumen()}")
    except ErrorSoftwareFJ as e:
        logging.error(f"Op 1 fallida: {e}")

    # 2. Registro inválido de cliente (nombre corto)
    try:
        c_malo = Cliente("CLI-02", "Al", "correo_sin_arroba")
        clientes.append(c_malo)
    except ErrorSoftwareFJ as e:
        logging.error(f"Op 2 fallida (esperada): {e}")
        print(f"[ERROR CONTROLADO] Operación 2: {e}")

    # 3. Registro válido de cliente 2
    try:
        c2 = Cliente("CLI-03", "Laura Gómez", "laura.gomez@empresa.com")
        clientes.append(c2)
        print(f"[OK] Operación 3: {c2.obtener_resumen()}")
    except ErrorSoftwareFJ as e:
        logging.error(f"Op 3 fallida: {e}")

    # 4. Creación correcta de servicio: Sala
    try:
        s1 = ReservaSala("SRV-01", "Sala de Juntas Norte", 50000, capacidad=10)
        servicios.append(s1)
        print(f"[OK] Operación 4: {s1.obtener_resumen()}")
    except ErrorSoftwareFJ as e:
        logging.error(f"Op 4 fallida: {e}")

    # 5. Creación incorrecta de servicio (tarifa negativa)
    try:
        s_malo = AlquilerEquipo("SRV-02", "Portátil Gamer", -15000, gama="Alta")
        servicios.append(s_malo)
    except ErrorSoftwareFJ as e:
        logging.error(f"Op 5 fallida (esperada): {e}")
        print(f"[ERROR CONTROLADO] Operación 5: {e}")

    # 6. Creación correcta de servicio: Equipo y Asesoría
    try:
        s2 = AlquilerEquipo("SRV-03", "Workstation Render 3D", 35000, gama="Profesional")
        s3 = AsesoriaEspecializada("SRV-04", "Arquitectura Cloud", 80000, especialidad="DevOps")
        servicios.extend([s2, s3])
        print(f"[OK] Operación 6: Creados {s2.obtener_resumen()} y {s3.obtener_resumen()}")
    except ErrorSoftwareFJ as e:
        logging.error(f"Op 6 fallida: {e}")

    # 7. Reserva exitosa con descuento (sobrecarga de parámetros)
    try:
        r1 = Reserva("RES-01", c1, s1, horas=4)
        r1.procesar_y_confirmar(descuento=0.10)  # 10% de descuento
        reservas.append(r1)
        print(f"[OK] Operación 7: {r1.obtener_resumen()}")
    except ErrorSoftwareFJ as e:
        print(f"[ERROR CONTROLADO] Operación 7: {e}")

    # 8. Reserva fallida: intentar reservar la misma sala que ya quedó ocupada
    try:
        r2 = Reserva("RES-02", c2, s1, horas=2)
        r2.procesar_y_confirmar()
    except ErrorSoftwareFJ as e:
        print(f"[ERROR CONTROLADO] Operación 8 (Encadenada): {e} -> Causa: {e.__cause__}")

    # 9. Reserva fallida: equipo por menos de 2 horas (regla de negocio)
    try:
        r3 = Reserva("RES-03", c2, s2, horas=1)
        r3.procesar_y_confirmar()
    except ErrorSoftwareFJ as e:
        print(f"[ERROR CONTROLADO] Operación 9 (Encadenada): {e} -> Causa: {e.__cause__}")

    # 10. Reserva exitosa de Asesoría con bono automático (>5 horas) y posterior cancelación
    try:
        r4 = Reserva("RES-04", c2, s3, horas=6)
        r4.procesar_y_confirmar()
        reservas.append(r4)
        print(f"[OK] Operación 10a: {r4.obtener_resumen()}")
        r4.cancelar()
        print(f"[OK] Operación 10b (Cancelación): {r4.obtener_resumen()}")
    except ErrorSoftwareFJ as e:
        print(f"[ERROR CONTROLADO] Operación 10: {e}")

    print("\n=== EJECUCIÓN FINALIZADA SIN INTERRUPCIONES. REVISE 'sistema_fj.log' ===")

if __name__ == "__main__":
    ejecutar_simulacion()
