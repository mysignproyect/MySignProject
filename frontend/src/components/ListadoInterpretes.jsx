import { useState, useEffect } from "react";
import { getInterpretes } from "../services/interpretesService";
import "../assets/css/InterpretesYServicios.css";
import "../assets/css/Gif.css";
import tituloGif from "../assets/gif/titulo.gif";
import Gif from "../assets/gif/perro.gif";

export default function ListadoInterpretes() {
  const [especialidades, setEspecialidades] = useState("");
  const [zona, setZona] = useState("");

  const [gifState, setGifState] = useState({
    visible: false,
    src: "",
    x: 0,
    y: 0,
  });

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

  const gifUrls = {
    Especialidades: tituloGif,
    Zona: Gif,
    Médica: tituloGif,
    Legal: Gif,
    Educativa: tituloGif,
    Empresarial: Gif,
    Eventos: Gif,
    Centro: tituloGif,
    Norte: Gif,
    Sur: tituloGif,
    Oriente: Gif,
    Occidente: Gif,
  };

  const handleMouseEnter = (e, key) => {
    const rect = e.target.getBoundingClientRect();
    const src = gifUrls[key] || tituloGif;
    setGifState({
      visible: true,
      src: src,
      x: rect.right + 15,
      y: rect.top + window.scrollY,
    });
  };

  const handleMouseLeave = () => {
    setGifState({ ...gifState, visible: false });
  };

  return (
    <div className="entidades_interpretes_container">
      <section className="hero_interpretes_entidades">
        <div className="hero-texto">
          <div className="filtros">
            <select
              value={especialidades}
              onChange={(e) => setEspecialidades(e.target.value)}
              onMouseEnter={(e) =>
                handleMouseEnter(e, especialidades || "Especialidades")
              }
              onMouseLeave={handleMouseLeave}
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
              onMouseEnter={(e) => handleMouseEnter(e, zona || "Zona")}
              onMouseLeave={handleMouseLeave}
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

      {gifState.visible && gifState.src && (
        <div
          className="gif-container"
          style={{
            top: gifState.y,
            left: gifState.x,
            position: "absolute",
          }}
        >
          <img src={gifState.src} alt="GIF de ayuda" className="hover-gif" />
        </div>
      )}

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