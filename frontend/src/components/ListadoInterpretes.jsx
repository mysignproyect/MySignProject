import { useState } from "react";
import CardInterpretes from "./CardInterpretes";
import {
  getInterpretes,
  getPorZona,
  getPorEspecialidad
} from "../services/interpretesService";
import titulo_gif from "../assets/gif/titulo.gif";

export default function ListadoInterpretes() {
  const [vista, setVista] = useState("listado");
  const [fetchFn, setFetchFn] = useState(() => getInterpretes);
  const [filtroActivo, setFiltroActivo] = useState(false);

  const zonas = ["Centro", "Norte", "Sur", "Oriente", "Occidente"];
  const especialidades = ["Médica", "Legal", "Educativa", "Empresarial", "Eventos"];

  const mostrarFiltro = (tipo) => {
    if (tipo === "zona") setVista("zonas");
    else if (tipo === "especialidad") setVista("especialidades");
  };

  const seleccionarZona = (zona) => {
    setFetchFn(() => async () => await getPorZona(zona));
    setFiltroActivo(true);
    setVista("listado");
  };

  const seleccionarEspecialidad = (esp) => {
    setFetchFn(() => async () => await getPorEspecialidad(esp));
    setFiltroActivo(true);
    setVista("listado");
  };

  const volverAlListado = () => {
    setFetchFn(() => getInterpretes);
    setFiltroActivo(false);
    setVista("listado");
  };

  return (
     <div className="interpretes-container">
      {vista === "listado" && (
        <>
          {!filtroActivo && (
            <ul className="menu-filtros">
              <li onClick={() => mostrarFiltro("zona")}>Zona</li>
              <li onClick={() => mostrarFiltro("especialidad")}>Especialidad</li>
            </ul>
          )}
          <CardInterpretes
            fetchFunction={fetchFn}
            onVolver={volverAlListado}
            mostrarVolver={filtroActivo}
          />
        </>
      )}

      {vista === "zonas" && (
        <div className="tarjetas-filtro">
          {zonas.map((z) => (
            <div key={z} className="tarjeta" onClick={() => seleccionarZona(z)}>
              <img src={`/src/assets/gif/${z.toLowerCase()}.gif`} className="gif_filtro" alt={z} />
              <p>{z}</p>
            </div>
          ))}
          <button onClick={volverAlListado} className="volver-btn">Volver</button>
        </div>
      )}

      {vista === "especialidades" && (
        <div className="tarjetas-filtro">
          {especialidades.map((e) => (
            <div key={e} className="tarjeta" onClick={() => seleccionarEspecialidad(e)}>
              <img src={`/src/assets/gif/${e.toLowerCase()}.gif`} className="gif_filtro" alt={e} />
              <p>{e}</p>
            </div>
          ))}
          <button onClick={volverAlListado} className="volver-btn">Volver</button>
        </div>
      )}
    </div>
  );
}
