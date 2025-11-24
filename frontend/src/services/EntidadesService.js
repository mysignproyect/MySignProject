import API_BASE_URL from "../config/api";

export async function getEntidades() {
  const response = await fetch(`${API_BASE_URL}/servicios`);
  if (!response.ok) throw new Error("Error al obtener entidades");
  return response.json();
}
