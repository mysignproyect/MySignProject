import { useState, useEffect } from "react";
import { getInterpretes } from "../services/interpretesService";
import "../assets/css/InterpretesYServicios.css";

export default function ListadoInterpretes() {
  const [especialidades, setEspecialidades] = useState("");
  const [zona, setZona] = useState("");

  const [interpretes, setInterpretes] = useState([]);

  useEffect(() => {
    getInterpretes()
      .then(setInterpretes)
      .catch((err) => console.error("Error cargando intérpretes:", err));
  }, []);

  const interpretesFiltrados = interpretes.filter(
    (i) =>
      (especialidades
        ? i.especialidades.includes(especialidades)
        : true) &&
      (zona ? i.zonas_cobertura.includes(zona) : true)
  );


  return (
    <div className="entidades_interpretes_container">
      <section className="hero_interpretes_entidades">
        <div className="hero-texto">
          <div className="filtros">
            <select
              value={especialidades}
              onChange={(e) => setEspecialidades(e.target.value)}
            >
              <option value="">Todas las especialidades</option>
              <option value="Médica">Médica</option>
              <option value="Legal">Legal</option>
              <option value="Educativa">Educativa</option>
              <option value="Empresarial">Empresarial</option>
              <option value="Eventos">Eventos</option>
            </select>

            <select
              value={zona}
              onChange={(e) => setZona(e.target.value)}
            >
              <option value="">Todas las zonas</option>
              <option value="Centro">Centro</option>
              <option value="Norte">Norte</option>
              <option value="Sur">Sur</option>
              <option value="Oriente">Oriente</option>
              <option value="Occidente">Occidente</option>
            </select>
          </div>
        </div>
      </section>

      <section className="lista_interpretes_entidades">
        <h2 className="titulo-lista">Lista de Intérpretes</h2>

        <div className="grid_interpretes_entidades">
          {interpretesFiltrados.length > 0 ? (
            interpretesFiltrados.map((i) => (
              <div key={i.id} className="card_interpretes_entidad">
                <h3>{i.nombre}</h3>
                <p>🏷️ Especialidades: {i.especialidades.join(", ")}</p>
                <p>📍 Zonas: {i.zonas_cobertura.join(", ")}</p>
                <p>📞 Teléfono: {i.telefono}</p>
                <p>📱 WhatsApp: {i.whatsapp || "No disponible"}</p>
              </div>
            ))
          ) : (
            <p>No hay intérpretes que coincidan con los filtros seleccionados 😢</p>
          )}
        </div>
      </section>
    </div>
  );
}