import "../assets/css/Servicios.css";
import gif_Interpretes from "../assets/gif/Interpretes.gif";
import gif_Entidades from "../assets/gif/Entidades.gif";
import { Link } from "react-router-dom";
import "../assets/css/Gif.css";


export default function Servicios() {

  return (
    <div id="container_servicios">
        <section id="servicio_numero_uno">
            <div id="img_servicio_uno">
                <img src={gif_Interpretes} alt="" />
            </div>
            
            <div id="info_servicio_uno">
                <p>Accede a un directorio de intérpretes de Lengua de Señas Colombiana, filtrados por especialidad, disponibilidad y zona.</p>
                <Link to="/interpretes" id="info_servicio_button_link">
                  <button id="info_servicio_button">Encontrar intérprete</button>
                </Link>
            </div>
        </section>
        <section id="servicio_numero_dos">
            <div id="img_servicio_dos">
                <img src={gif_Entidades} alt="" />   
            </div>
            
            <div id="info_servicio_dos">
                <h2>Contactarse con entidad</h2>
                <p>Ubica hospitales y centros de salud accesibles en Medellín, con información de contacto directo y servicios inclusivos.</p>
                 <Link to="/entidades" id="info_servicio_button_link">
                  <button id="info_servicio_button">Contactarse con entidad</button>
                 </Link>
            </div>
        </section>
        
        
    </div>
  );
}