import API_BASE_URL from "../config/api";

export async function getInterpretes() {
  const response = await fetch(`${API_BASE_URL}/interpretes`);
  if (!response.ok) throw new Error("Error al obtener intérpretes");
  return response.json();
}
