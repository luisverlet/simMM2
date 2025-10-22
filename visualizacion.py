import numpy as np
from vpython import sphere, box, label, color, canvas, vector, rate
from simulacion import simular_mm2
from parametros import LAMBDA, MU, SERVIDORES
import math


def mm2_statistics(LAMBDA, MU, SERVIDORES):
    ro = LAMBDA / (SERVIDORES * MU)
    sum_terms = sum([(LAMBDA / MU) ** n / math.factorial(n) for n in range(SERVIDORES)])
    term_s = (LAMBDA / MU) ** SERVIDORES / (math.factorial(SERVIDORES) * (1 - ro))
    P0 = 1.0 / (sum_terms + term_s)
    Lq = (P0 * ((LAMBDA / MU) ** SERVIDORES) * ro) / (math.factorial(SERVIDORES) * ((1 - ro) ** 2))
    L = Lq + LAMBDA / MU
    Wq = Lq / LAMBDA
    W = Wq + 1 / MU
    Pb = P0 * ((LAMBDA / MU) ** SERVIDORES) / math.factorial(SERVIDORES) * (ro / (1 - ro))
    return dict(P0=P0, ro=ro, Lq=Lq, L=L, Wq=Wq, W=W, Pb=Pb)


resultados = mm2_statistics(LAMBDA, MU, SERVIDORES)
resultados_label_text = (
    f"Parámetros del Sistema\n"
    f"λ: {LAMBDA:.2f} veh/min\n"
    f"μ: {MU:.2f} veh/min/servidor\n"
    f"Tiempo medio servicio: {60/MU:.2f} s\n"
    f"Servidores: {SERVIDORES}\n\n"
    f"Resultados del Modelo\n"
    f"P₀ (sistema vacío): {resultados['P0']:.4f} ({resultados['P0']*100:.2f}%)\n"
    f"ρ (utilización): {resultados['ro']:.3f} ({resultados['ro']*100:.1f}%)\n"
    f"Lq (veh en cola): {resultados['Lq']:.2f}\n"
    f"L (total): {resultados['L']:.2f}\n"
    f"Wq (cola): {resultados['Wq']*60:.1f} seg\n"
    f"W (total): {resultados['W']*60:.1f} seg\n"
    f"P ambos ocupados: {resultados['Pb']:.3f} ({resultados['Pb']*100:.1f}%)"
)


scene = canvas(title="Simulación MM2 Tráfico Y", width=1920, height=1080)
scene.background = color.gray(0.15)
scene.fullscreen = True
scene.autoscale = False


CARRIL_LARGO = 12
POSTRAMAL_X = 6
POS_ENTRADA_X = -CARRIL_LARGO / 2 + 1
POS_RAMAL_X = POSTRAMAL_X
RAMAL_LARGO = 6
RAMAL_DESVIO = 2.3
POS_SALIDA_X = POS_RAMAL_X + RAMAL_LARGO + 1.2
DISTANCIA_ENTRE_BOLAS = 0.8
DURACION = 60


# Carretera principal y ramales (con salida larga)
box(pos=vector((POS_ENTRADA_X + POS_RAMAL_X) / 2, 0, 0), size=vector(POS_RAMAL_X - POS_ENTRADA_X, 0.12, 0.7), color=color.gray(0.4))
box(pos=vector(POS_RAMAL_X + RAMAL_LARGO / 2, 0, RAMAL_DESVIO / 2), size=vector(RAMAL_LARGO, 0.12, 0.7), color=color.gray(0.4))
box(pos=vector(POS_RAMAL_X + RAMAL_LARGO / 2, 0, -RAMAL_DESVIO / 2), size=vector(RAMAL_LARGO, 0.12, 0.7), color=color.gray(0.4))
box(pos=vector(POS_RAMAL_X + RAMAL_LARGO + 0.6, 0, RAMAL_DESVIO / 2), size=vector(1.2, 0.12, 0.7), color=color.gray(0.35))
box(pos=vector(POS_RAMAL_X + RAMAL_LARGO + 0.6, 0, -RAMAL_DESVIO / 2), size=vector(1.2, 0.12, 0.7), color=color.gray(0.35))


servidor_pos = [vector(POS_RAMAL_X + RAMAL_LARGO, 0, RAMAL_DESVIO / 2), vector(POS_RAMAL_X + RAMAL_LARGO, 0, -RAMAL_DESVIO / 2)]
servidores = [box(pos=servidor_pos[i], size=vector(1, 0.6, 0.85), color=color.blue) for i in range(SERVIDORES)]


datos_label = label(
    pos=vector(POS_ENTRADA_X, 2, 0),
    text=resultados_label_text,
    height=17,
    box=True,
    color=color.white,
    background=color.gray(0.25),
    border=10,
    opacity=0.78
)


eventos = simular_mm2(DURACION)


autos, estado, destino, servidor_de_auto = [], [], [], []
tiempo_llegada_servidor = []  # NUEVO: registrar cuando llega al servidor

for i, evento in enumerate(eventos):
    s = sphere(pos=vector(POS_ENTRADA_X - i * DISTANCIA_ENTRE_BOLAS, 0.22, 0), radius=0.27, color=color.red)
    autos.append(s)
    estado.append("esperando")
    destino.append((POS_ENTRADA_X - i * DISTANCIA_ENTRE_BOLAS, 0))
    servidor_de_auto.append(None)
    tiempo_llegada_servidor.append(None)  # NUEVO


servidores_ocupados = [None, None]  # None = libre, id_auto = ocupado
servidores_bloqueados = [False, False]  # Para evitar asignaciones duplicadas


dt = 0.03
t = 0
vel_avance = 1.2
vel_desvio = 1.8
vel_salida = 2.0
DISTANCIA_MINIMA = 0.6


def hay_espacio_adelante(idx, autos, estado):
    auto_actual = autos[idx]
    for j in range(len(autos)):
        if j == idx or not autos[j].visible:
            continue
        auto_otro = autos[j]
        if estado[idx] in ["esperando", "avanzando"] and estado[j] in ["esperando", "avanzando", "en_bifurcacion"]:
            if abs(auto_otro.pos.z - auto_actual.pos.z) < 0.3:
                if auto_otro.pos.x > auto_actual.pos.x and auto_otro.pos.x - auto_actual.pos.x < DISTANCIA_MINIMA:
                    return False
        if estado[idx] in ["desviando", "en_ramal"] and estado[j] in ["desviando", "en_ramal", "atendiendo"]:
            if abs(auto_otro.pos.z - auto_actual.pos.z) < 0.5:
                if auto_otro.pos.x > auto_actual.pos.x and auto_otro.pos.x - auto_actual.pos.x < DISTANCIA_MINIMA:
                    return False
    return True


while t < DURACION + 30:
    # 1. Liberar servidores cuando termine el tiempo de servicio
    for s in range(SERVIDORES):
        if servidores_ocupados[s] is not None:
            idx = servidores_ocupados[s]
            evento = eventos[idx]
            # CORREGIDO: verificar que haya pasado el tiempo de servicio desde que llegó al servidor
            if tiempo_llegada_servidor[idx] is not None and evento.duracion_servicio is not None:
                tiempo_en_servidor = t - tiempo_llegada_servidor[idx]
                if tiempo_en_servidor >= evento.duracion_servicio and estado[idx] == "atendiendo":
                    estado[idx] = "saliendo"
                    destino[idx] = (POS_SALIDA_X, servidor_pos[servidor_de_auto[idx]].z)
                    servidores_ocupados[s] = None
                    servidores_bloqueados[s] = False


    # 2. Procesamiento de cada vehículo
    for i, evento in enumerate(eventos):
        if not autos[i].visible:
            continue
        auto = autos[i]


        # Estado: esperando
        if estado[i] == "esperando":
            if evento.tiempo_inicio_servicio is not None and t >= evento.tiempo_inicio_servicio:
                servidor_asignado = None
                for s in range(SERVIDORES):
                    if servidores_ocupados[s] is None and not servidores_bloqueados[s]:
                        servidor_asignado = s
                        servidores_ocupados[s] = i
                        servidores_bloqueados[s] = True
                        break
                if servidor_asignado is not None:
                    estado[i] = "avanzando"
                    servidor_de_auto[i] = servidor_asignado
                    destino[i] = (POS_RAMAL_X - 0.3, 0)
            else:
                autos_delante = sum(
                    1
                    for j in range(i)
                    if estado[j] in ["esperando"]
                    and eventos[j].tiempo_inicio_servicio is not None
                    and t < eventos[j].tiempo_inicio_servicio
                )
                pos_x_objetivo = POS_RAMAL_X - 1.5 - autos_delante * DISTANCIA_ENTRE_BOLAS
                if hay_espacio_adelante(i, autos, estado):
                    dx = pos_x_objetivo - auto.pos.x
                    if abs(dx) > 0.02:
                        auto.pos.x += np.clip(dx, -vel_avance * dt, vel_avance * dt)
                auto.pos.z = 0
                auto.color = color.red


        # Estado: avanzando hacia bifurcación
        elif estado[i] == "avanzando":
            if hay_espacio_adelante(i, autos, estado):
                dx = destino[i][0] - auto.pos.x
                if abs(dx) > 0.01:
                    auto.pos.x += np.clip(dx, -vel_avance * dt, vel_avance * dt)
            auto.pos.z = 0
            auto.color = color.red
            if abs(auto.pos.x - destino[i][0]) < 0.08:
                estado[i] = "en_bifurcacion"
                z_destino = RAMAL_DESVIO / 2 if servidor_de_auto[i] == 0 else -RAMAL_DESVIO / 2
                destino[i] = (POS_RAMAL_X, z_destino)


        # Estado: en bifurcación (comienza desvío)
        elif estado[i] == "en_bifurcacion":
            dz = destino[i][1] - auto.pos.z
            if abs(dz) > 0.01:
                auto.pos.z += np.clip(dz, -vel_desvio * dt, vel_desvio * dt)
            dx = destino[i][0] - auto.pos.x
            if abs(dx) > 0.01:
                auto.pos.x += np.clip(dx, -vel_avance * dt * 0.5, vel_avance * dt * 0.5)
            auto.color = color.red
            if abs(auto.pos.z - destino[i][1]) < 0.05:
                estado[i] = "en_ramal"
                destino[i] = (servidor_pos[servidor_de_auto[i]].x - 0.5, servidor_pos[servidor_de_auto[i]].z)


        # Estado: en ramal (avanzando hacia servidor)
        elif estado[i] == "en_ramal":
            if hay_espacio_adelante(i, autos, estado):
                dx = destino[i][0] - auto.pos.x
                if abs(dx) > 0.01:
                    auto.pos.x += np.clip(dx, -vel_avance * dt, vel_avance * dt)
            auto.pos.z = servidor_pos[servidor_de_auto[i]].z
            auto.color = color.red
            if abs(auto.pos.x - destino[i][0]) < 0.08:
                estado[i] = "atendiendo"
                destino[i] = (servidor_pos[servidor_de_auto[i]].x, servidor_pos[servidor_de_auto[i]].z)
                tiempo_llegada_servidor[i] = t  # NUEVO: registrar cuando llega al servidor


        # Estado: atendiendo (en el servidor) - PERMANECE QUIETO
        elif estado[i] == "atendiendo":
            auto.pos.x = servidor_pos[servidor_de_auto[i]].x
            auto.pos.z = servidor_pos[servidor_de_auto[i]].z
            auto.color = color.yellow
            # El cambio a "saliendo" ahora lo maneja el bloque de liberación de servidores


        # Estado: saliendo (abandonando el sistema)
        elif estado[i] == "saliendo":
            dx = destino[i][0] - auto.pos.x
            if abs(dx) > 0.01:
                auto.pos.x += np.clip(dx, -vel_salida * dt, vel_salida * dt)
            auto.pos.z = servidor_pos[servidor_de_auto[i]].z
            auto.color = color.red
            if auto.pos.x >= POS_SALIDA_X:
                auto.visible = False


    rate(int(1 / dt))
    t += dt


while True:
    rate(10)
