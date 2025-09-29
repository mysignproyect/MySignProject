import { useState } from "react";
import { X } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { Button } from "./ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "./ui/dropdown-menu";

import { useState } from "react";
import { X } from "lucide-react";

export default function Nav() {
  const [search, setSearch] = useState("");

  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
      {/* Logo + Iconos */}
      <div className="flex items-center gap-3">
        <span className="font-bold text-lg">MY SIGN</span>
        <div className="flex gap-2 text-2xl">
          <span>☝️</span>
          <span>👍</span>
          <span>✌️</span>
          <span>👉</span>
          <span>👎</span>
        </div>
      </div>

      {/* Barra de búsqueda */}
      <div className="relative">
        <input
          type="text"
          placeholder="Búsqueda..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded-full px-4 py-1 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        {search && (
          <button
            onClick={() => setSearch("")}
            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
          >
            <X size={16} />
          </button>
        )}
      </div>
    </nav>
  );
}
