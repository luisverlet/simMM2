import numpy as np
from vpython import box, label, color, canvas, vector, rate, cylinder, sphere, compound
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


def crear_carro(pos, col):
    """Crea un modelo 3D de carro"""
    partes = []
    partes.append(box(pos=vector(0, 0.06, 0), size=vector(0.6, 0.25, 0.35), color=col))
    partes.append(box(pos=vector(0, 0.26, 0), size=vector(0.35, 0.2, 0.3), color=col))
    partes.append(cylinder(pos=vector(-0.2, -0.10, -0.2), axis=vector(0, 0, 0.05), radius=0.10, color=color.black))
    partes.append(cylinder(pos=vector(0.2, -0.10, -0.2), axis=vector(0, 0, 0.05), radius=0.10, color=color.black))
    partes.append(cylinder(pos=vector(-0.2, -0.10, 0.15), axis=vector(0, 0, 0.05), radius=0.10, color=color.black))
    partes.append(cylinder(pos=vector(0.2, -0.10, 0.15), axis=vector(0, 0, 0.05), radius=0.10, color=color.black))
    return compound(partes, pos=pos)


def crear_guardia(pos):
    """Crea modelo 3D de guardia"""
    partes = []
    partes.append(cylinder(pos=vector(0, 0, 0), axis=vector(0, 0.45, 0), radius=0.18, color=vector(0.2, 0.3, 0.6)))
    partes.append(sphere(pos=vector(0, 0.6, 0), radius=0.15, color=vector(0.9, 0.75, 0.6)))
    partes.append(cylinder(pos=vector(0, 0.68, 0), axis=vector(0, 0.1, 0), radius=0.16, color=vector(0.1, 0.15, 0.3)))
    partes.append(box(pos=vector(0, 0.73, 0.08), size=vector(0.25, 0.02, 0.12), color=vector(0.1, 0.15, 0.3)))
    return compound(partes, pos=pos)


def crear_bandera_venezuela(pos):
    """Crea bandera de Venezuela"""
    partes = []
    partes.append(cylinder(pos=vector(0, 0, 0), axis=vector(0, 1.2, 0), radius=0.025, color=vector(0.5, 0.5, 0.5)))
    partes.append(sphere(pos=vector(0, 1.2, 0), radius=0.05, color=vector(0.8, 0.7, 0.2)))
    partes.append(box(pos=vector(0.35, 1.0, 0), size=vector(0.7, 0.18, 0.02), color=vector(1, 0.85, 0)))
    partes.append(box(pos=vector(0.35, 0.82, 0), size=vector(0.7, 0.18, 0.02), color=vector(0, 0.2, 0.65)))
    for i in range(8):
        x_offset = 0.05 + i * 0.08
        partes.append(sphere(pos=vector(x_offset, 0.82, 0.02), radius=0.015, color=color.white))
    partes.append(box(pos=vector(0.35, 0.64, 0), size=vector(0.7, 0.18, 0.02), color=vector(0.85, 0.1, 0.15)))
    return compound(partes, pos=pos)


def crear_garita_lateral(pos):
    """Crea garita"""
    partes = []
    partes.append(box(pos=vector(0, 0, 0), size=vector(1.2, 0.08, 1.2), color=vector(0.65, 0.65, 0.65)))
    altura_pared = 1.2
    centro_pared = altura_pared / 2 + 0.04
    partes.append(box(pos=vector(0, centro_pared, 0), size=vector(0.08, altura_pared, 1.2), color=vector(0.88, 0.88, 0.92)))
    partes.append(box(pos=vector(0.56, centro_pared, 0), size=vector(0.08, altura_pared, 1.2), color=vector(0.88, 0.88, 0.92)))
    partes.append(box(pos=vector(0.28, centro_pared, -0.56), size=vector(1.2, altura_pared, 0.08), color=vector(0.88, 0.88, 0.92)))
    partes.append(box(pos=vector(0.28, centro_pared, 0.56), size=vector(1.2, altura_pared, 0.08), color=vector(0.88, 0.88, 0.92)))
    partes.append(box(pos=vector(0.28, 1.29, 0), size=vector(1.35, 0.12, 1.35), color=vector(0.55, 0.3, 0.2)))
    partes.append(box(pos=vector(-0.2, 0.5, 0), size=vector(0.35, 0.9, 0.45), color=vector(0.4, 0.3, 0.2)))
    return compound(partes, pos=pos)


def crear_edificio(pos, ancho, alto, profundo):
    """Crea edificio"""
    partes = []
    partes.append(box(pos=vector(0, alto/2, 0), size=vector(ancho, alto, profundo), color=vector(0.75, 0.75, 0.78)))
    for i in range(3):
        for j in range(int(alto / 0.8)):
            partes.append(box(pos=vector(-ancho/3 + i*ancho/3, 0.3 + j*0.8, profundo/2 + 0.02), 
                            size=vector(0.25, 0.35, 0.02), color=vector(0.4, 0.6, 0.8)))
    partes.append(box(pos=vector(0, alto + 0.1, 0), size=vector(ancho + 0.2, 0.2, profundo + 0.2), color=vector(0.6, 0.6, 0.65)))
    return compound(partes, pos=pos)


resultados = mm2_statistics(LAMBDA, MU, SERVIDORES)

if resultados['ro'] >= 1.0:
    scene = canvas(title="Simulación MM2 - Control Vehicular", width=1920, height=1080)
    scene.background = vector(0.15, 0.25, 0.15)
    err_label = label(pos=vector(0, 0, 0), text="¡ERROR!\nLa utilización (ρ) es mayor o igual a 1.\nNo es posible simular: revisa los parámetros.", height=34, color=color.red, box=True, opacity=0.85)
    while True:
        rate(10)

N = max(1, int(round(resultados['L'])))
resultados_label_text = (
    f"Control Vehicular - Puente Simón Bolívar\n"
    f"λ: {LAMBDA:.2f} veh/min  μ: {MU:.2f} veh/min/servidor  S: {SERVIDORES}\n"
    f"Utilización ρ: {resultados['ro']:.3f} ({100*resultados['ro']:.1f}%)  Servicio: {60/MU:.1f}s\n"
    f"Lq (cola): {resultados['Lq']:.2f}  L (sistema): {resultados['L']:.2f}\n"
    f"Wq (espera): {resultados['Wq']*60:.1f}s  W (total): {resultados['W']*60:.1f}s"
)

scene = canvas(title="Simulación MM2 - Control Vehicular", width=1920, height=1080)
scene.background = vector(0.25, 0.35, 0.25)
scene.range = 12
scene.center = vector(2, 0, 0)

ALTURA_CARRETERA = -0.55     # Altura de la carretera
ALTURA_CARROS = -0.25        # Altura de los vehículos
ALTURA_GARITAS = 0             # Altura de las garitas y edificios

CARRIL_LARGO = 8
POS_ENTRADA_X = -4
POS_RAMAL_X = 3.0
RAMAL_LARGO = 3.5
RAMAL_DESVIO = 1.8
POS_SALIDA_X = POS_RAMAL_X + RAMAL_LARGO + 1.5

# ===== CARRETERA =====
box(pos=vector((POS_ENTRADA_X + POS_RAMAL_X) / 2, ALTURA_CARRETERA, 0), 
    size=vector(POS_RAMAL_X - POS_ENTRADA_X, 0.08, 0.9), 
    color=vector(0.3, 0.3, 0.35))

for x in np.arange(POS_ENTRADA_X, POS_RAMAL_X, 0.5):
    box(pos=vector(x, ALTURA_CARRETERA + 0.05, 0), size=vector(0.3, 0.01, 0.08), color=color.white)

box(pos=vector(POS_RAMAL_X + RAMAL_LARGO / 2, ALTURA_CARRETERA, RAMAL_DESVIO / 2), 
    size=vector(RAMAL_LARGO, 0.08, 0.9), 
    color=vector(0.3, 0.3, 0.35))
box(pos=vector(POS_RAMAL_X + RAMAL_LARGO / 2, ALTURA_CARRETERA, -RAMAL_DESVIO / 2), 
    size=vector(RAMAL_LARGO, 0.08, 0.9), 
    color=vector(0.3, 0.3, 0.35))

box(pos=vector(POS_RAMAL_X, ALTURA_CARRETERA, 0), size=vector(0.4, 0.08, RAMAL_DESVIO + 0.6), color=vector(0.3, 0.3, 0.35))

box(pos=vector(POS_RAMAL_X + RAMAL_LARGO + 0.75, ALTURA_CARRETERA, RAMAL_DESVIO / 2), 
    size=vector(1.5, 0.08, 0.9), color=vector(0.3, 0.3, 0.35))
box(pos=vector(POS_RAMAL_X + RAMAL_LARGO + 0.75, ALTURA_CARRETERA, -RAMAL_DESVIO / 2), 
    size=vector(1.5, 0.08, 0.9), color=vector(0.3, 0.3, 0.35))

# ===== GARITAS (VARIABLE) =====
garita_pos = [
    vector(POS_RAMAL_X + RAMAL_LARGO - 0.5, ALTURA_GARITAS, RAMAL_DESVIO / 2 + 1.2),
    vector(POS_RAMAL_X + RAMAL_LARGO - 0.5, ALTURA_GARITAS, -RAMAL_DESVIO / 2 - 1.2)
]

garitas = [crear_garita_lateral(garita_pos[i]) for i in range(SERVIDORES)]
guardias = [crear_guardia(garita_pos[i] + vector(-0.8, 0, 0)) for i in range(SERVIDORES)]
banderas = [crear_bandera_venezuela(garita_pos[i] + vector(0.5, 1.35, 0)) for i in range(SERVIDORES)]

# ===== EDIFICIOS (VARIABLE) =====
crear_edificio(vector(POS_SALIDA_X + 2, ALTURA_GARITAS, 3), 2.5, 4, 1.5)
crear_edificio(vector(POS_SALIDA_X + 2, ALTURA_GARITAS, -3), 2.0, 3.5, 1.2)
crear_edificio(vector(POS_SALIDA_X + 5, ALTURA_GARITAS, 2), 1.8, 5, 1.3)
crear_edificio(vector(POS_SALIDA_X + 5, ALTURA_GARITAS, -4), 2.2, 4.5, 1.4)

srv_labels = [label(pos=garita_pos[i] + vector(0, 2.0, 0), text="LIBRE", height=16, 
                    color=color.white, box=False, opacity=0.85) for i in range(SERVIDORES)]

label(pos=vector(POS_ENTRADA_X - 1, 3.5, 0), text=resultados_label_text, height=13, 
      box=True, color=color.white, background=vector(0.15, 0.2, 0.25), border=6, opacity=0.9)

eventos_pool = simular_mm2(max(80, 5 * N))
eventos_pool = eventos_pool[:N]

autos, estado, servidor_de_auto, tiempo_llegada_servidor, duracion_servicio, orden_llegada, angulo_auto = [], [], [], [], [], [], []
DISTANCIA_ENTRE_BOLAS = 0.7
contador_orden = 0

colores_carros = [vector(0.8, 0.1, 0.1), vector(0.1, 0.2, 0.8), vector(0.9, 0.9, 0.1), 
                  vector(0.2, 0.7, 0.3), vector(0.9, 0.4, 0.1), vector(0.7, 0.7, 0.7),
                  vector(0.6, 0.1, 0.6), vector(0.1, 0.6, 0.6)]

for i in range(N):
    col = colores_carros[i % len(colores_carros)]
    # ===== CARROS (VARIABLE) =====
    c = crear_carro(vector(POS_ENTRADA_X - i * DISTANCIA_ENTRE_BOLAS, ALTURA_CARROS, 0), col)
    autos.append(c)
    estado.append("cola")
    servidor_de_auto.append(None)
    tiempo_llegada_servidor.append(None)
    duracion_servicio.append(np.clip(np.random.exponential(60 / MU), 2.0, 20.0))
    orden_llegada.append(contador_orden)
    angulo_auto.append(0)
    contador_orden += 1

servidores_ocupados = [None, None]
servidores_bloqueados = [False, False]

dt = 0.03
t = 0
vel_cola = 0.7
vel_avance = 1.2
vel_desvio = 1.0
vel_salida = 1.4

while True:
    for s in range(SERVIDORES):
        idx = servidores_ocupados[s]
        if idx is not None and estado[idx] == "atendiendo":
            srv_labels[s].text = "REVISANDO"
            srv_labels[s].color = color.yellow
        else:
            srv_labels[s].text = "LIBRE"
            srv_labels[s].color = color.green

    for s in range(SERVIDORES):
        idx = servidores_ocupados[s]
        if idx is not None:
            if tiempo_llegada_servidor[idx] is not None and duracion_servicio[idx] is not None:
                tiempo_en_servidor = t - tiempo_llegada_servidor[idx]
                if tiempo_en_servidor >= duracion_servicio[idx] and estado[idx] == "atendiendo":
                    estado[idx] = "saliendo"
                    servidores_ocupados[s] = None
                    servidores_bloqueados[s] = False

    cola_ordenada = []
    for i in range(N):
        if autos[i].visible and estado[i] == "cola":
            cola_ordenada.append((i, autos[i].pos.x, orden_llegada[i]))
    cola_ordenada.sort(key=lambda x: x[2])

    for i in range(N):
        if not autos[i].visible:
            continue
        auto = autos[i]

        if estado[i] == "cola":
            if len(cola_ordenada) > 0 and cola_ordenada[0][0] == i:
                servidor_asignado = None
                for s in range(SERVIDORES):
                    if servidores_ocupados[s] is None and not servidores_bloqueados[s]:
                        servidor_asignado = s
                        servidores_ocupados[s] = i
                        servidores_bloqueados[s] = True
                        break
                if servidor_asignado is not None:
                    estado[i] = "avanzando_a_bifurcacion"
                    servidor_de_auto[i] = servidor_asignado
            
            mi_indice_en_cola = None
            for idx, (veh_id, _, _) in enumerate(cola_ordenada):
                if veh_id == i:
                    mi_indice_en_cola = idx
                    break
            
            if mi_indice_en_cola is not None:
                pos_x_objetivo = POS_RAMAL_X - 0.6 - mi_indice_en_cola * DISTANCIA_ENTRE_BOLAS
                
                if pos_x_objetivo > auto.pos.x + 0.01:
                    puede_avanzar = True
                    if mi_indice_en_cola > 0:
                        delante_id, delante_x, _ = cola_ordenada[mi_indice_en_cola - 1]
                        if autos[delante_id].pos.x - auto.pos.x < DISTANCIA_ENTRE_BOLAS * 0.8:
                            puede_avanzar = False
                    
                    if puede_avanzar:
                        auto.pos.x += vel_cola * dt
            
            auto.pos.y = ALTURA_CARROS
            auto.pos.z = 0
            angulo_auto[i] = 0

        elif estado[i] == "avanzando_a_bifurcacion":
            dx = POS_RAMAL_X - auto.pos.x
            if abs(dx) > 0.01:
                auto.pos.x += np.clip(dx, -vel_avance * dt, vel_avance * dt)
            auto.pos.z = 0
            auto.pos.y = ALTURA_CARROS
            angulo_auto[i] = 0
            if abs(auto.pos.x - POS_RAMAL_X) < 0.08:
                estado[i] = "desviando_a_ramal"

        elif estado[i] == "desviando_a_ramal":
            z_destino = RAMAL_DESVIO / 2 if servidor_de_auto[i] == 0 else -RAMAL_DESVIO / 2
            dx = (POS_RAMAL_X + 0.5) - auto.pos.x
            if abs(dx) > 0.01:
                auto.pos.x += np.clip(dx, -vel_desvio * dt * 0.5, vel_desvio * dt * 0.5)
            dz = z_destino - auto.pos.z
            if abs(dz) > 0.01:
                auto.pos.z += np.clip(dz, -vel_desvio * dt, vel_desvio * dt)
            auto.pos.y = ALTURA_CARROS
            
            if servidor_de_auto[i] == 0:
                angulo_auto[i] = math.radians(25)
            else:
                angulo_auto[i] = math.radians(-25)
            
            if abs(auto.pos.z - z_destino) < 0.08:
                estado[i] = "en_ramal"

        elif estado[i] == "en_ramal":
            destino_x = POS_RAMAL_X + RAMAL_LARGO - 0.5
            dx = destino_x - auto.pos.x
            if abs(dx) > 0.01:
                auto.pos.x += np.clip(dx, -vel_avance * dt, vel_avance * dt)
            auto.pos.z = RAMAL_DESVIO / 2 if servidor_de_auto[i] == 0 else -RAMAL_DESVIO / 2
            auto.pos.y = ALTURA_CARROS
            angulo_auto[i] = 0
            if abs(auto.pos.x - destino_x) < 0.08:
                estado[i] = "atendiendo"
                tiempo_llegada_servidor[i] = t

        elif estado[i] == "atendiendo":
            auto.pos.x = POS_RAMAL_X + RAMAL_LARGO - 0.5
            auto.pos.z = RAMAL_DESVIO / 2 if servidor_de_auto[i] == 0 else -RAMAL_DESVIO / 2
            auto.pos.y = ALTURA_CARROS
            angulo_auto[i] = 0

        elif estado[i] == "saliendo":
            dx = POS_SALIDA_X - auto.pos.x
            if abs(dx) > 0.01:
                auto.pos.x += np.clip(dx, -vel_salida * dt, vel_salida * dt)
            auto.pos.z = RAMAL_DESVIO / 2 if servidor_de_auto[i] == 0 else -RAMAL_DESVIO / 2
            auto.pos.y = ALTURA_CARROS
            angulo_auto[i] = 0
            if auto.pos.x >= POS_SALIDA_X:
                pos_mas_atras = POS_ENTRADA_X
                for j in range(N):
                    if estado[j] == "cola" and autos[j].visible:
                        if autos[j].pos.x < pos_mas_atras:
                            pos_mas_atras = autos[j].pos.x
                
                auto.pos = vector(pos_mas_atras - DISTANCIA_ENTRE_BOLAS * 2, ALTURA_CARROS, 0)
                auto.visible = True
                estado[i] = "cola"
                servidor_de_auto[i] = None
                tiempo_llegada_servidor[i] = None
                duracion_servicio[i] = np.clip(np.random.exponential(60 / MU), 2.0, 20.0)
                orden_llegada[i] = contador_orden
                angulo_auto[i] = 0
                contador_orden += 1
        
        auto.rotate(angle=angulo_auto[i] - auto.rotate_angle if hasattr(auto, 'rotate_angle') else angulo_auto[i], 
                   axis=vector(0, 1, 0), origin=auto.pos)
        auto.rotate_angle = angulo_auto[i]

    rate(int(1 / dt))
    t += dt
