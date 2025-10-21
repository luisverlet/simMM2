import simpy
import numpy as np
from parametros import LAMBDA, MU, SERVIDORES

class EventoAuto:
    def __init__(self, id, tiempo_llegada):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_inicio_servicio = None
        self.tiempo_salida = None

def llegada_autos(env, sistema, eventos, duracion):
    id_auto = 0
    while env.now < duracion:
        id_auto += 1
        evento = EventoAuto(id=id_auto, tiempo_llegada=env.now)
        eventos.append(evento)
        env.process(servicio_auto(env, sistema, evento))
        intervalo = np.random.exponential(60 / LAMBDA)
        yield env.timeout(intervalo)

def servicio_auto(env, sistema, evento):
    with sistema.request() as req:
        yield req
        evento.tiempo_inicio_servicio = env.now
        # TIEMPO DE SERVICIO EXPONENCIAL, pero limitado entre 1 y 20 segundos
        tiempo_servicio = np.clip(np.random.exponential(60 / MU), 1.0, 20.0)
        yield env.timeout(tiempo_servicio)
        evento.tiempo_salida = env.now

def simular_mm2(duracion=60):
    env = simpy.Environment()
    sistema = simpy.Resource(env, capacity=SERVIDORES)
    eventos = []
    env.process(llegada_autos(env, sistema, eventos, duracion))
    env.run(until=duracion)
    return eventos

if __name__ == '__main__':
    registros = simular_mm2(120)
    print("Autos simulados:", len(registros))
    for e in registros[:5]:
        print(vars(e))
