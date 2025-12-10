import React, { useEffect, useState } from "react";
import { api } from "../api/client";

const StatusBadge = ({ status }) => {
    const styles = {
    new: "bg-blue-50 text-blue-700 border-blue-200",
    approved: "bg-green-50 text-green-700 border-green-200",
    rejected: "bg-red-50 text-red-700 border-red-200",
    sent: "bg-gray-100 text-gray-600 border-gray-200",
    responded: "bg-purple-50 text-purple-700 border-purple-200",
  };

  const labels = {
    new: "Новая",
    approved: "Одобрено",
    rejected: "Отказ",
    sent: "Отправлено",
    responded: "Ответили",
  };

  return (
    <span
      className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${
        styles[status] || styles.new
      }`}
    >
      {labels[status] || status}
    </span>
  );
};

export const Dashboard = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    const res = await api.getTopCompanies();
    if (res.status === "success") setCompanies(res.data);
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Компании (Топ-20)</h2>
      {loading ? <div>Загрузка...</div> : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 font-semibold">Компания</th>
                <th className="px-6 py-4 font-semibold">Скор</th>
                <th className="px-6 py-4 font-semibold">Статус</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {companies.map((company) => (
                <tr key={company.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-bold">{company.name}</td>
                  <td className="px-6 py-4">{company.score}</td>
                  <td className="px-6 py-4"><StatusBadge status={company.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};