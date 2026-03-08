"""
Anymap TS del Parque Norte de Madrid
Visualización de datos del parque usando técnicas de series temporales
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import folium
from folium.plugins import HeatMap
import json

class ParqueNorteMadrid:
    """Clase principal para el análisis del Parque Norte de Madrid"""
    
    def __init__(self):
        self.nombre = "Parque Norte de Madrid"
        self.coordenadas = [40.4740, -3.6147]  # Coordenadas aproximadas
        self.datos_simulados = None
        
    def generar_datos_simulados(self, dias=365):
        """Genera datos simulados de visitantes y actividades"""
        fechas = pd.date_range(end=datetime.now(), periods=dias, freq='D')
        
        datos = {
            'fecha': fechas,
            'visitantes': np.random.poisson(500, dias) + 
                         np.sin(np.arange(dias) * 2 * np.pi / 365) * 200 +
                         np.where(fechas.weekday < 5, 100, 300),  # Más visitantes los fines de semana
            'temperatura': 10 + 15 * np.sin(np.arange(dias) * 2 * np.pi / 365) + 
                          np.random.normal(0, 5, dias),
            'actividades': np.random.choice(['Caminata', 'Ciclismo', 'Picnic', 'Deporte', 'Observación'], 
                                           dias, p=[0.3, 0.25, 0.2, 0.15, 0.1])
        }
        
        self.datos_simulados = pd.DataFrame(datos)
        return self.datos_simulados
    
    def crear_mapa_interactivo(self):
        """Crea un mapa interactivo del Parque Norte"""
        mapa = folium.Map(location=self.coordenadas, zoom_start=15)
        
        # Añadir marcador del parque
        folium.Marker(
            self.coordenadas,
            popup=f'<b>{self.nombre}</b><br>Área recreativa principal',
            tooltip='Haz clic para más información',
            icon=folium.Icon(color='green', icon='tree-conifer')
        ).add_to(mapa)
        
        # Añadir puntos de interés alrededor del parque
        puntos_interes = [
            [[40.4755, -3.6160], "Entrada Principal"],
            [[40.4730, -3.6130], "Área de Picnic"],
            [[40.4720, -3.6155], "Zona Deportiva"],
            [[40.4760, -3.6120], "Mirador"]
        ]
        
        for coord, nombre in puntos_interes:
            folium.Marker(
                coord,
                popup=f'<b>{nombre}</b>',
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
        
        # Añadir polígono del área del parque (aproximado)
        area_parque = [
            [40.4750, -3.6170],
            [40.4765, -3.6125],
            [40.4715, -3.6115],
            [40.4705, -3.6165],
            [40.4750, -3.6170]
        ]
        
        folium.Polygon(
            area_parque,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.2,
            popup='Área aproximada del Parque Norte'
        ).add_to(mapa)
        
        return mapa
    
    def analizar_series_temporales(self):
        """Realiza análisis de series temporales de los datos"""
        if self.datos_simulados is None:
            self.generar_datos_simulados()
        
        datos = self.datos_simulados.copy()
        datos.set_index('fecha', inplace=True)
        
        # Análisis mensual
        datos_mensual = datos.resample('M').agg({
            'visitantes': 'sum',
            'temperatura': 'mean'
        })
        
        return datos_mensual
    
    def generar_visualizaciones(self):
        """Genera visualizaciones de los datos"""
        if self.datos_simulados is None:
            self.generar_datos_simulados()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Gráfico 1: Visitantes diarios
        axes[0, 0].plot(self.datos_simulados['fecha'], self.datos_simulados['visitantes'])
        axes[0, 0].set_title('Visitantes Diarios - Parque Norte de Madrid')
        axes[0, 0].set_xlabel('Fecha')
        axes[0, 0].set_ylabel('Número de Visitantes')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Temperatura media
        axes[0, 1].plot(self.datos_simulados['fecha'], self.datos_simulados['temperatura'], color='red')
        axes[0, 1].set_title('Temperatura Media Diaria')
        axes[0, 1].set_xlabel('Fecha')
        axes[0, 1].set_ylabel('Temperatura (°C)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico 3: Distribución de actividades
        actividades_counts = self.datos_simulados['actividades'].value_counts()
        axes[1, 0].bar(actividades_counts.index, actividades_counts.values)
        axes[1, 0].set_title('Distribución de Actividades')
        axes[1, 0].set_xlabel('Actividad')
        axes[1, 0].set_ylabel('Frecuencia')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Gráfico 4: Visitantes por día de la semana
        self.datos_simulados['dia_semana'] = self.datos_simulados['fecha'].dt.day_name()
        visitantes_por_dia = self.datos_simulados.groupby('dia_semana')['visitantes'].mean()
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        visitantes_por_dia = visitantes_por_dia.reindex(dias_orden)
        axes[1, 1].bar(visitantes_por_dia.index, visitantes_por_dia.values)
        axes[1, 1].set_title('Visitantes Promedio por Día de la Semana')
        axes[1, 1].set_xlabel('Día de la Semana')
        axes[1, 1].set_ylabel('Visitantes Promedio')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig

def main():
    """Función principal"""
    print("=== Anymap TS - Parque Norte de Madrid ===\n")
    
    # Crear instancia del análisis
    parque = ParqueNorteMadrid()
    
    # Generar datos
    print("Generando datos simulados...")
    datos = parque.generar_datos_simulados()
    print(f"Datos generados: {len(datos)} registros")
    print(f"Período: {datos['fecha'].min().date()} a {datos['fecha'].max().date()}")
    
    # Análisis de series temporales
    print("\nRealizando análisis de series temporales...")
    analisis_mensual = parque.analizar_series_temporales()
    print("\nResumen mensual:")
    print(analisis_mensual.tail())
    
    # Crear visualizaciones
    print("\nGenerando visualizaciones...")
    fig = parque.generar_visualizaciones()
    fig.savefig('visualizaciones_parque_norte.png', dpi=300, bbox_inches='tight')
    print("Visualizaciones guardadas en 'visualizaciones_parque_norte.png'")
    
    # Crear mapa interactivo
    print("\nCreando mapa interactivo...")
    mapa = parque.crear_mapa_interactivo()
    mapa.save('mapa_parque_norte.html')
    print("Mapa interactivo guardado en 'mapa_parque_norte.html'")
    
    # Generar reporte
    with open('reporte_parque_norte.txt', 'w') as f:
        f.write(f"REPORTE: {parque.nombre}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total de registros: {len(datos)}\n")
        f.write(f"Visitantes totales simulados: {datos['visitantes'].sum():,.0f}\n")
        f.write(f"Temperatura promedio: {datos['temperatura'].mean():.1f}°C\n")
        f.write(f"Actividad más popular: {datos['actividades'].mode()[0]}\n\n")
        
        f.write("Resumen mensual:\n")
        f.write(str(analisis_mensual.tail()))
    
    print("\n=== Análisis completado ===")
    print("Archivos generados:")
    print("1. visualizaciones_parque_norte.png - Gráficos de análisis")
    print("2. mapa_parque_norte.html - Mapa interactivo")
    print("3. reporte_parque_norte.txt - Reporte de análisis")

if __name__ == "__main__":
    main()