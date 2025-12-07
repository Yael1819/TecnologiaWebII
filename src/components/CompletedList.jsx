// El componente recibe dos props:
// tasks  lista de tareas completadas
// onDelete  funcion para eliminar una tarea
function CompletedList({ tasks, onDelete }) {

  // Si no hay tareas conpletadas mostramos un mensaje
  if (tasks.length === 0) {
    return <p>No hay tareas completadas.</p>;
  }

  // Si  hay tareas renderizamos una lista <ul>
  return (
    <ul>
      {/* recorremos todas las tareas completads usando .map */}
      {tasks.map((t) => (
        <li key={t.id}> {/* key unica para cada elemento */}

          {/* texto principal de la tarea */}
          {t.texto}

          {/* si la tarea tiene fecha entonces la mostramos */}
          {t.fecha && <span> — Fecha: {t.fecha}</span>}

          {/* si la tarea tiene hora la mostramos */}
          {t.hora && <span> — Hora: {t.hora}</span>}

          {/* icono de completada */}
          {' '}✔

          {/* botn para eliminar la tarea usa la prop onDelet */}
          <button onClick={() => onDelete(t.id)}>Eliminar</button>
        </li>
      ))}
    </ul>
  );
}

export default CompletedList;
