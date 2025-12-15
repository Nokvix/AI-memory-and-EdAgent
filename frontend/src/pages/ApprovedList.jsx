import React, { useState, useEffect } from "react";
import { api } from "../api/client";
import { Send, CheckCircle } from "lucide-react";

export const ApprovedList = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const res = await api.getTopCompanies();
      if (res.status === "success") {
        const approved = res.data.filter(
          (c) => c.status === "approved" || c.status === "sent"
        );
        setCompanies(approved);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (id) => {
    if (!window.confirm("Действительно отправить письмо?")) return;

    await api.sendEmail(id);
    alert("Письмо успешно отправлено!");
    loadData();
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Готовые к отправке</h2>
        <p className="text-gray-500 mt-1">
          Компании, для которых письма были одобрены
        </p>
      </div>

      {loading ? (
        <div className="text-center py-10">Загрузка...</div>
      ) : (
        <div className="grid gap-4">
          {companies.length === 0 && (
            <div className="text-center py-12 bg-white rounded-xl border border-dashed border-gray-300 text-gray-400">
              Список пуст. Одобрите письма на главной странице.
            </div>
          )}

          {companies.map((company) => (
            <div
              key={company.id}
              className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between"
            >
              <div>
                <div className="flex items-center gap-3">
                  <h3 className="font-bold text-lg text-gray-800">
                    {company.name}
                  </h3>
                  {company.status === "sent" && (
                    <span className="bg-green-100 text-green-700 text-xs px-2 py-0.5 rounded-full flex items-center gap-1">
                      <CheckCircle size={12} /> Отправлено
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  HR-менеджер: hr@
                  {company.url?.split("hh.ru")[1] || "example.com"}
                </p>
              </div>

              {company.status !== "sent" ? (
                <button
                  onClick={() => handleSend(company.id)}
                  className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-sm shadow-blue-200"
                >
                  <Send size={16} /> Отправить
                </button>
              ) : (
                <button
                  disabled
                  className="text-gray-400 px-4 py-2 text-sm font-medium cursor-not-allowed"
                >
                  Письмо ушло
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
