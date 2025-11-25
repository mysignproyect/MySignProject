import { useState, useEffect } from "react";
import { getEntidades } from "../services/EntidadesService";
import "../assets/css/InterpretesYServicios.css";

export default function ListadoEntidades() {
  const [categoria, setCategoria] = useState("");
  const [zona, setZona] = useState("");
  const [accesibilidad, setAccesibilidad] = useState("");

  const [entidades, setEntidades] = useState([]);

  useEffect(() => {
    getEntidades()
      .then(setEntidades)
      .catch((err) => console.error("Error cargando entidades:", err));
  }, []);

  const entidadesFiltradas = entidades.filter(
    (e) =>
      (categoria ? e.categoria === categoria : true) &&
      (zona ? e.zona === zona : true) &&
      (accesibilidad ? e.accesibilidad === accesibilidad : true)
  );


  return (
    <div className="entidades_interpretes_container">
      <section className="hero_interpretes_entidades">
        <div className="hero-texto">
          <div className="filtros">
            <select
              value={categoria}
              onChange={(e) => setCategoria(e.target.value)}
            >
              <option value="">Todas las categorías</option>
              <option value="Salud">Salud</option>
              <option value="Educación">Educación</option>
              <option value="Gobierno">Gobierno</option>
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

            <select
              value={accesibilidad}
              onChange={(e) => setAccesibilidad(e.target.value)}
            >
              <option value="">Todas</option>
              <option value="Rampas">Rampas</option>
              <option value="Intérpretes">Intérpretes</option>
              <option value="Braille">Braille</option>
              <option value="Todos">Total Accesibilidad</option>
            </select>
          </div>
        </div>
      </section>

      <section className="lista_interpretes_entidades">
        <h2 className="titulo-lista">Lista de entidades</h2>

        <div className="grid_interpretes_entidades">
          {entidadesFiltradas.length > 0 ? (
            entidadesFiltradas.map((entidad) => (
              <div key={entidad.id} className="card_interpretes_entidad">
                <h3>{entidad.nombre}</h3>
                <p>
                  🏷️ Categoría: {entidad.categoria}
                </p>
                <p>
                  📍 Zona: {entidad.zona}
                </p>
                <p>
                  ♿ Accesibilidad: {entidad.caracteristicas_accesibilidad?.join(", ")}
                </p>
                <p>{entidad.descripcion}</p>
              </div>
            ))
          ) : (
            <p>No hay entidades que coincidan con los filtros seleccionados 😢</p>
          )}
        </div>
      </section>
    </div>
  );
}