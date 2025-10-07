import Nav from "../components/Nav";
import "../assets/css/InicioPage.css";
import Servicios from "../components/Servicios";
import Footer from "../components/FooterDeLaPagina";
import img_SN from "../assets/img/imagenSobreNosotros.jpeg";


export default function InicioPage() {
  return (
    <body>
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
              <img src={img_SN} alt="" id="Img" />
            </article>
        </div>
        <h1 id="titulo_servicios">Servicios</h1>
        <Servicios />
      </main>
      <Footer />
    </body>
  );
}
