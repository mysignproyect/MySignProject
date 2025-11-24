<<<<<<< HEAD
import API_BASE_URL from "../config/api";

export async function getInterpretes() {
  const response = await fetch(`${API_BASE_URL}/interpretes`);
  if (!response.ok) throw new Error("Error al obtener intérpretes");
  return response.json();
}
=======
// services/interpretesService.js
import API_BASE_URL from "../config/api.js";

/**
 * Servicio para interactuar con el endpoint de intérpretes de la API My Sign
 */

/**
 * Obtiene todos los intérpretes o filtrados por parámetros
 * @param {Object} filtros - Objeto con filtros opcionales
 * @param {string} filtros.especialidad - Filtrar por especialidad (Médica, Legal, Educativa, Empresarial, Eventos)
 * @param {string} filtros.zona - Filtrar por zona de cobertura (Centro, Norte, Sur, Oriente, Occidente)
 * @param {string} filtros.disponibilidad - Filtrar por tipo de disponibilidad
 * @param {string} filtros.sort_by - Ordenar por campo (nombre, experiencia)
 * @param {string} filtros.order - Orden (asc, desc)
 * @param {number} filtros.page - Número de página para paginación
 * @param {number} filtros.limit - Cantidad de resultados por página
 * @returns {Promise<Array>} Lista de intérpretes
 */
export const obtenerInterpretes = async (filtros = {}) => {
  try {
    // Construir parámetros de consulta
    const params = new URLSearchParams();
    
    if (filtros.especialidad) params.append("especialidad", filtros.especialidad);
    if (filtros.zona) params.append("zona", filtros.zona);
    if (filtros.disponibilidad) params.append("disponibilidad", filtros.disponibilidad);
    if (filtros.sort_by) params.append("sort_by", filtros.sort_by);
    if (filtros.order) params.append("order", filtros.order);
    if (filtros.page) params.append("page", filtros.page);
    if (filtros.limit) params.append("limit", filtros.limit);

    const url = `${API_BASE_URL}/interpretes${params.toString() ? '?' + params.toString() : ''}`;
    
    console.log("🔗 URL de la petición:", url); // Debug
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors' // Importante para CORS
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error ${response.status}: ${errorText || response.statusText}`);
    }
    
    const data = await response.json();
    console.log("✅ Datos recibidos:", data); // Debug
    return data;
  } catch (error) {
    console.error("❌ Error al obtener intérpretes:", error);
    throw error;
  }
};

/**
 * Obtiene un intérprete por su ID
 * @param {string} interpreteId - ID del intérprete
 * @returns {Promise<Object>} Datos del intérprete
 */
export const obtenerInterpretePorId = async (interpreteId) => {
  try {
    const url = `${API_BASE_URL}/interpretes/${interpreteId}`;
    console.log("🔗 Obteniendo intérprete:", url);
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Intérprete no encontrado");
      }
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`❌ Error al obtener intérprete ${interpreteId}:`, error);
    throw error;
  }
};

/**
 * Obtiene intérpretes por especialidad
 * @param {string} especialidad - Especialidad a filtrar
 * @param {Object} opciones - Opciones adicionales (sort_by, order, page, limit)
 * @returns {Promise<Array>} Lista de intérpretes
 */
export const obtenerInterpretesPorEspecialidad = async (especialidad, opciones = {}) => {
  try {
    const params = new URLSearchParams();
    
    if (opciones.sort_by) params.append("sort_by", opciones.sort_by);
    if (opciones.order) params.append("order", opciones.order);
    if (opciones.page) params.append("page", opciones.page);
    if (opciones.limit) params.append("limit", opciones.limit);

    const url = `${API_BASE_URL}/interpretes/especialidad/${especialidad}${params.toString() ? '?' + params.toString() : ''}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`❌ Error al obtener intérpretes de especialidad ${especialidad}:`, error);
    throw error;
  }
};

/**
 * Obtiene intérpretes por zona de cobertura
 * @param {string} zona - Zona a filtrar
 * @param {Object} opciones - Opciones adicionales (especialidad, sort_by, order, page, limit)
 * @returns {Promise<Array>} Lista de intérpretes
 */
export const obtenerInterpretesPorZona = async (zona, opciones = {}) => {
  try {
    const params = new URLSearchParams();
    
    if (opciones.especialidad) params.append("especialidad", opciones.especialidad);
    if (opciones.sort_by) params.append("sort_by", opciones.sort_by);
    if (opciones.order) params.append("order", opciones.order);
    if (opciones.page) params.append("page", opciones.page);
    if (opciones.limit) params.append("limit", opciones.limit);

    const url = `${API_BASE_URL}/interpretes/zona/${zona}${params.toString() ? '?' + params.toString() : ''}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`❌ Error al obtener intérpretes de zona ${zona}:`, error);
    throw error;
  }
};

/**
 * Obtiene intérpretes por disponibilidad
 * @param {string} tipo - Tipo de disponibilidad (inmediata, tiempo_completo, por_horas, fines_semana)
 * @param {Object} opciones - Opciones adicionales (especialidad, zona, sort_by, order, page, limit)
 * @returns {Promise<Array>} Lista de intérpretes
 */
export const obtenerInterpretesPorDisponibilidad = async (tipo, opciones = {}) => {
  try {
    const params = new URLSearchParams();
    params.append("tipo", tipo);
    
    if (opciones.especialidad) params.append("especialidad", opciones.especialidad);
    if (opciones.zona) params.append("zona", opciones.zona);
    if (opciones.sort_by) params.append("sort_by", opciones.sort_by);
    if (opciones.order) params.append("order", opciones.order);
    if (opciones.page) params.append("page", opciones.page);
    if (opciones.limit) params.append("limit", opciones.limit);

    const url = `${API_BASE_URL}/interpretes/disponibilidad?${params.toString()}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors'
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`❌ Error al obtener intérpretes con disponibilidad ${tipo}:`, error);
    throw error;
  }
};

// Exportar valores constantes para usar en componentes
export const ESPECIALIDADES = [
  "Médica",
  "Legal",
  "Educativa",
  "Empresarial",
  "Eventos"
];

export const ZONAS = [
  "Centro",
  "Norte",
  "Sur",
  "Oriente",
  "Occidente"
];

export const TIPOS_DISPONIBILIDAD = [
  "inmediata",
  "tiempo_completo",
  "por_horas",
  "fines_semana"
];
>>>>>>> 4426972ac95bbef5d30173c6d608ac32daa0d008
