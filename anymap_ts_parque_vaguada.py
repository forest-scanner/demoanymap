#!/usr/bin/env python3
"""
Anymap TS - Parque La Vaguada de Madrid
Análisis de series temporales y visualización geoespacial del Parque La Vaguada
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import folium
from folium import plugins
import json
import warnings
warnings.filterwarnings('ignore')

class ParqueLaVaguadaTS:
    """
    Clase para análisis de series temporales del Parque La Vaguada de Madrid
    """
    
    def __init__(self):
        """Inicializa el análisis del Parque La Vaguada"""
        self.nombre = "Parque La Vaguada"
        self.ubicacion = {"lat": 40.4780, "lon": -3.7110}  # Coordenadas aproximadas
        self.datos = None
        self.puntos_interes = self._definir_puntos_interes()
        
    def _definir_puntos_interes(self):
        """Define los puntos de interés del Parque La Vaguada"""
        return {
            "entrada_principal": {"nombre": "Entrada Principal", "lat": 40.4785, "lon": -3.7105, "tipo": "acceso"},
            "lago_central": {"nombre": "Lago Central", "lat": 40.4778, "lon": -3.7112, "tipo": "agua"},
            "area_infantil": {"nombre": "Área Infantil", "lat": 40.4782, "lon": -3.7115, "tipo": "recreo"},
            "pista_deporte": {"nombre": "Pista Deportiva", "lat": 40.4775, "lon": -3.7108, "tipo": "deporte"},
            "zona_arbolada": {"nombre": "Zona Arbolada", "lat": 40.4788, "lon": -3.7118, "tipo": "naturaleza"},
            "anfiteatro": {"nombre": "Anfiteatro", "lat": 40.4772, "lon": -3.7102, "tipo": "cultura"},
            "cafeteria": {"nombre": "Cafetería", "lat": 40.4780, "lon": -3.7100, "tipo": "servicio"},
            "estacionamiento": {"nombre": "Estacionamiento", "lat": 40.4790, "lon": -3.7095, "tipo": "acceso"}
        }
    
    def generar_datos_simulados(self, dias=365):
        """
        Genera datos simulados de visitantes del Parque La Vaguada
        
        Args:
            dias (int): Número de días a simular
        """
        fecha_inicio = datetime(2024, 1, 1)
        fechas = [fecha_inicio + timedelta(days=i) for i in range(dias)]
        
        # Patrones estacionales
        estacionalidad = 50 * np.sin(2 * np.pi * np.arange(dias) / 365)
        
        # Patrón semanal (más visitantes fines de semana)
        semanal = np.array([30 if (fecha.weekday() >= 5) else 0 for fecha in fechas])
        
        # Patrón mensual (más visitantes en primavera/verano)
        mensual = np.array([40 if (fecha.month in [4, 5, 6, 7, 8, 9]) else 0 for fecha in fechas])
        
        # Ruido aleatorio
        ruido = np.random.normal(0, 15, dias)
        
        # Temperatura simulada (correlacionada con visitantes)
        temperatura_base = 15 + 10 * np.sin(2 * np.pi * np.arange(dias) / 365)
        temperatura = temperatura_base + np.random.normal(0, 3, dias)
        
        # Generar visitantes base
        visitantes_base = 200 + estacionalidad + semanal + mensual + ruido
        visitantes_base = np.maximum(visitantes_base, 50)  # Mínimo 50 visitantes
        
        # Ajustar por temperatura (más visitantes con buen tiempo)
        ajuste_temperatura = 0.5 * (temperatura - 15)
        visitantes = visitantes_base + ajuste_temperatura
        visitantes = np.maximum(visitantes, 30)  # Mínimo 30 visitantes
        
        # Actividades (distribución porcentual)
        actividades = {
            'caminar': 0.35,
            'correr': 0.20,
            'ciclismo': 0.15,
            'deporte': 0.10,
            'recreo': 0.12,
            'otros': 0.08
        }
        
        # Generar datos por actividad
        datos_actividades = {}
        for actividad, porcentaje in actividades.items():
            datos_actividades[actividad] = visitantes * porcentaje + np.random.normal(0, 5, dias)
        
        # Crear DataFrame
        self.datos = pd.DataFrame({
            'fecha': fechas,
            'visitantes': visitantes.astype(int),
            'temperatura': temperatura.round(1),
            'dia_semana': [fecha.strftime('%A') for fecha in fechas],
            'mes': [fecha.month for fecha in fechas],
            'es_fin_semana': [1 if fecha.weekday() >= 5 else 0 for fecha in fechas],
            'es_verano': [1 if fecha.month in [6, 7, 8] else 0 for fecha in fechas]
        })
        
        # Añadir datos de actividades
        for actividad, valores in datos_actividades.items():
            self.datos[f'actividad_{actividad}'] = valores.astype(int)
        
        print(f"Datos simulados generados para {dias} días")
        print(f"Visitantes promedio: {self.datos['visitantes'].mean():.0f}")
        print(f"Temperatura promedio: {self.datos['temperatura'].mean():.1f}°C")
        
        return self.datos
    
    def analizar_series_temporales(self):
        """Realiza análisis de series temporales"""
        if self.datos is None:
            print("Primero genera los datos simulados")
            return None
        
        resultados = {}
        
        # Estadísticas básicas
        resultados['estadisticas'] = {
            'total_visitantes': int(self.datos['visitantes'].sum()),
            'promedio_diario': float(self.datos['visitantes'].mean()),
            'maximo_diario': int(self.datos['visitantes'].max()),
            'minimo_diario': int(self.datos['visitantes'].min()),
            'desviacion_estandar': float(self.datos['visitantes'].std())
        }
        
        # Análisis por día de la semana
        resultados['por_dia_semana'] = self.datos.groupby('dia_semana')['visitantes'].agg(['mean', 'sum']).round(0).to_dict()
        
        # Análisis por mes
        resultados['por_mes'] = self.datos.groupby('mes')['visitantes'].agg(['mean', 'sum']).round(0).to_dict()
        
        # Correlación temperatura-visitantes
        correlacion = self.datos['temperatura'].corr(self.datos['visitantes'])
        resultados['correlacion_temperatura'] = float(correlacion)
        
        # Distribución de actividades
        actividades_cols = [col for col in self.datos.columns if col.startswith('actividad_')]
        total_actividades = self.datos[actividades_cols].sum().sum()
        distribucion = {}
        for col in actividades_cols:
            actividad = col.replace('actividad_', '')
            total = self.datos[col].sum()
            porcentaje = (total / total_actividades) * 100
            distribucion[actividad] = {
                'total': int(total),
                'porcentaje': float(porcentaje)
            }
        resultados['distribucion_actividades'] = distribucion
        
        # Tendencia (media móvil 7 días)
        self.datos['media_movil_7d'] = self.datos['visitantes'].rolling(window=7).mean()
        
        return resultados
    
    def crear_visualizaciones(self):
        """Crea visualizaciones del análisis"""
        if self.datos is None:
            print("Primero genera los datos simulados")
            return None
        
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle(f'Análisis de Series Temporales - {self.nombre}', fontsize=16, fontweight='bold')
        
        # 1. Serie temporal de visitantes
        axes[0, 0].plot(self.datos['fecha'], self.datos['visitantes'], alpha=0.7, linewidth=1)
        axes[0, 0].plot(self.datos['fecha'], self.datos['media_movil_7d'], 'r-', linewidth=2, label='Media móvil 7d')
        axes[0, 0].set_title('Visitantes Diarios')
        axes[0, 0].set_xlabel('Fecha')
        axes[0, 0].set_ylabel('Número de Visitantes')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Visitantes vs Temperatura
        scatter = axes[0, 1].scatter(self.datos['temperatura'], self.datos['visitantes'], 
                                     c=self.datos['mes'], alpha=0.6, cmap='viridis')
        axes[0, 1].set_title('Visitantes vs Temperatura')
        axes[0, 1].set_xlabel('Temperatura (°C)')
        axes[0, 1].set_ylabel('Visitantes')
        plt.colorbar(scatter, ax=axes[0, 1], label='Mes')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Visitantes por día de la semana
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dias_espanol = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        visitas_por_dia = self.datos.groupby('dia_semana')['visitantes'].mean().reindex(dias_orden)
        axes[1, 0].bar(dias_espanol, visitas_por_dia.values, color='skyblue')
        axes[1, 0].set_title('Promedio de Visitantes por Día de la Semana')
        axes[1, 0].set_xlabel('Día de la Semana')
        axes[1, 0].set_ylabel('Visitantes Promedio')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Distribución de actividades
        actividades_cols = [col for col in self.datos.columns if col.startswith('actividad_')]
        total_actividades = self.datos[actividades_cols].sum()
        actividades_nombres = [col.replace('actividad_', '').capitalize() for col in actividades_cols]
        axes[1, 1].pie(total_actividades.values, labels=actividades_nombres, autopct='%1.1f%%')
        axes[1, 1].set_title('Distribución de Actividades')
        
        # 5. Visitantes por mes
        visitas_por_mes = self.datos.groupby('mes')['visitantes'].mean()
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        axes[2, 0].bar(meses, visitas_por_mes.values, color='lightgreen')
        axes[2, 0].set_title('Promedio de Visitantes por Mes')
        axes[2, 0].set_xlabel('Mes')
        axes[2, 0].set_ylabel('Visitantes Promedio')
        axes[2, 0].grid(True, alpha=0.3, axis='y')
        
        # 6. Histograma de visitantes
        axes[2, 1].hist(self.datos['visitantes'], bins=30, edgecolor='black', alpha=0.7)
        axes[2, 1].axvline(self.datos['visitantes'].mean(), color='red', linestyle='--', 
                          label=f'Media: {self.datos["visitantes"].mean():.0f}')
        axes[2, 1].set_title('Distribución de Visitantes Diarios')
        axes[2, 1].set_xlabel('Número de Visitantes')
        axes[2, 1].set_ylabel('Frecuencia')
        axes[2, 1].legend()
        axes[2, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('visualizaciones_parque_vaguada.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualizaciones guardadas en 'visualizaciones_parque_vaguada.png'")
        
    def crear_mapa_interactivo(self):
        """Crea un mapa interactivo del Parque La Vaguada"""
        # Crear mapa centrado en el parque
        mapa = folium.Map(
            location=[self.ubicacion['lat'], self.ubicacion['lon']],
            zoom_start=16,
            tiles='cartodbpositron'
        )
        
        # Añadir marcador del parque
        folium.Marker(
            location=[self.ubicacion['lat'], self.ubicacion['lon']],
            popup=f'<b>{self.nombre}</b><br>Parque Urbano',
            icon=folium.Icon(color='green', icon='tree-conifer', prefix='fa')
        ).add_to(mapa)
        
        # Añadir puntos de interés
        colores = {
            'acceso': 'blue',
            'agua': 'lightblue',
            'recreo': 'orange',
            'deporte': 'red',
            'naturaleza': 'green',
            'cultura': 'purple',
            'servicio': 'gray'
        }
        
        iconos = {
            'acceso': 'sign-in',
            'agua': 'tint',
            'recreo': 'child',
            'deporte': 'futbol-o',
            'naturaleza': 'tree',
            'cultura': 'music',
            'servicio': 'coffee'
        }
        
        for punto_id, info in self.puntos_interes.items():
            folium.Marker(
                location=[info['lat'], info['lon']],
                popup=f"<b>{info['nombre']}</b><br>Tipo: {info['tipo']}",
                icon=folium.Icon(color=colores[info['tipo']], icon=iconos[info['tipo']], prefix='fa')
            ).add_to(mapa)
        
        # Añadir círculo para representar el área del parque
        folium.Circle(
            location=[self.ubicacion['lat'], self.ubicacion['lon']],
            radius=200,  # Aproximadamente 200 metros
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.2,
            popup='Área aproximada del parque'
        ).add_to(mapa)
        
        # Añadir control de capas
        folium.LayerControl().add_to(mapa)
        
        # Añadir minimapa
        minimap = plugins.MiniMap()
        mapa.add_child(minimap)
        
        # Guardar mapa
        mapa.save('mapa_parque_vaguada.html')
        
        print(f"Mapa interactivo guardado en 'mapa_parque_vaguada.html'")
        print(f"Abre el archivo en tu navegador para ver el mapa interactivo")
        
        return mapa
    
    def generar_reporte(self, resultados):
        """Genera un reporte detallado del análisis"""
        if resultados is None:
            print("Primero realiza el análisis")
            return None
        
        reporte = f"""
        ============================================
        REPORTE DE ANÁLISIS - PARQUE LA VAGUADA DE MADRID
        ============================================
        
        1. ESTADÍSTICAS GENERALES:
        --------------------------
        • Total de visitantes: {resultados['estadisticas']['total_visitantes']:,}
        • Promedio diario: {resultados['estadisticas']['promedio_diario']:.0f} visitantes
        • Máximo diario: {resultados['estadisticas']['maximo_diario']} visitantes
        • Mínimo diario: {resultados['estadisticas']['minimo_diario']} visitantes
        • Desviación estándar: {resultados['estadisticas']['desviacion_estandar']:.0f} visitantes
        • Correlación temperatura-visitantes: {resultados['correlacion_temperatura']:.2f}
        
        2. ANÁLISIS POR DÍA DE LA SEMANA:
        ----------------------------------
        """
        for dia, valores in resultados['por_dia_semana'].items():
            reporte += f"  • {dia}: Promedio = {valores['mean']:.0f}, Total = {valores['sum']:.0f}\n"
        
        reporte += f"""
        
        3. ANÁLISIS POR MES:
        ----------------------
        """
        for mes, valores in resultados['por_mes'].items():
            reporte += f"  • Mes {mes}: Promedio = {valores['mean']:.0f}, Total = {valores['sum']:.0f}\n"
        
        reporte += f"""
        
        4. DISTRIBUCIÓN DE ACTIVIDADES:
        --------------------------------
        """
        for actividad, datos in resultados['distribucion_actividades'].items():
            reporte += f"  • {actividad.capitalize()}: {datos['porcentaje']:.1f}% ({datos['total']})
"
        
        reporte += """
        
        ============================================
        FIN DEL REPORTE
        ============================================
        """
        
        with open('reporte_parque_vaguada.txt', 'w') as f:
            f.write(reporte)
        
        print("Reporte guardado en 'reporte_parque_vaguada.txt'")


if __name__ == "__main__":
    analisis = ParqueLaVaguadaTS()
    datos = analisis.generar_datos_simulados(dias=365)
    resultados = analisis.analizar_series_temporales()
    analisis.crear_visualizaciones()
    analisis.crear_mapa_interactivo()
    analisis.generar_reporte(resultados)
