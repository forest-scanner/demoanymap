#!/usr/bin/env python3
"""
Análisis de series temporales y visualización geoespacial del Parque Norte de Madrid.
Implementación de Anymap TS para análisis de datos de visitantes y actividades.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta
import seaborn as sns
from typing import Dict, List, Tuple
import json


class ParqueNorteMadrid:
    """Clase principal para el análisis del Parque Norte de Madrid."""
    
    def __init__(self):
        """Inicializa el análisis del Parque Norte de Madrid."""
        self.nombre = "Parque Norte de Madrid"
        self.coordenadas = (40.4740, -3.6867)  # Coordenadas aproximadas
        self.puntos_interes = {
            "Entrada Principal": (40.4745, -3.6870),
            "Lago": (40.4735, -3.6855),
            "Zona Infantil": (40.4748, -3.6860),
            "Área Deportiva": (40.4730, -3.6880),
            "Jardín Botánico": (40.4750, -3.6845),
        }
        self.actividades = ["Caminar", "Correr", "Ciclismo", "Picnic", "Juegos", "Observación"]
        
    def generar_datos_simulados(self, dias: int = 365) -> pd.DataFrame:
        """
        Genera datos simulados de visitantes del parque.
        
        Args:
            dias: Número de días a simular
            
        Returns:
            DataFrame con datos simulados
        """
        fecha_inicio = datetime(2024, 1, 1)
        fechas = [fecha_inicio + timedelta(days=i) for i in range(dias)]
        
        # Generar datos con patrones estacionales
        np.random.seed(42)  # Para reproducibilidad
        
        # Visitantes con patrones estacionales
        base_visitantes = 500
        estacionalidad = 300 * np.sin(2 * np.pi * np.arange(dias) / 365)
        fin_de_semana = np.array([100 if (fecha.weekday() >= 5) else 0 for fecha in fechas])
        ruido = np.random.normal(0, 50, dias)
        visitantes = base_visitantes + estacionalidad + fin_de_semana + ruido
        visitantes = np.maximum(visitantes, 100)  # Mínimo 100 visitantes
        
        # Temperatura con estacionalidad
        temperatura_base = 15
        temp_estacional = 10 * np.sin(2 * np.pi * np.arange(dias) / 365 - np.pi/2)
        temp_ruido = np.random.normal(0, 3, dias)
        temperatura = temperatura_base + temp_estacional + temp_ruido
        
        # Actividades (distribución probabilística)
        actividades_probs = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]  # Probabilidades
        actividades = np.random.choice(self.actividades, dias, p=actividades_probs)
        
        # Crear DataFrame
        datos = pd.DataFrame({
            'fecha': fechas,
            'visitantes': visitantes.astype(int),
            'temperatura': temperatura.round(1),
            'actividad_principal': actividades,
            'dia_semana': [fecha.strftime('%A') for fecha in fechas],
            'mes': [fecha.month for fecha in fechas],
            'es_fin_semana': [fecha.weekday() >= 5 for fecha in fechas]
        })
        
        return datos
    
    def analizar_series_temporales(self, datos: pd.DataFrame = None) -> Dict:
        """
        Realiza análisis de series temporales sobre los datos del parque.
        
        Args:
            datos: DataFrame con datos (si es None, genera datos nuevos)
            
        Returns:
            Diccionario con análisis estadístico
        """
        if datos is None:
            datos = self.generar_datos_simulados()
        
        # Análisis básico
        analisis = {
            'total_visitantes': int(datos['visitantes'].sum()),
            'promedio_diario': float(datos['visitantes'].mean()),
            'max_visitantes': int(datos['visitantes'].max()),
            'min_visitantes': int(datos['visitantes'].min()),
            'temperatura_promedio': float(datos['temperatura'].mean()),
        }
        
        # Análisis por mes
        datos_mensual = datos.groupby('mes').agg({
            'visitantes': ['sum', 'mean', 'std'],
            'temperatura': 'mean'
        }).round(2)
        
        # Análisis por día de semana
        datos_semana = datos.groupby('dia_semana').agg({
            'visitantes': 'mean',
            'temperatura': 'mean'
        }).round(2)
        
        # Correlación entre temperatura y visitantes
        correlacion = datos['temperatura'].corr(datos['visitantes'])
        
        analisis.update({
            'datos_mensual': datos_mensual,
            'datos_semana': datos_semana,
            'correlacion_temperatura_visitantes': float(correlacion),
            'actividad_mas_popular': datos['actividad_principal'].mode()[0],
            'distribucion_actividades': datos['actividad_principal'].value_counts().to_dict()
        })
        
        return analisis
    
    def generar_visualizaciones(self, datos: pd.DataFrame = None) -> plt.Figure:
        """
        Genera visualizaciones de los datos del parque.
        
        Args:
            datos: DataFrame con datos (si es None, genera datos nuevos)
            
        Returns:
            Figura de matplotlib con múltiples gráficos
        """
        if datos is None:
            datos = self.generar_datos_simulados(180)  # 6 meses para visualización
        
        # Crear figura con múltiples subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Análisis del {self.nombre}', fontsize=16, fontweight='bold')
        
        # 1. Serie temporal de visitantes
        axes[0, 0].plot(datos['fecha'], datos['visitantes'], color='green', linewidth=2)
        axes[0, 0].set_title('Visitantes Diarios', fontweight='bold')
        axes[0, 0].set_xlabel('Fecha')
        axes[0, 0].set_ylabel('Número de Visitantes')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Serie temporal de temperatura
        axes[0, 1].plot(datos['fecha'], datos['temperatura'], color='red', linewidth=2)
        axes[0, 1].set_title('Temperatura Diaria', fontweight='bold')
        axes[0, 1].set_xlabel('Fecha')
        axes[0, 1].set_ylabel('Temperatura (°C)')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Distribución de actividades
        actividad_counts = datos['actividad_principal'].value_counts()
        axes[0, 2].bar(actividad_counts.index, actividad_counts.values, color='skyblue')
        axes[0, 2].set_title('Actividades Principales', fontweight='bold')
        axes[0, 2].set_xlabel('Actividad')
        axes[0, 2].set_ylabel('Frecuencia')
        axes[0, 2].tick_params(axis='x', rotation=45)
        
        # 4. Visitantes por día de la semana
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        visitas_semana = datos.groupby('dia_semana')['visitantes'].mean().reindex(dias_orden)
        axes[1, 0].bar(visitas_semana.index, visitas_semana.values, color='orange')
        axes[1, 0].set_title('Visitantes Promedio por Día', fontweight='bold')
        axes[1, 0].set_xlabel('Día de la Semana')
        axes[1, 0].set_ylabel('Visitantes Promedio')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 5. Histograma de visitantes
        axes[1, 1].hist(datos['visitantes'], bins=30, color='purple', alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('Distribución de Visitantes', fontweight='bold')
        axes[1, 1].set_xlabel('Número de Visitantes')
        axes[1, 1].set_ylabel('Frecuencia')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Scatter plot: temperatura vs visitantes
        axes[1, 2].scatter(datos['temperatura'], datos['visitantes'], 
                          alpha=0.6, color='teal', s=20)
        axes[1, 2].set_title('Temperatura vs Visitantes', fontweight='bold')
        axes[1, 2].set_xlabel('Temperatura (°C)')
        axes[1, 2].set_ylabel('Visitantes')
        axes[1, 2].grid(True, alpha=0.3)
        
        # Ajustar layout
        plt.tight_layout()
        
        return fig
    
    def crear_mapa_interactivo(self) -> folium.Map:
        """
        Crea un mapa interactivo del Parque Norte de Madrid.
        
        Returns:
            Mapa de folium con puntos de interés
        """
        # Crear mapa centrado en el parque
        mapa = folium.Map(
            location=self.coordenadas,
            zoom_start=16,
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        # Añadir marcador principal del parque
        folium.Marker(
            location=self.coordenadas,
            popup=f'<b>{self.nombre}</b><br>Área recreativa principal',
            tooltip=self.nombre,
            icon=folium.Icon(color='green', icon='tree', prefix='fa')
        ).add_to(mapa)
        
        # Añadir puntos de interés
        for nombre, coords in self.puntos_interes.items():
            folium.Marker(
                location=coords,
                popup=f'<b>{nombre}</b><br>Punto de interés',
                tooltip=nombre,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
        
        # Añadir círculo para representar el área del parque
        folium.Circle(
            location=self.coordenadas,
            radius=200,  # Aproximadamente 200 metros
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.2,
            popup='Área aproximada del parque'
        ).add_to(mapa)
        
        # Añadir control de capas
        folium.LayerControl().add_to(mapa)
        
        return mapa
    
    def generar_reporte(self, datos: pd.DataFrame = None) -> str:
        """
        Genera un reporte de análisis en formato texto.
        
        Args:
            datos: DataFrame con datos (si es None, genera datos nuevos)
            
        Returns:
            String con el reporte de análisis
        """
        if datos is None:
            datos = self.generar_datos_simulados()
        
        analisis = self.analizar_series_temporales(datos)
        
        reporte = f"""
        {'='*60}
        REPORTE DE ANÁLISIS - {self.nombre}
        {'='*60}
        
        RESUMEN ESTADÍSTICO:
        {'-'*40}
        • Total de visitantes: {analisis['total_visitantes']:,}
        • Promedio diario: {analisis['promedio_diario']:.0f} visitantes
        • Máximo diario: {analisis['max_visitantes']} visitantes
        • Mínimo diario: {analisis['min_visitantes']} visitantes
        • Temperatura promedio: {analisis['temperatura_promedio']:.1f}°C
        
        ANÁLISIS DE CORRELACIÓN:
        {'-'*40}
        • Correlación temperatura-visitantes: {analisis['correlacion_temperatura_visitantes']:.3f}
        
        ACTIVIDADES MÁS POPULARES:
        {'-'*40}
        • Actividad más frecuente: {analisis['actividad_mas_popular']}
        
        DISTRIBUCIÓN DE ACTIVIDADES:
        {'-'*40}
        """
        
        for actividad, frecuencia in analisis['distribucion_actividades'].items():
            porcentaje = (frecuencia / len(datos)) * 100
            reporte += f"  • {actividad}: {frecuencia} días ({porcentaje:.1f}%)\n"
        
        reporte += f"""
        ANÁLISIS POR DÍA DE LA SEMANA:
        {'-'*40}
        """
        
        for dia, datos_dia in analisis['datos_semana'].iterrows():
            reporte += f"  • {dia}: {datos_dia['visitantes']:.0f} visitantes, {datos_dia['temperatura']:.1f}°C\n"
        
        reporte += f"""
        {'='*60}
        Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        {'='*60}
        """
        
        return reporte


def main():
    """Función principal para ejecutar el análisis completo."""
    print("Iniciando análisis del Parque Norte de Madrid...")
    
    # Crear instancia
    parque = ParqueNorteMadrid()
    print(f"Analizando: {parque.nombre}")
    
    # Generar datos
    print("Generando datos simulados...")
    datos = parque.generar_datos_simulados(dias=365)
    print(f"Datos generados: {len(datos)} días")
    
    # Realizar análisis
    print("Realizando análisis de series temporales...")
    analisis = parque.analizar_series_temporales(datos)
    print(f"Total de visitantes: {analisis['total_visitantes']:,}")
    
    # Generar visualizaciones
    print("Generando visualizaciones...")
    fig = parque.generar_visualizaciones(datos)
    fig.savefig('visualizaciones_parque_norte.png', dpi=300, bbox_inches='tight')
    print("Visualizaciones guardadas en 'visualizaciones_parque_norte.png'")
    
    # Crear mapa interactivo
    print("Creando mapa interactivo...")
    mapa = parque.crear_mapa_interactivo()
    mapa.save('mapa_parque_norte.html')
    print("Mapa guardado en 'mapa_parque_norte.html'")
    
    # Generar reporte
    print("Generando reporte de análisis...")
    reporte = parque.generar_reporte(datos)
    
    with open('reporte_parque_norte.txt', 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print("Reporte guardado en 'reporte_parque_norte.txt'")
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("\nArchivos generados:")
    print("1. visualizaciones_parque_norte.png - Gráficos de análisis")
    print("2. mapa_parque_norte.html - Mapa interactivo")
    print("3. reporte_parque_norte.txt - Reporte detallado")
    
    # Mostrar parte del reporte en consola
    print("\n" + "="*60)
    print("RESUMEN DEL REPORTE:")
    print("="*60)
    lines = reporte.split('\n')[:25]  # Mostrar primeras 25 líneas
    print('\n'.join(lines))
    print("... (ver archivo completo para más detalles)")


if __name__ == "__main__":
    main()