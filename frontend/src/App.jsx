import { Routes, Route } from "react-router-dom";
import Inicio from "./pages/InicioPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />
    </Routes>
  );
}
