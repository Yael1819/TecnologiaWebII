// El componente TaskItem recibe 3 props
// task un objeto que contiene todo lo relacionado a la tarea 
// onComplte  funcion que viene del componente padre y marca la tarea como completada
// onDelete  función que elimina una tarea según su id
function TaskItem({ task, onComplete, onDelete }) {

  return (
    // Cada tarea individual está envuelta en un <li> para mantener el formato de lista
    <li className="task-item">

      {/* contenedor para organizar el texto y la fecha/hora */}
      <div className="task-content">

        {/* muestra siempre el texto de la tarea */}
        <span className="task-text">{task.texto}</span>

        {/* renderizado condicional
            Este bloque solo se muestra si la tarea tiene una fecha o una hora
            Si ambas están vacias no aparece nada
        */}
        {(task.fecha || task.hora) && (
          <div className="task-datetime">

            {/* muestra la fecha solamente si existe */}
            {task.fecha && <span className="date"> {task.fecha}</span>}

            {/* Muestra la hora solamente si existe */}
            {task.hora && <span className="time"> {task.hora}</span>}
          </div>
        )}
      </div>

      {/* Zona de botones de accion */}
      <div className="task-actions">

        {/* el boton de completar solo aparece si la tarea no esta completada */}
        {!task.completada && (
          <button
            // llama a la funcion del padre pasando el id de la tarea
            onClick={() => onComplete(task.id)}
            className="btn-complete"
          >
            Completar
          </button>
        )}

        {/* boto de eliminar que siempre aparece */}
        <button
          // llama a la funcion del padre para eliminar la tarea
          onClick={() => onDelete(task.id)}
          className="btn-delete"
        >
          Eliminar
        </button>
      </div>
    </li>
  );
}

export default TaskItem;
