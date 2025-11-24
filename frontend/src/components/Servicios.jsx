import { useState } from "react";
import "../assets/css/Servicios.css";
import logo_serv_uno from "../assets/img/ServicioNumeroUno.jpeg";
import logo_serv_dos from "../assets/img/ServicioNumeroDos.jpeg";
import gif_Interpretes from "../assets/gif/interpretes.gif";
import gif_Entidades from "../assets/gif/Entidades.gif";
import { Link } from "react-router-dom";
import "../assets/css/Gif.css";


export default function Servicios() {
  const [search, setSearch] = useState("");
   const [showEntidadesGif, setShowEntidadesGif] = useState(false);
   const [showInterpretesGif, seShowInterpretesGif] = useState(false);
  return (
    <div id="container_servicios">
        <section 
            onMouseEnter={() => seShowInterpretesGif(true)} 
            onMouseLeave={() => seShowInterpretesGif(false)}
            id="servicio_numero_uno">
            <div id="img_servicio_uno">
                <img src={logo_serv_uno} alt="" />
            </div>
            
            <div id="info_servicio_uno">
                <p>Accede a un directorio de intérpretes de Lengua de Señas Colombiana, filtrados por especialidad, disponibilidad y zona.</p>
                <Link to="/interpretes" id="info_servicio_button_link">
                  <button id="info_servicio_button">Encontrar intérprete</button>
                </Link>
            </div>
        </section>
        {showInterpretesGif && (
          <div className="gif-container interprete">
            <img 
              src={gif_Interpretes} 
              className="hover-gif"
            />
          </div>
        )}
        
        <section
              onMouseEnter={() => setShowEntidadesGif(true)} 
              onMouseLeave={() => setShowEntidadesGif(false)}
              id="servicio_numero_dos">
            <div id="img_servicio_dos">
                <img src={logo_serv_dos} alt="" />   
            </div>
            
            <div id="info_servicio_dos">
                <h2>Contactarse con entidad</h2>
                <p>Ubica hospitales y centros de salud accesibles en Medellín, con información de contacto directo y servicios inclusivos.</p>
                 <Link to="/entidades" id="info_servicio_button_link">
                   <button id="info_servicio_button">Contactarse con entidad</button>
                 </Link>
            </div>
        </section>
        {showEntidadesGif && (
          <div className="gif-container entidades">
            <img 
              src={gif_Entidades} 
              className="hover-gif"
            />
          </div>
        )}
        
    </div>
  );
}