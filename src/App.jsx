import { useState } from "react";
import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import CompletedList from "./components/CompletedList";
import "./App.css";


function App() {
const [tasks, setTasks] = useState([]);

// Agregar tarea
const addTask = (texto, fecha, hora) => {
const nueva = {
id: Date.now(),
texto: texto,
fecha: fecha || null, // null si no se proporcionó
hora: hora || null, // null si no se proporcionó
completada: false,
};


// nueva lista inmutable
setTasks((prev) => [...prev, nueva]);


// Mostrar alerta de éxito al agregar
alert("Tarea agregada correctamente");
};


// Completar tarea (no mutamos el objeto original)
const completeTask = (id) => {
const nuevas = tasks.map((t) => (t.id === id ? { ...t, completada: true } : t));
setTasks(nuevas);
alert("Tarea marcada como completada");
};


// Eliminar tarea
const deleteTask = (id) => {
const nuevas = tasks.filter((t) => t.id !== id);
setTasks(nuevas);
alert("Tarea eliminada");
};


// Contadores solicitados
const pendientes = tasks.filter((t) => !t.completada).length;
const realizadas = tasks.filter((t) => t.completada).length;


return (
<div className="app-container">
<h1>Gestor de Tareas</h1>


{/* Formulario para agregar tareas */}
<TaskForm onAdd={addTask} />


{/* Contadores */}
<div className="counters">
<p>Tareas pendientes: {pendientes}</p>
<p>Tareas realizadas: {realizadas}</p>
</div>


<h2>Tareas Pendientes</h2>
<TaskList
tasks={tasks.filter((t) => !t.completada)}
onComplete={completeTask}
onDelete={deleteTask}
/>


<h2>Tareas Completadas</h2>
<CompletedList tasks={tasks.filter((t) => t.completada)} onDelete={deleteTask} />
</div>
);
}


export default App;