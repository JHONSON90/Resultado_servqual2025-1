import pandas as pd
from geopy.geocoders import Nominatim
import time

# Configurar el geocodificador
geolocator = Nominatim(user_agent="pasto_barrios_app")

# Lista de barrios
barrios = [
    'Ocho de Marzo, Pasto, Nariño, Colombia',
    'Agualongo, Pasto, Nariño, Colombia',
    'Aire Libre, Pasto, Nariño, Colombia',
    'Altos de la Colina, Pasto, Nariño, Colombia',
    'Altos del Campo, Pasto, Nariño, Colombia',
    'Aquine, Pasto, Nariño, Colombia',
    'Aquine I, Pasto, Nariño, Colombia',
    'Aquine II, Pasto, Nariño, Colombia',
    'Atahualpa, Pasto, Nariño, Colombia',
    'La Aurora, Pasto, Nariño, Colombia',
    'Av. Boyaca , Pasto, Nariño, Colombia',
    'Av. Idema, Pasto, Nariño, Colombia',
    'Av. Colombia, Pasto, Nariño, Colombia',
    'Bachue, Pasto, Nariño, Colombia',
    'Bella Vista, Pasto, Nariño, Colombia',
    'Bombona , Pasto, Nariño, Colombia',
    'San Ignacio, Pasto, Nariño, Colombia',
    'Caicedo, Pasto, Nariño, Colombia',
    'Caicedo alto, Pasto, Nariño, Colombia',
    'Caicedo Bajo, Pasto, Nariño, Colombia',
    'Cantarana, Pasto, Nariño, Colombia',
    'Caracha, Pasto, Nariño, Colombia',
    'Carlos Pizarro, Pasto, Nariño, Colombia',
    'La Carolina, Pasto, Nariño, Colombia',
    'Castellana, Pasto, Nariño, Colombia',
    'Cementerio, Pasto, Nariño, Colombia',
    'Chambu , Pasto, Nariño, Colombia',
    'Chambu I, Pasto, Nariño, Colombia',
    'Chambu II, Pasto, Nariño, Colombia',
    'Chapal, Pasto, Nariño, Colombia',
    'Chile, Pasto, Nariño, Colombia',
    'Condominio Mirador de Aquine Apto 206, Pasto, Nariño, Colombia',
    'Corazon de Jesus, Pasto, Nariño, Colombia',
    'El Lorenzo, Pasto, Nariño, Colombia',
    'El Pilar, Pasto, Nariño, Colombia',
    'El Recuerdo, Pasto, Nariño, Colombia',
    'El Tejar, Pasto, Nariño, Colombia',
    'Esmeralda, Pasto, Nariño, Colombia',
    'Fatima, Pasto, Nariño, Colombia',
    'Floresta, Pasto, Nariño, Colombia',
    'Granada, Pasto, Nariño, Colombia',
    'Gualcaloma, Pasto, Nariño, Colombia',
    'Juanoy, Pasto, Nariño, Colombia',
    'Julian Bucheli, Pasto, Nariño, Colombia',
    'La Colina, Pasto, Nariño, Colombia',
    'La Cruz, Pasto, Nariño, Colombia',
    'La Esmeralda, Pasto, Nariño, Colombia',
    'La Floresta, Pasto, Nariño, Colombia',
    'La Lomita, Pasto, Nariño, Colombia',
    'La Minga, Pasto, Nariño, Colombia',
    'Las Americas , Pasto, Nariño, Colombia',
    'Las Cuadras, Pasto, Nariño, Colombia',
    'Las Mercedes, Pasto, Nariño, Colombia',
    'Libertad, Pasto, Nariño, Colombia',
    'Lorenzo, Pasto, Nariño, Colombia',
    'Los Laureles, Pasto, Nariño, Colombia',
    'Los Rosales Anganoy, Pasto, Nariño, Colombia',
    'Manantial, Pasto, Nariño, Colombia',
    'Maria Isabel, Pasto, Nariño, Colombia',
    'Maridiaz, Pasto, Nariño, Colombia',
    'Mariluz, Pasto, Nariño, Colombia',
    'Mariluz II, Pasto, Nariño, Colombia',
    'Mariluz 3, Pasto, Nariño, Colombia',
    'Mercedario, Pasto, Nariño, Colombia',
    'Mijitayo, Pasto, Nariño, Colombia',
    'Miraflores, Pasto, Nariño, Colombia',
    'Morasurco, Pasto, Nariño, Colombia',
    'Niza, Pasto, Nariño, Colombia',
    'Niza II, Pasto, Nariño, Colombia',
    'Nueva Granada, Pasto, Nariño, Colombia',
    'Nuevo Sol, Pasto, Nariño, Colombia',
    'Panamericano, Pasto, Nariño, Colombia',
    'Pandiaco, Pasto, Nariño, Colombia',
    'Panoramico, Pasto, Nariño, Colombia',
    'Panoramico 1 et, Pasto, Nariño, Colombia',
    'Panoramico 2 et, Pasto, Nariño, Colombia',
    'Pilar, Pasto, Nariño, Colombia',
    'Altos del campo, Pasto, Nariño, Colombia',
    'Pucalpa II, Pasto, Nariño, Colombia',
    'Quillasinga, Pasto, Nariño, Colombia',
    'Quintas de San Pedro, Pasto, Nariño, Colombia',
    'Quito Lopez, Pasto, Nariño, Colombia',
    'Quito Lopez 3, Pasto, Nariño, Colombia',
    'San Andres, Pasto, Nariño, Colombia',
    'San Diego, Pasto, Nariño, Colombia',
    'San Diego Norte, Pasto, Nariño, Colombia',
    'San Juan de Dios, Pasto, Nariño, Colombia',
    'San Miguel, Pasto, Nariño, Colombia',
    'San Vicente, Pasto, Nariño, Colombia',
    'Santa Barbara, Pasto, Nariño, Colombia',
    'Santa Monica, Pasto, Nariño, Colombia',
    'Sendoya, Pasto, Nariño, Colombia',
    'Tamasagra, Pasto, Nariño, Colombia',
    'Tamasagra 1 etapa, Pasto, Nariño, Colombia',
    'Venecia, Pasto, Nariño, Colombia',
    'Versalles, Pasto, Nariño, Colombia',
    'Palermo, Pasto, Nariño, Colombia',
    'Villa Docente, Pasto, Nariño, Colombia',
    'Villa Flor, Pasto, Nariño, Colombia',
    'Villa Olímpica, Pasto, Nariño, Colombia',
    'Villa Recreo, Pasto, Nariño, Colombia',
    'Villa Vergel, Pasto, Nariño, Colombia',
    'Villaflor, Pasto, Nariño, Colombia',
    'Villaflor 2, Pasto, Nariño, Colombia',
    'Zarama, Pasto, Nariño, Colombia',
    'San Miguel de Obonuco, Pasto, Nariño, Colombia',
    'Nuevo Horizonte, Pasto, Nariño, Colombia'
]

def geocodificar_barrios(lista_barrios):
    resultados = []
    
    for barrio in lista_barrios:
        try:
            print(f"Buscando: {barrio}")
            location = geolocator.geocode(barrio)
            
            if location:
                resultados.append({
                    'Barrio': barrio.split(',')[0],
                    'Latitud': location.latitude,
                    'Longitud': location.longitude,
                    'Dirección_Completa': location.address
                })
            else:
                resultados.append({
                    'Barrio': barrio.split(',')[0],
                    'Latitud': None,
                    'Longitud': None,
                    'Dirección_Completa': 'No encontrado'
                })
            
            # Pausa para ser respetuoso con el servicio
            time.sleep(1)
            
        except Exception as e:
            print(f"Error con {barrio}: {e}")
            resultados.append({
                'Barrio': barrio.split(',')[0],
                'Latitud': None,
                'Longitud': None,
                'Dirección_Completa': f'Error: {e}'
            })
    
    return pd.DataFrame(resultados)

# Ejecutar la geocodificación
df_coordenadas = geocodificar_barrios(barrios)

# Guardar resultados
df_coordenadas.to_csv('coordenadas_barrios_pasto.csv', index=False)
print("Geocodificación completada. Resultados guardados en CSV.")