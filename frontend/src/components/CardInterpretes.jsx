import { useEffect, useState } from "react";

export default function CardInterpretes({ fetchFunction, onVolver, mostrarVolver }) {
  const [interpretes, setInterpretes] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      setCargando(true);
      try {
        const data = await fetchFunction(); // Llama al servicio recibido
        setInterpretes(data || []);
      } catch (error) {
        console.error("Error cargando intérpretes:", error);
        setInterpretes([]);
      } finally {
        setCargando(false);
      }
    };

    cargar();
  }, [fetchFunction]);

  return (
    <div id="interpretes">
      {mostrarVolver && (
        <button onClick={onVolver} className="volver-btn">
          ← Volver
        </button>
      )}

      {cargando ? (
        <p>Cargando intérpretes...</p>
      ) : interpretes.length > 0 ? (
        interpretes.map((int) => (
          <div key={int.id} className="interprete-card">
            <img
              src={int.foto || "https://via.placeholder.com/200x200.png?text=Sin+Foto"}
              alt={int.nombre}
            />
            <ul>
              <li><strong>{int.nombre}</strong></li>
              <li>Especialidad: {int.especialidades?.join(", ")}</li>
              <li>Zonas: {int.zonas_cobertura?.join(", ")}</li>
              <li>Disponibilidad: {int.disponibilidad}</li>
              <li>Tel: {int.telefono}</li>
              <li>Correo: {int.email}</li>
            </ul>
          </div>
        ))
      ) : (
        <p>No hay intérpretes disponibles.</p>
      )}
    </div>
  );
}
