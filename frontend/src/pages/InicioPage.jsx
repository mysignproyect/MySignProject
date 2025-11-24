import Nav from "../components/Nav";
import "../assets/css/InicioPage.css";
import Servicios from "../components/Servicios";
import "../assets/css/Gif.css";
import Footer from "../components/FooterDeLaPagina";
import gif_SN from "../assets/gif/Quien_somos.gif";
import gif_Servicios from "../assets/gif/Servicios.gif";
import { useState } from "react";

export default function InicioPage() {
 const [search, setSearch] = useState("");
 const [showServiciosGif, setShowServiciosGif] = useState(false);
  return (
    <>
      <Nav />
      <main>
        <div id="container_info_nosotros">
            <section id="sobreNosotros">
              <h1>Sobre Nosotros</h1>
              <p>Una aplicación web que conecta a la comunidad sorda de Medellín con 
                servicios accesibles, intérpretes de Lengua de Señas Colombiana 
                y un sistema de emergencias inclusivo.</p>
            </section>
            <article id="img_nosotros">
              <img src={gif_SN} alt="Imagen sobre nosotros" id="Img" />
            </article>
        </div>
        
        <h1 
          onMouseEnter={() => setShowServiciosGif(true)} 
          onMouseLeave={() => setShowServiciosGif(false)}
          id="titulo_servicios"
        >
          Servicios
        </h1>
        {showServiciosGif && (
          <div className="gif-container servicios">
            <img 
              src={gif_Servicios} 
              className="hover-gif"
            />
          </div>
        )} 
    
        <Servicios />
      </main>
      <Footer />
    </>
  );
}