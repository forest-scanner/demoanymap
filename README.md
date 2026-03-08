# Anymap TS - Parque Norte de Madrid

Análisis de series temporales y visualización geoespacial del Parque Norte de Madrid.

## Descripción

Este proyecto implementa un sistema de análisis de series temporales (Time Series) combinado con visualización geoespacial (Anymap) para el Parque Norte de Madrid. Incluye:

- Generación de datos simulados de visitantes
- Análisis de series temporales
- Visualizaciones estadísticas
- Mapa interactivo con Folium
- Reportes automáticos

## Características

1. **Datos Simulados**: Generación de datos realistas de visitantes, temperatura y actividades
2. **Análisis TS**: Procesamiento de series temporales con pandas
3. **Visualización**: Gráficos con matplotlib y mapas interactivos con folium
4. **Geoespacial**: Representación del parque y puntos de interés

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/forest-scanner/anymap-ts-parque-norte-madrid.git
cd anymap-ts-parque-norte-madrid

# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

Ejecutar el análisis principal:

```bash
python parque_norte_madrid.py
```

Esto generará:
- `visualizaciones_parque_norte.png`: Gráficos de análisis
- `mapa_parque_norte.html`: Mapa interactivo
- `reporte_parque_norte.txt`: Reporte de análisis

## Estructura del Proyecto

```
anymap-ts-parque-norte-madrid/
├── parque_norte_madrid.py    # Código principal
├── requirements.txt          # Dependencias
├── README.md                # Documentación
├── .gitignore              # Archivos ignorados por Git
└── ejemplo_analisis.ipynb   # Notebook de ejemplo
```

## Ejemplo de Salida

El análisis incluye:
- Visitantes diarios y tendencias estacionales
- Temperatura media
- Distribución de actividades
- Visitantes por día de la semana
- Mapa interactivo con puntos de interés

## Tecnologías

- Python 3.8+
- Pandas (análisis de datos)
- Matplotlib (visualización)
- Folium (mapas interactivos)
- NumPy (cálculos numéricos)

## Licencia

MIT License

## Autor

Ruben - Proyecto de demostración Anymap TS