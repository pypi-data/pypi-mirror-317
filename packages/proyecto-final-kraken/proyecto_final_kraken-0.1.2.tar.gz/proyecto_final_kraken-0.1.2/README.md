# Proyecto Final - Bandas de Bollinger en Kraken

Este proyecto permite descargar cotizaciones de pares de monedas desde Kraken, calcular las Bandas de Bollinger y generar señales de compra/venta basadas en los cruces de estas bandas. El resultado se visualiza en un gráfico interactivo.

---

## **Requisitos del sistema**
- Python 3.9 o superior
- Sistema operativo: Windows, macOS o Linux

---

## **Configuración del entorno**

### **Usando un entorno virtual con `venv`**
1. Asegúrate de estar en el directorio del proyecto:
   ```bash
   cd "D:\Cursos\Master Big Data\Curso Python\Proyecto\Proyecto Final"
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv env
   ```

3. Activa el entorno virtual:
   - **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source env/bin/activate
     ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Ejecución del proyecto**

1. Activa el entorno virtual (si no lo has hecho ya):
   ```bash
   .\env\Scripts\activate
   ```

2. Ejecuta el programa principal:
   ```bash
   python main.py
   ```

3. Sigue las instrucciones en la terminal para seleccionar un par de monedas, descargar datos y visualizar el análisis en un gráfico.

---

## **Descripción técnica**

### **Bandas de Bollinger**
Este proyecto utiliza las Bandas de Bollinger como indicador técnico para analizar la volatilidad del precio:
- **Banda superior**: EMA20 + 2 * desviación estándar.
- **Banda inferior**: EMA20 - 2 * desviación estándar.
- **EMA20**: Media móvil exponencial de 20 periodos.

### **Señales de compra/venta**
Se generan señales basadas en los cruces del precio con las Bandas de Bollinger:
- **Compra**: El precio cruza hacia arriba la banda inferior.
- **Venta**: El precio cruza hacia abajo la banda superior.

---

## **Estructura del proyecto**

```plaintext
Proyecto Final/
├── proyecto_kraken/             # Paquete principal
│   ├── __init__.py              # Inicializa el paquete
│   ├── bollinger_bands.py       # Módulo para las Bandas de Bollinger
│   ├── kraken_client.py         # Módulo para interactuar con la API de Kraken
│   ├── plot_utils.py            # Módulo para graficar
│   ├── main.py                  # Script principal del proyecto
├── tests/                       # Pruebas unitarias del proyecto
│   ├── test_bollinger.py        # Pruebas unitarias para Bandas de Bollinger
│   ├── test_kraken.py           # Pruebas unitarias para Kraken
│   ├── test_plot.py             # Pruebas unitarias para las gráficas
├── .gitignore                   # Exclusiones para Git
├── MANIFEST.in                  # Archivos adicionales para incluir en el paquete
├── pytest.ini                   # Configuración para pytest
├── README.md                    # Documentación del proyecto
├── requirements.txt             # Dependencias del proyecto para pip
├── setup.py                     # Configuración para empaquetar y distribuir
```

---

## **Ejemplo de ejecución**

### **Selección de par de monedas**
El programa solicitará que selecciones un par de monedas disponible en Kraken, como por ejemplo:
```plaintext
Seleccione el número correspondiente al par de monedas:
1. BTC/USD
2. ETH/USD
3. XRP/USD
Has seleccionado: BTC/USD
```

---

## **Reproducibilidad del entorno**

### **Con Conda**
Si prefieres usar Conda para gestionar el entorno virtual:
1. Instala Miniconda desde: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Crea el entorno virtual desde el archivo `environment.yml`:
   ```bash
   conda env create -f environment.yml
   ```
3. Activa el entorno:
   ```bash
   conda activate proy1
   ```

4. Ejecuta el programa:
   ```bash
   python main.py
   ```

---

## **Dependencias**
El proyecto utiliza las siguientes librerías:
- `krakenex`
- `matplotlib`
- `pandas`
- `numpy` (si es necesaria)

---

## **Autor**
**Pedro Montt Pacheco**  
Estudiante del Máster en Big Data - Universidad de Navarra