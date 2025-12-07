// Importamos useState para manejar estados dentro del componente
import { useState } from "react";

// Componente TaskForm recibe como PROP la función onAdd 
function TaskForm({ onAdd }) {

  // Estados locales para almacenar lo que el usuario escribe
  const [texto, setTexto] = useState(""); // descripcion de la tarea
  const [fecha, setFecha] = useState(""); // fecha opcional
  const [hora, setHora] = useState("");   // hora opcional

  // Función que se ejecuta cuando se envía el formulario
  const handleSubmit = (e) => {
    e.preventDefault(); // evita que la pagina se recargue automáticamente

    // Expresión regular que filtra solamente letras
    const soloLetras = texto.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ]/g, "");

    // Validacion: minimo 3 letras reales
    if (soloLetras.length < 3) {
      alert("La descripción debe tener al menos 3 letras.");
      return; // detenemos la ejecucion si no cumple
    }

    // Validacion: maximo 150 caracteres
    if (texto.length > 150) {
      alert("Máximo 150 caracteres.");
      return;
    }

    // Llamamos a la funcion que viene desde App.jsx
    // Si fecha u hora estan vacios se  envia null
    onAdd(texto, fecha || null, hora || null);

    // Limpiamos los campos del formulario
    setTexto("");
    setFecha("");
    setHora("");
  };

  return (
    // Formulario que llama a handleSubmit cuando se envia
    <form onSubmit={handleSubmit} className="task-form">

      {/* Campo de texto para la descripcion */}
      <input
        type="text"
        placeholder="Descripción"
        value={texto}               // el estado controla el valor
        onChange={(e) => setTexto(e.target.value)} // actualiza el estado
      />

      {/* Selector de fecha (opcional) */}
      <input
        type="date"
        value={fecha}
        onChange={(e) => setFecha(e.target.value)}
      />

      {/* Selector de hora (opcional) */}
      <input
        type="time"
        value={hora}
        onChange={(e) => setHora(e.target.value)}
      />

      {/* Botón que activa el submit del formulario */}
      <button type="submit">Agregar</button>
    </form>
  );
}

// Exportamos el componente para que pueda usarse en App.jsx
export default TaskForm;
