import { useState } from "react";
import "../assets/css/InterpretesYServicios.css";
import tituloGif from '../assets/gif/titulo.gif';
import Gif from '../assets/gif/perro.gif';


export default function ListadoEntidades() {
    const [categoria, setCategoria] = useState("");
    const [zona, setZona] = useState("");
    const [accesibilidad, setAccesibilidad] = useState("");

    const [gifState, setGifState] = useState({
        visible: false,
        src: '',
        x: 0,
        y: 0
    });

    const entidades = [
        {id: 1, nombre: "Alcaldía de Medellín", descripcion: "Entidad gubernamental local.", categoria:"gobierno", zona:"centro", accesibilidad:"rampa"},
        {id: 2, nombre: "Gobernación de Antioquia", descripcion: "Administración departamental.", categoria:"gobierno", zona:"centro", accesibilidad:"interpretes"},
        {id: 3, nombre: "Secretaría de Inclusión Social", descripcion: "Programas para la comunidad.", categoria:"gobierno", zona:"sur", accesibilidad:"braille"},
        {id: 4, nombre: "Metro de Medellín", descripcion: "Sistema de transporte público accesible.", categoria:"transporte", zona:"centro", accesibilidad:"todos"},
        {id: 5, nombre: "Hospital General", descripcion: "Servicios de salud con accesibilidad.", categoria:"salud", zona:"norte", accesibilidad:"rampa"},
        {id: 6, nombre: "Universidad de Antioquia", descripcion: "Institución de educación superior.", categoria:"educacion", zona:"occidente", accesibilidad:"interpretes"},
    ]; 

    const entidadesFiltradas = entidades.filter((e) =>
        (categoria ? e.categoria === categoria : true) &&
        (zona ? e.zona === zona : true) &&
        (accesibilidad ? e.accesibilidad === accesibilidad : true)
    ); 
    const gifUrls = {
        Especialidades: tituloGif,
        Zona: Gif,
        Accesibilidad: tituloGif,
        Médica: tituloGif,
        Legal: Gif,
        Educativa: tituloGif,
        Empresarial: Gif,
        Eventos: Gif,
        Centro: tituloGif,
        Norte: Gif,
        Sur: tituloGif,
        Oriente: Gif, 
        Occidente: Gif,
        rampa: tituloGif,
        interpretes: Gif,
        braille: tituloGif,
        todos: Gif
    };

    const handleMouseEnter = (e, key) => {
        const rect = e.target.getBoundingClientRect();
        
        const src = gifUrls[key] || tituloGif; 

        setGifState({
            visible: true,
            src: src, 
            x: rect.right + 15, 
            y: rect.top + window.scrollY 
        });
    };

    const handleMouseLeave = () => {
        setGifState({ ...gifState, visible: false });
    };
    

    return (
        <>
          <div className="entidades_interpretes_container">
              <section className="hero_interpretes_entidades">
                  <div className="hero-texto">

                      <div className="filtros">
                          <select 
                            value={categoria} 
                            onChange={(e)=>setCategoria(e.target.value)}
                            onMouseEnter={(e) => handleMouseEnter(e, categoria || 'Especialidades')} 
                            onMouseLeave={handleMouseLeave}
                          >
                              <option value="Especialidades">Especialidades</option>
                              <option value="Médica">Médica</option>
                              <option value="Legal">Legal</option>
                              <option value="Educativa">Educativa</option>
                              <option value="Empresarial">Empresarial</option>
                              <option value="Eventos">Eventos</option>
                          </select>


                          <select 
                            value={zona} 
                            onChange={(e)=>setZona(e.target.value)}
                            onMouseEnter={(e) => handleMouseEnter(e, zona || 'Zona')}
                            onMouseLeave={handleMouseLeave}
                          >
                              <option value="Zona">Zona</option>
                              <option value="Centro">Centro</option>
                              <option value="Norte">Norte</option>
                              <option value="Sur">Sur</option>
                              <option value="Oriente">Oriente</option>
                              <option value="Occidente">Occidente</option>
                          </select>

                           <select 
                           value={accesibilidad} 
                                onChange={(e)=>setAccesibilidad(e.target.value)}
                                onMouseEnter={(e) => handleMouseEnter(e, accesibilidad || 'rampa')}
                                onMouseLeave={handleMouseLeave}
                            >
                                <option value="Accesibilidad">Accesibilidad</option>
                                <option value="rampa">Rampa</option>
                                <option value="interpretes">Intérpretes</option>
                                <option value="braille">Señalética Braille</option>
                                <option value="todos">Total Accesibilidad</option>
                            </select>

                      </div>
                  </div>
              </section>

              {gifState.visible && gifState.src && (
                  <div 
                      className="gif-container" 
                      style={{ 
                          top: gifState.y, 
                          left: gifState.x,
                          position: 'absolute'
                      }}
                  >
                      <img src={gifState.src} alt="GIF de ayuda" className="hover-gif" />
                  </div>
              )}

              <section className="lista_interpretes_entidades">
                  <h2 className="titulo-lista">Lista de entidades</h2>

                  <div className="grid_interpretes_entidades">
                      {entidadesFiltradas.length > 0 ? (
                          entidadesFiltradas.map((entidad) => (
                              <div key={entidad.id} className="card_interpretes_entidad">
                                  <h3>{entidad.nombre}</h3>
                                  <p>
                                      <span role="img" aria-label="Especialidad">🏷️</span>
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
                              </div>
                          ))
                      ) : (
                          <p>No hay entidades que coincidan con los filtros seleccionados 😢</p>
                      )}
                  </div>
              </section>
          </div>

        </>
    );
}