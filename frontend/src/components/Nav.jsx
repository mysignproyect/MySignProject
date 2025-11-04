import { useState } from "react";
import "../assets/css/Nav.css";
import logo_nom from "../assets/img/nombre_proyecto.JPG";
import titulo_gif from "../assets/gif/titulo.gif";
import { Link } from "react-router-dom";

export default function Nav() {
  const [search, setSearch] = useState("");
  const [showGif, setShowGif] = useState(false);

  return (
    <nav id="nav">
        <div id="nav_info"onMouseEnter={() => setShowGif(true)} onMouseLeave={() => setShowGif(false)}>
            <Link to="/" id="info_servicio_button_link">
               <span id="nav_info_name">MY SIGN</span>
            </Link>
            <img id="nav_info_img" src={logo_nom} alt="Logo de proyecto" /> 
            {showGif && (
              <div className="gif-container">
                <img 
                  src={titulo_gif} 
                  className="hover-gif"
                />
              </div>
            )}    
        </div>
        <div id="buscador">
            <div className="buscador_input">
                <input 
                    type="text" 
                    placeholder="Búsqueda..." 
                    value={search} 
                    onChange={(e) => {
                        setSearch(e.target.value);
                    }}
                    id="nav_input"
                />
                {search && (
                    <button 
                        onClick={() => {
                            setSearch("");
                        }} 
                        className="nav_boton_cerrar"
                    >
                        ✕
                    </button>
                )}
            </div>
        </div>
    </nav>
  );
}