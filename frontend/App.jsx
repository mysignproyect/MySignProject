import Navbar from "./components/Nav";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 p-6">
        <h1 className="text-2xl font-bold">Página Principal</h1>
        <p>Contenido de la Home</p>
      </main>
    </div>
  );
}
