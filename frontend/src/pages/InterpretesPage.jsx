import Nav from "../components/Nav";
import "../assets/css/InicioPage.css";
import ListadoInterpretes from "../components/ListadoInterpretes";
import Footer from "../components/FooterDeLaPagina";
import img_SN from "../assets/img/imagenSobreNosotros.jpeg";

export default function Interpretes() {
  return (
    <>
      <Nav />
      <main>
        <div id="container_info_nosotros">
            <section id="sobreNosotros">
              <h1>Directorio de interpretes</h1>
              <p>Busca intérpretes certificados en LSC según tu necesidad, zona y disponibilidad. 
                Accede a perfiles, experiencia y contacto directo.</p>
            </section>
            <article id="img_nosotros">
              <img src={img_SN} alt="Imagen sobre nosotros" id="Img" />
            </article>
        </div>
        <ListadoInterpretes />
      </main>
      <Footer />
    </>
  );
}