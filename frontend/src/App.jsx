import { Routes, Route } from "react-router-dom";
import Inicio from "./pages/InicioPage";
import InterpretesPage from "./pages/InterpretesPage";
import EntidadesPage from "./pages/EntidadesPage"

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />
      |<Route path="/interpretes" element={<InterpretesPage />} />
      <Route path="/entidades" element={<EntidadesPage />} />
    </Routes>
  );
}
