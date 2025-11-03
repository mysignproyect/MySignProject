import { useState } from "react";
import "../assets/css/Nav.css";
import logo_nom from "../assets/img/nombre_proyecto.JPG";

export default function Nav() {
  const [search, setSearch] = useState("");

  return (
    <nav id="nav">
        <div id="nav_info">
            <span id="nav_info_name">MY SIGN</span>
            <img id="nav_info_img" src={logo_nom} alt="Logo de proyecto" />      
        </div>
        <div id="buscador">
            <div className="buscador_input">
                <input type="text" placeholder="Búsqueda..." value={search} onChange={(e) => setSearch(e.target.value)} id="nav_input"/>
                {search && (
                    <button onClick={() => setSearch("")} className="nav_boton_cerrar">X</button>
                )}
            </div>
        </div>
    </nav>
  );
}
