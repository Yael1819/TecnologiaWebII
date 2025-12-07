// este componente recibe
// tasks  un arreglo con todas las tareas no completadas
// onComplete  funcion que marca una tarea como completada
// onDelet funcion que elimina una tarea
function TaskList({ tasks, onComplete, onDelete }) {
  return (
    <div className="task-list">

      {/* si no hay tareas en el arreglo se muestra un mensaje */}
      {tasks.length === 0 && <p>No hay tareas</p>}

      {/* Se recorre la lista usando .map para renderizar un TaskItem por cada tarea.
          cada TaskItem recibe los datos de la tarea y las funciones del padre. 
      */}
      {tasks.map((task) => (
        <TaskItem
          key={task.id}            // react usa key para optimizar listas
          task={task}              // se pasa la info completa de la tarea
          onComplete={onComplete}  // funcin que completa la tarea
          onDelete={onDelete}      // funcion que elimina la tarea
        />
      ))}
    </div>
  );
}

export default TaskList;
