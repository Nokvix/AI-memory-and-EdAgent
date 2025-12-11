import React from "react";
import { BrowserRouter, Routes, Route  } from "react-router-dom";
import { Header } from "./components/Header";
import { Dashboard } from "./pages/Dashboard";
import { CompanyDetail } from "./pages/CompanyDetail";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
        <Header />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/company/:id" element={<CompanyDetail />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
