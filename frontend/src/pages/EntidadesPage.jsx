import Nav from "../components/Nav";
import "../assets/css/EntidadesPage.css"; // 🚨 ¡Tu CSS se mantiene!
import Footer from "../components/FooterDeLaPagina";
import img_SN from "../assets/img/imagenSobreNosotros.jpeg";
import { useState } from "react";

export default function EntidadesPage() {
    const [categoria, setCategoria] = useState("");
    const [zona, setZona] = useState("");
    const [accesibilidad, setAccesibilidad] = useState("");

    const entidades = [
        {id: 1, nombre: "Alcaldía de Medellín", descripcion: "Entidad gubernamental local.", categoria:"gobierno", zona:"centro", accesibilidad:"rampa"},
        {id: 2, nombre: "Gobernación de Antioquia", descripcion: "Administración departamental.", categoria:"gobierno", zona:"centro", accesibilidad:"interpretes"},
        {id: 3, nombre: "Secretaría de Inclusión Social", descripcion: "Programas para la comunidad.", categoria:"gobierno", zona:"sur", accesibilidad:"braille"},
        {id: 4, nombre: "Metro de Medellín", descripcion: "Sistema de transporte público accesible.", categoria:"transporte", zona:"centro", accesibilidad:"todos"},
        {id: 5, nombre: "Hospital General", descripcion: "Servicios de salud con accesibilidad.", categoria:"salud", zona:"norte", accesibilidad:"rampa"},
        {id: 6, nombre: "Universidad de Antioquia", descripcion: "Institución de educación superior.", categoria:"educacion", zona:"occidente", accesibilidad:"interpretes"},
    ]; //

    const entidadesFiltradas = entidades.filter((e) =>
        (categoria ? e.categoria === categoria : true) &&
        (zona ? e.zona === zona : true) &&
        (accesibilidad ? e.accesibilidad === accesibilidad : true)
    ); //


    return (
        <>
            <Nav/>

            <main className="entidades-container">
                <section className="hero-entidades">
                    <div className="hero-texto">
                        <h1>Contactarse con entidades</h1>
                        <p>
                            Accede a instituciones accesibles en Medellín y contáctalas fácilmente.
                        </p>

                        {/* SELECTORES DE FILTRO */}
                        <div className="filtros">
                            <select value={categoria} onChange={(e)=>setCategoria(e.target.value)}>
                                <option value="">Categoría</option>
                                <option value="salud">Salud</option>
                                <option value="educacion">Educación</option>
                                <option value="gobierno">Gobierno</option>
                                <option value="transporte">Transporte</option>
                            </select>

                            <select value={zona} onChange={(e)=>setZona(e.target.value)}>
                                <option value="">Zona</option>
                                <option value="centro">Centro</option>
                                <option value="norte">Norte</option>
                                <option value="sur">Sur</option>
                                <option value="occidente">Occidente</option>
                                {/* Nota: Agrega las zonas de tu mock data si faltan */}
                            </select>

                            <select value={accesibilidad} onChange={(e)=>setAccesibilidad(e.target.value)}>
                                <option value="">Accesibilidad</option>
                                <option value="rampa">Rampa</option>
                                <option value="interpretes">Intérpretes</option>
                                <option value="braille">Señalética Braille</option>
                                <option value="todos">Total Accesibilidad</option>
                                {/* Nota: Asegúrate de que los valores coincidan exactamente con la data hardcodeada (e.g., "rampa", "interpretes") */}
                            </select>
                        </div>
                    </div>

                    <div className="hero-img">
                        <img src={img_SN} alt="Imagen accesibilidad"/>
                    </div>
                </section>

                {/* LISTA DE ENTIDADES (Renderizado usando la data filtrada localmente) */}
                <section className="lista-entidades">
                    <h2 className="titulo-lista">Lista de Entidades</h2>

                    <div className="grid-entidades">
                        {entidadesFiltradas.length > 0 ? (
                            entidadesFiltradas.map((entidad) => (
                                <div key={entidad.id} className="card-entidad">
                                    <h3>{entidad.nombre}</h3>
                                    <p>
                                        <span role="img" aria-label="Categoría">🏷️</span>
                                        Categoría: {entidad.categoria.charAt(0).toUpperCase() + entidad.categoria.slice(1)}
                                    </p>
                                    <p>
                                        <span role="img" aria-label="Zona">📍</span>
                                        Zona: {entidad.zona.charAt(0).toUpperCase() + entidad.zona.slice(1)}
                                    </p>
                                    <p>
                                        <span role="img" aria-label="Accesibilidad">♿</span>
                                        Accesibilidad: {entidad.accesibilidad}
                                    </p>
                                    <p>{entidad.descripcion}</p>
                                    <button className="btn-ver">Ver más</button>
                                </div>
                            ))
                        ) : (
                            <p>No hay entidades que coincidan con los filtros seleccionados 😢</p>
                        )}
                    </div>
                </section>
            </main>

            <Footer/>
        </>
    );
}