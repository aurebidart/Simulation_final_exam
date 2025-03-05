# Simulador de Atención en un Cajero Automático

Este proyecto es una simulación de un sistema de atención en un cajero con un único servidor, donde los clientes llegan en intervalos de tiempo exponenciales y reciben un servicio con tiempos también exponenciales. La simulación permite configurar distintos parámetros y visualizar los resultados en forma de estadísticas, tablas y gráficos.

## 📌 Enunciado

Este proyecto parte del enunciado de la materia **Simulación** de la **Universidad Tecnológica Nacional – Facultad Regional Córdoba**:

> Un promedio de 10 automóviles por hora llegan a un cajero con un solo servidor que proporciona servicio sin que uno descienda del automóvil. Suponga que el tiempo de servicio promedio por cada cliente es de 4 minutos, y que tanto los tiempos de llegadas como los de servicios son exponenciales.

El objetivo es responder las siguientes preguntas mediante la simulación:

1. ¿Cuál es la probabilidad de que el cajero esté ocioso?
2. ¿Cuál es el número promedio de automóviles que están en la cola del cajero?
3. ¿Cuál es la cantidad promedio de tiempo que un cliente pasa haciendo cola?
4. ¿Cuántos clientes atenderá en promedio el cajero por hora?

## 📦 Requisitos

Este proyecto utiliza **Python** junto con las siguientes librerías:

- `tkinter`: Para la interfaz gráfica.
- `matplotlib`: Para generar gráficos.
- `random`, `math`, `copy`: Para manejar la simulación y sus datos.

Para instalar las dependencias necesarias, ejecuta:

```sh
pip install matplotlib
```

## 🚀 Ejecución

Para correr la simulación, simplemente ejecuta el archivo principal:

```sh
python main.py
```

Se abrirá una interfaz gráfica que permitirá configurar los parámetros de la simulación y visualizar los resultados.

## 🛠 Funcionalidades

### 1️⃣ Configuración de la Simulación
- Definir la tasa de llegada de autos (media de tiempo entre llegadas o frecuencia por hora).
- Definir la tasa de servicio del cajero.
- Especificar la duración de la simulación (en minutos o cantidad de eventos).

### 2️⃣ Ejecución de la Simulación
- Se genera un modelo basado en eventos discretos.
- Se simulan las llegadas y atenciones de los autos.
- Se registran los datos de cada evento.

### 3️⃣ Resultados
- **Estadísticas generales**
  - Probabilidad de que el cajero esté ocioso.
  - Número promedio de autos en la cola.
  - Tiempo promedio de espera en la cola.
  - Promedio de clientes atendidos por hora.
- **Visualización de Datos**
  - Tabla detallada de eventos.
  - Gráficos de evolución del sistema.

## 🖥 Interfaz Gráfica

La aplicación tiene dos ventanas principales:

1. **Configuración de la Simulación**: Permite ingresar los parámetros antes de iniciar la simulación.
2. **Resultados**: Muestra estadísticas clave, permite visualizar datos en tabla y gráficos.

## 📊 Ejemplo de Resultados

- Probabilidad de inactividad: `0.25`
- Autos promedio en la cola: `1.5`
- Tiempo promedio de espera: `3.2 minutos`
- Clientes atendidos por hora: `8.5`

## 🔗 Contribución

Si deseas mejorar la simulación o agregar nuevas funcionalidades, puedes hacer un fork del repositorio y enviar un pull request.

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**, por lo que puedes utilizarlo y modificarlo libremente.

Hecho con ❤️ por Aurelio García Bidart