import Nav from "../components/Nav";
import "../assets/css/InicioPage.css";
import Entidades from "../components/ListadoEntidades";
import Footer from "../components/FooterDeLaPagina";
import gif_Entidades from "../assets/gif/Entidades.gif";

export default function EntidadesPage() {
    return (
        <>
            <Nav/>
            <main>
                <div id="container_info_nosotros">
                    <section id="sobreNosotros">
                        <h1>Contactarse con entidades</h1>
                        <p>Accede a instituciones accesibles en Medellín y contáctalas fácilmente. 
                        Encuentra datos actualizados, horarios y opciones de atención inclusiva.</p>
                    </section>
                    <article id="img_nosotros">
                        <img src={gif_Entidades} alt="Imagen sobre nosotros" id="Img" />
                    </article>
                </div>
                <Entidades />
            </main>
            <Footer/>
        </>
    );
}