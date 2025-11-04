import { useEffect, useState } from "react";
import "../assets/css/CardInterpretes.css";

export default function CardInterpretes({ fetchFunction, onVolver, mostrarVolver }) {
  const [interpretes, setInterpretes] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      setCargando(true);
      try {
        const data = await fetchFunction();
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
    <div id="interpretes" className="interpretes">
      {mostrarVolver && (
        <button onClick={onVolver} className="volver_btn">
          ← Volver
        </button>
      )}
        <div className="Interprete_card_general">
            {cargando ? (
              <p>Cargando intérpretes...</p>
            ) : interpretes.length > 0 ? (
              interpretes.map((int) => (

                <div key={int.id} className="interprete_card">
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
    </div>
  );
}
