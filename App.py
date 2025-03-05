import tkinter as tk # Libería de Python para crear interfaces gráficas
from tkinter import ttk
import matplotlib.pyplot as plt # Librería para crear gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
import copy #para mantener una copia de los datos

class Cliente:
    def __init__(self, id, status, arrival_time):
        self.id = id
        self.status = status
        self.arrival_time = arrival_time

class SimulationSetup:
    """Primera ventana: Configuración de la simulación."""
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración de Simulación")
        self.root.geometry("500x400")

        # Variables para los parámetros de la simulación. Rate, es el valor (mu), type es el tipo de dato
        self.arrival_rate = tk.DoubleVar(value=6.0)
        self.arrival_type = tk.StringVar(value="Tiempo medio entre llegadas")
        self.service_rate = tk.DoubleVar(value=4.0)
        self.service_type = tk.StringVar(value="Tiempo medio de servicio")

        self.simulation_data = []   # Datos de la simulación
        self.current_data = {}      # Datos actuales
        self.previous_data = {}     # Datos previos
        self.contador_autos = 0     # Contador de autos. Se usa para asignar un id a cada auto

        # Configuración de tiempo
        self.simulation_duration_type = tk.StringVar(value="Minutos") # Unidad de tiempo (Minutos o Eventos)
        self.simulation_duration = tk.IntVar(value=60)

        self.create_widgets()   # Crea la ventana de configuración

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10") # Frame principal. Definición de ventana.
        frame.pack(expand=True, fill="both")

        # Configuración de estilos
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 12, "bold"), foreground="blue")
        style.configure("Section.TLabel", font=("Helvetica", 10, "bold"), foreground="darkgreen")
        style.configure("Entry.TEntry", font=("Helvetica", 10))
        style.configure("TCombobox", font=("Helvetica", 10))

        # Título de la sección de llegada de autos
        ttk.Label(frame, text="Configuración de Llegada de Autos", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Selección entre "Tiempo medio entre llegadas" y "Frecuencia media de llegadas"
        ttk.Label(frame, text="Tipo de parámetro de llegada:", style="Section.TLabel").grid(row=1, column=0, sticky="w")
        arrival_type_combobox = ttk.Combobox(frame, textvariable=self.arrival_type, values=["Tiempo medio entre llegadas", "Frecuencia media de llegadas"])
        arrival_type_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        arrival_type_combobox.bind("<<ComboboxSelected>>", self.update_arrival_label)  # Actualizar etiqueta al cambiar

        # Etiqueta dinámica para el parámetro de llegada
        self.arrival_label = ttk.Label(frame, text="Tiempo medio entre llegadas (minutos):", style="Section.TLabel")
        self.arrival_label.grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.arrival_rate, style="Entry.TEntry").grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Separador
        ttk.Separator(frame, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        # Título de la sección de servicio
        ttk.Label(frame, text="Configuración de Servicio", style="Title.TLabel").grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Selección entre "Tiempo medio de servicio" y "Frecuencia media de servicio"
        ttk.Label(frame, text="Tipo de parámetro de servicio:", style="Section.TLabel").grid(row=5, column=0, sticky="w")
        service_type_combobox = ttk.Combobox(frame, textvariable=self.service_type, values=["Tiempo medio de servicio", "Frecuencia media de servicio"])
        service_type_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        service_type_combobox.bind("<<ComboboxSelected>>", self.update_service_label)  # Actualizar etiqueta al cambiar

        # Etiqueta dinámica para el parámetro de servicio
        self.service_label = ttk.Label(frame, text="Tiempo medio de servicio (minutos):", style="Section.TLabel")
        self.service_label.grid(row=6, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.service_rate, style="Entry.TEntry").grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        # Separador
        ttk.Separator(frame, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

        # Título de la sección de duración de la simulación
        ttk.Label(frame, text="Duración de la Simulación", style="Title.TLabel").grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Configuración de tiempo
        ttk.Label(frame, text="Unidad de tiempo:", style="Section.TLabel").grid(row=9, column=0, sticky="w")
        time_unit_combobox = ttk.Combobox(frame, textvariable=self.simulation_duration_type, values=["Minutos", "Eventos"])
        time_unit_combobox.grid(row=9, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(frame, text="Duración de la simulación:", style="Section.TLabel").grid(row=10, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.simulation_duration, style="Entry.TEntry").grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        # Botón para iniciar la simulación
        ttk.Button(frame, text="Iniciar Simulación", command=self.run_simulation, style="Accent.TButton").grid(row=11, column=0, columnspan=2, pady=20)

        # Ajustar el tamaño de las columnas
        frame.columnconfigure(1, weight=1)

    def update_arrival_label(self, event=None):
        """Actualiza la etiqueta del parámetro de llegada según la selección del usuario."""
        if self.arrival_type.get() == "Tiempo medio entre llegadas":
            self.arrival_label.config(text="Tiempo medio entre llegadas (minutos):")
        else:
            self.arrival_label.config(text="Frecuencia media de llegadas (autos por hora):")
    
    def update_service_label(self, event=None):
        """Actualiza la etiqueta del parámetro de servicio según la selección del usuario."""
        if self.service_type.get() == "Tiempo medio de servicio":
            self.service_label.config(text="Tiempo medio de servicio (minutos):")
        else:
            self.service_label.config(text="Frecuencia media de servicio (autos por hora):")

    def run_simulation(self):
        """Inicia la simulación con los parámetros configurados."""
        
        if self.arrival_type.get() == "Frecuencia media de llegadas":   # Hace la transfomración de la frecuencia a mu
            self.arrival_rate.set(60 / self.arrival_rate.get())
        
        if self.service_type.get() == "Frecuencia media de servicio":   # Hace la transfomración de la frecuencia a mu
            self.service_rate.set(60 / self.service_rate.get())
        
        self.simulate()
        data_results = SimulationResults(tk.Toplevel(), self.simulation_data, self.previous_data, self.current_data) # Crea ventana de resultados
    
    def simulate(self):
        """Ejecuta la simulación"""
        # Reiniciar los datos de la simulación
        self.simulation_data = []
        self.contador_autos = 1 # Id de autos
        
        # Inicializar los datos de la simulación
        random1 = random.random()
        self.current_data = {
            "event": "Inicialización",
            "clock": 0,
            "random1": random1,
            "timeBetweenArrivals": -1 * self.arrival_rate.get() * math.log(1 - random1),
            "nextArrival": -1 * self.arrival_rate.get() * math.log(1 - random1),
            "random2": 0,
            "serviceTime": 0,
            "serviceCompletion": 100000000000, # Valor muy alto para asegurar que el primer cliente sea atendido
            "serverStatus": "Libre",
            "queueLength": 0,
            "idleTimeAccumulator": 0,    # Acumulador de tiempo ocioso
            "waitingTimeAccumulator": 0, # Acumulador de tiempo de espera
            "carsServedCount": 0,        # Contador de autos con acceso a la caja
            "carsCompletedCount": 0,     # Acumulador de autos con atención finalizada
            "cars": []
        }
        
        print("Simulación iniciada") # logueo de la sumulación iniciada
        self.simulation_data.append(copy.deepcopy(self.current_data)) # A la tabla se le agrega el current data
        
        i = 1 # Iterador contador de eventos
        # Si la unidad de tiempo es en minutos comparar con el clock
        # si es en eventos comparar con el iterador i
        while (self.simulation_duration_type.get() == "Minutos" and self.current_data.get("clock") < self.simulation_duration.get()) or (self.simulation_duration_type.get() == "Eventos" and i < self.simulation_duration.get()):
            self.previous_data = copy.deepcopy(self.current_data)
            
            # Evento Llegada de cliente
            if self.previous_data.get("nextArrival") < self.previous_data.get("serviceCompletion"):
                self.current_data["event"] = "Llegada auto " + str(self.contador_autos) 
                self.current_data["clock"] = self.previous_data.get("nextArrival")
                
                # Llegada de cliente
                self.current_data["random1"] = random.random()
                self.current_data["timeBetweenArrivals"] = -1 * self.arrival_rate.get() * math.log(1 - self.current_data.get("random1"))
                self.current_data["nextArrival"] = self.current_data.get("clock") + self.current_data.get("timeBetweenArrivals")
                
                # Fin atención
                if self.previous_data.get("serverStatus") == "Libre": # Pregunta si el servidor está libre
                    self.current_data["random2"] = random.random()
                    self.current_data["serviceTime"] = -1 * self.service_rate.get() * math.log(1 - self.current_data.get("random2"))
                    self.current_data["serviceCompletion"] = self.current_data.get("clock") + self.current_data.get("serviceTime")
                else:
                    self.current_data["random2"] = ''
                    self.current_data["serviceTime"] = ''
                    self.current_data["serviceCompletion"] = self.previous_data.get("serviceCompletion") # Arrastra el tiempo del cliente anterior 
                
                # Servidor
                self.current_data["serverStatus"] = "Ocupado" # Siempre está ocupado cuando llega un cliente. 
                if self.previous_data.get("serverStatus") == "Libre":
                    self.current_data["queueLength"] = 0
                else:
                    self.current_data["queueLength"] = self.previous_data.get("queueLength") + 1
                    
                # Estadísticas
                # Acumulado de tiempo ocioso
                if self.previous_data.get("serverStatus") == "Libre":
                    self.current_data["idleTimeAccumulator"] = self.previous_data.get("idleTimeAccumulator") + self.current_data.get("clock") - self.previous_data.get("clock")
                else:
                    self.current_data["idleTimeAccumulator"] = self.previous_data.get("idleTimeAccumulator") # Arrastra el tiempo ocioso acumulado hasta el momento
                
                # Acumulado tiempo de espera
                self.current_data["waitingTimeAccumulator"] = self.previous_data.get("waitingTimeAccumulator")
                
                # Contador de autos con acceso a la caja
                if self.previous_data.get("serverStatus") == "Libre":
                    self.current_data["carsServedCount"] = self.previous_data.get("carsServedCount") + 1
                else:
                    self.current_data["carsServedCount"] = self.previous_data.get("carsServedCount")
                
                # Acumulador clientes con atención finalizada
                self.current_data["carsCompletedCount"] = self.previous_data.get("carsCompletedCount")
                
                #Autos
                cliente = Cliente(self.contador_autos, "Esperando atención", self.current_data.get("clock")) # Por defecto tiene el estado "Esperando atención"
                if self.previous_data.get("serverStatus") == "Libre": # Acá pregunto el estado del servidor
                    cliente.status = "Siendo atendido"
                
                # Update cars
                self.current_data["cars"].append(cliente)
                self.contador_autos += 1
            # Evento Fin de atención
            else:
                self.current_data["event"] = "Fin atención auto " + str(self.current_data.get("cars")[0].id) # El que se está atendiendo es el primero del array por eso [0]
                self.current_data["clock"] = self.previous_data.get("serviceCompletion") # EL tiempo del clock actual es el tiempo de fin de atención 
                
                # Llegada de cliente
                self.current_data["random1"] = ''
                self.current_data["timeBetweenArrivals"] = ''
                self.current_data["nextArrival"] = self.previous_data.get("nextArrival")
                
                # Fin de atención
                if self.previous_data.get("queueLength") > 0:
                    self.current_data["random2"] = random.random()
                    self.current_data["serviceTime"] = -1 * self.service_rate.get() * math.log(1 - self.current_data.get("random2")) # Acá se cambiar la distribución
                    self.current_data["serviceCompletion"] = self.current_data.get("clock") + self.current_data.get("serviceTime")
                else:
                    self.current_data["random2"] = ''
                    self.current_data["serviceTime"] = ''
                    self.current_data["serviceCompletion"] = 100000000000
                
                # Servidor
                if self.previous_data.get("queueLength") > 0:
                    self.current_data["serverStatus"] = "Ocupado"
                    self.current_data["queueLength"] = self.previous_data.get("queueLength") - 1
                else:
                    self.current_data["serverStatus"] = "Libre"
                    self.current_data["queueLength"] = 0
                
                # Estadísticas
                # Acumulado de tiempo ocioso
                self.current_data["idleTimeAccumulator"] = self.previous_data.get("idleTimeAccumulator") # Arrastra el anterior, porque si es un fin de atención no suma tiempo ocioso
                
                # Acumulado tiempo de espera
                if self.previous_data.get("queueLength") > 0:
                    self.current_data["waitingTimeAccumulator"] = self.previous_data.get("waitingTimeAccumulator") + self.current_data.get("clock") - self.previous_data.get("cars")[1].arrival_time
                else:
                    self.current_data["waitingTimeAccumulator"] = self.previous_data.get("waitingTimeAccumulator") # No había nadie en la cola, arrastra el anterior
                
                # Contador de autos con acceso a la caja
                if self.previous_data.get("queueLength") > 0:
                    self.current_data["carsServedCount"] = self.previous_data.get("carsServedCount") + 1
                else:
                    self.current_data["carsServedCount"] = self.previous_data.get("carsServedCount")
                
                # Acumulador clientes con atención finalizada
                self.current_data["carsCompletedCount"] = self.previous_data.get("carsCompletedCount") + 1
                
                # Autos
                self.current_data["cars"].pop(0)
                if self.previous_data.get("queueLength") > 0:
                    self.current_data["cars"][0].status = "Siendo atendido" # Cambia el id de 1 a 0 porque se eliminó el primero
            
            # Guardar los datos de la simulación
            self.simulation_data.append(copy.deepcopy(self.current_data)) # Se agrega el current data a la tabla
            
            i += 1
        print("Simulación finalizada") # logueo de la simulación finalizada

class SimulationResults:
    """Segunda ventana: Muestra los resultados de la simulación."""
    def __init__(self, root, simulation_data, previous_data, current_data):
        self.root = root
        self.root.title("Simulación Finalizada")
        self.root.geometry("450x300")
        
        self.range_type = tk.StringVar(value="Eventos")
        self.view_from = tk.IntVar(value=0)
        self.view_to = tk.IntVar(value=60)
        
        self.simulation_data = simulation_data # Guarda los datos de la simulación
        self.previous_data = previous_data
        self.current_data = current_data
        self.idle_probability = current_data.get("idleTimeAccumulator") / current_data.get("clock")
        self.average_cars_in_queue = current_data.get("waitingTimeAccumulator") / current_data.get("clock")
        self.average_waiting_time = current_data.get("waitingTimeAccumulator") / current_data.get("carsServedCount")
        self.average_customers_per_hour = current_data.get("carsCompletedCount") / current_data.get("clock") * 60
        

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(expand=True, fill="both")

        # Configuración de estilos
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 12, "bold"), foreground="blue")
        style.configure("Data.TLabel", font=("Helvetica", 10))
        style.configure("Entry.TEntry", font=("Helvetica", 10))

        # Estadísticas generales
        ttk.Label(frame, text="Estadísticas generales", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(frame, text="Probabilidad de que el cajero esté ocioso:", style="Data.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Label(frame, text=f"{self.idle_probability:.2f}", style="Data.TLabel").grid(row=1, column=1, sticky="w")

        ttk.Label(frame, text="Número promedio de autos en la cola:", style="Data.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Label(frame, text=f"{self.average_cars_in_queue:.2f}", style="Data.TLabel").grid(row=2, column=1, sticky="w")

        ttk.Label(frame, text="Tiempo promedio de espera en la cola:", style="Data.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(frame, text=f"{self.average_waiting_time:.2f} minutos", style="Data.TLabel").grid(row=3, column=1, sticky="w")

        ttk.Label(frame, text="Promedio de clientes atendidos por hora:", style="Data.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Label(frame, text=f"{self.average_customers_per_hour:.2f}", style="Data.TLabel").grid(row=4, column=1, sticky="w")

        # Separador
        ttk.Separator(frame, orient="horizontal").grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # Configuración de tiempo de visualización
        
        # Selector de tipo de rango a visualizar (eventos o tiempo)
        ttk.Label(frame, text="Definir rango en:", style="Title.TLabel").grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 10))
        ttk.Radiobutton(frame, text="Eventos", variable=self.range_type, value="Eventos").grid(row=7, column=0, sticky="w")
        ttk.Radiobutton(frame, text="Tiempo (minutos)", variable=self.range_type, value="time").grid(row=7, column=1, sticky="w")
        
        # Entradas para el rango de visualización
        ttk.Label(frame, text="Desde:", style="Data.TLabel").grid(row=8, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.view_from, style="Entry.TEntry").grid(row=8, column=1, sticky="w")
        ttk.Label(frame, text="Hasta:", style="Data.TLabel").grid(row=9, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.view_to, style="Entry.TEntry").grid(row=9, column=1, sticky="w")
        
        # Botones para mostrar la tabla y los histogramas
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Mostrar tabla", command=self.show_table).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Mostrar histogramas", command=self.show_graphs).pack(side="left", padx=5)
    
    def show_table(self):
        root_table = tk.Tk()
        if self.range_type.get() == "Eventos":
            root_table.title("Resultados de la Simulación (Eventos)")
            data_table = DataTable(root_table, self.simulation_data[self.view_from.get():self.view_to.get()], self.previous_data, self.current_data) # Crea la tabla con los datos del rango seleccionado. Instancia a la clase DataTable
        else:
            root_table.title("Resultados de la Simulación (Tiempo)")
            data_table = DataTable(root_table, [data for data in self.simulation_data if data["clock"] >= self.view_from.get() and data["clock"] <= self.view_to.get()], self.previous_data, self.current_data)
    
    def show_graphs(self):
        # Extraer los datos relevantes de simulation_data
        if self.range_type.get() == "Eventos":
            data = self.simulation_data[self.view_from.get():self.view_to.get()]
        else:
            data = [data for data in self.simulation_data if data["clock"] >= self.view_from.get() and data["clock"] <= self.view_to.get()]
        clocks = [data["clock"] for data in data] # Guarda toda la información de la simulación para luego mostrarlo en los gráficos
        idle_times = [data["idleTimeAccumulator"] for data in data]
        waiting_times = [data["waitingTimeAccumulator"] for data in data]
        cars_served = [data["carsServedCount"] for data in data]
        cars_completed = [data["carsCompletedCount"] for data in data]

        # Crear una nueva ventana para los gráficos
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Gráficos de Resultados")
        graph_window.geometry("800x600")

        # Crear una figura de matplotlib con 4 subplots
        fig, axes = plt.subplots(2, 2, figsize=(8, 6))
        fig.suptitle("Gráficos de Resultados de la Simulación")

        # Gráfico de idleTimeAccumulator vs clock
        axes[0, 0].plot(clocks, idle_times, color="blue", marker="o", linestyle="-")
        axes[0, 0].set_title("Tiempo de Inactividad Acumulado")
        axes[0, 0].set_xlabel("Clock")
        axes[0, 0].set_ylabel("Tiempo de Inactividad")

        # Gráfico de waitingTimeAccumulator vs clock
        axes[0, 1].plot(clocks, waiting_times, color="green", marker="o", linestyle="-")
        axes[0, 1].set_title("Tiempo de Espera Acumulado")
        axes[0, 1].set_xlabel("Clock")
        axes[0, 1].set_ylabel("Tiempo de Espera")

        # Gráfico de carsServedCount vs clock
        axes[1, 0].plot(clocks, cars_served, color="orange", marker="o", linestyle="-")
        axes[1, 0].set_title("Autos Atendidos")
        axes[1, 0].set_xlabel("Clock")
        axes[1, 0].set_ylabel("Número de Autos Atendidos")

        # Gráfico de carsCompletedCount vs clock
        axes[1, 1].plot(clocks, cars_completed, color="red", marker="o", linestyle="-")
        axes[1, 1].set_title("Autos Completados")
        axes[1, 1].set_xlabel("Clock")
        axes[1, 1].set_ylabel("Número de Autos Completados")

        # Ajustar el layout en una sola ventana
        plt.tight_layout()

        # Integrar la figura en la ventana de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

class DataTable:
    """Segunda ventana: Muestra la tabla con los resultados de la simulación."""
    def __init__(self, root, simulation_data, previous_data, current_data):
        self.root = root # Ventana principal
        self.root.title("Resultados de la Simulación")
        self.root.geometry("1200x600")
        
        self.simulation_data = simulation_data # Pasa info y la guarda en la clase
        self.previous_data = previous_data
        self.current_data = current_data
        for data in self.simulation_data: # Recorre la simulación y guarda el primer y último auto para saber cuantas columnas se van a dibujar
            if data.get("cars"):
                self.first_car = data.get("cars")[0].id
                break
        for data in self.simulation_data[::-1]:
            if data.get("cars"):
                self.last_car = data.get("cars")[-1].id
                break

        self.create_widgets()
        
        self.update_table()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(expand=True, fill="both")

        columns = ("Evento", "Reloj", "RND1", "TpoEntreLlegadas", "ProxLlegada",
                    "RND2", "TpoServicio", "FinAtención", "Estado", "Cola",
                    "ACTpoOcioso", "ACTpoEspera", "AutosAtendidos",
                    "AutosCompletados")

        if self.last_car - self.first_car < 1000: # Limitación de la cantidad de autos a mostrar en la tabla
            for car in range(self.first_car, self.last_car + 1):
                columns += (f"Car {car} Status", f"Car {car} Arrival Time")

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Definir los encabezados y el ancho de las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)

        # Scrollbar vertical
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Scrollbar horizontal
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)

        # Organizar con grid para mejor control del layout. Divide la ventana en filas y columnas (grilla)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Botón para cerrar la ventana
        ttk.Button(self.root, text="Cerrar", command=self.root.destroy).pack(pady=10)

    def update_table(self):
        
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla actual
        
        for data in self.simulation_data:
            if data.get("serviceCompletion") == 100000000000:
                data["serviceCompletion"] = ''
        
        # Para toda la informacion de la simulacion, previous data y current data
        for entry in self.simulation_data: # Round para redondear los valores
            row_data = [
                entry["event"],
                round(entry["clock"], 4),
                round(entry["random1"], 4)              if entry["random1"] != '' else '',
                round(entry["timeBetweenArrivals"], 4)  if entry["timeBetweenArrivals"] != '' else '',
                round(entry["nextArrival"], 4),
                round(entry["random2"], 4)              if entry["random2"] != '' else '',
                round(entry["serviceTime"], 4)          if entry["serviceTime"] != '' else '',
                round(entry["serviceCompletion"], 4)    if entry["serviceCompletion"] != '' else '',
                entry["serverStatus"],
                entry["queueLength"],
                round(entry["idleTimeAccumulator"], 4),
                round(entry["waitingTimeAccumulator"], 4),
                entry["carsServedCount"],
                entry["carsCompletedCount"],
            ]
            
            # Si el rango de autos es menor a 1000, se agregan los estados y tiempos de llegada de los autos
            # en la tabla
            if (self.last_car - self.first_car) < 1000:
                last_id = self.first_car
                for car in entry.get("cars"):
                    for empy in range(last_id, car.id):
                        row_data.append('')
                        row_data.append('')
                    row_data.append(car.status)
                    row_data.append(round(car.arrival_time, 4))
                    last_id = car.id + 1
            self.tree.insert("", "end", values=row_data) # Inserta los valores en la tabla

if __name__ == "__main__":
    root_setup = tk.Tk()
    app_setup = SimulationSetup(root_setup)
    root_setup.mainloop()
