import React from "react";
import { NavLink } from "react-router-dom";
import { Briefcase } from "lucide-react";

export const Header = () => {
  const linkClass = ({ isActive }) =>
    isActive
      ? "text-blue-600 font-bold border-b-2 border-blue-600 pb-4 -mb-4"
      : "text-gray-600 hover:text-blue-600 font-medium pb-4 -mb-4 border-b-2 border-transparent hover:border-gray-200 transition-all";

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between sticky top-0 z-10 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white shadow-lg shadow-blue-200">
          <Briefcase size={18} strokeWidth={3} />
        </div>
        <h1 className="text-xl font-bold text-gray-800 tracking-tight">
          Поиск партнёров
        </h1>
      </div>

      <nav className="flex gap-8 text-sm">
        <NavLink to="/" className={linkClass}>
          Все компании
        </NavLink>
        <NavLink to="/approved" className={linkClass}>
          Готовые к отправке
        </NavLink>
      </nav>
    </header>
  );
};
