const API_URL = "http://127.0.0.1:8000/api/interpretes";

export async function getInterpretes() {
  const res = await fetch(API_URL);
  return await res.json();
}

export async function getPorZona(zona) {
  const res = await fetch(`${API_URL}/zona/${zona}`);
  return await res.json();
}

export async function getPorEspecialidad(especialidad) {
  const res = await fetch(`${API_URL}/especialidad/${especialidad}`);
  return await res.json();
}
