import React from "react";
import { BrowserRouter } from "react-router-dom";
import { Header } from "./components/Header";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
        <Header />
      </div>
    </BrowserRouter>
  );
}

export default App;
