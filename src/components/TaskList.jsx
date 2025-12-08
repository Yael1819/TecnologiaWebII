// Importamos el componente TaskItem para poder usarlo dentro de la lista
import TaskItem from "./TaskItem";

// Componente TaskList
// Recibe 3 props:
//   tasks: lista de tareas pendientes (no completadas)
//  -onComplete: funcion que marca una tarea como completada
//  -onDelete: funcion para eliminar una tarea
function TaskList({ tasks, onComplete, onDelete }) {
  return (
    // Contenedor principal de la lista
    <div className="task-list">

      {/* Si no hay tareas en el arreglo, se muestra un mensaje */}
      {tasks.length === 0 && <p>No hay tareas</p>}

      {/* Recorremos todas las tareas usando .map.
          Por cada tarea generamos un componente TaskItem. */}
      {tasks.map((task) => (
        <TaskItem
          key={task.id}          // clave unica para ayudar a React a optimizar la lista
          task={task}            // se pasa toda la información de la tarea
          onComplete={onComplete} // funcion para completar la tarea
          onDelete={onDelete}     // funcin para eliminar la tarea
        />
      ))}
    </div>
  );
}

// Exportamos el componente para poder usarlo en otros archivos
export default TaskList;
