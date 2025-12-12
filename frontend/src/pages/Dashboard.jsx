import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { Link } from "react-router-dom";
import { ExternalLink, Mail, Filter } from "lucide-react";

const StatusBadge = ({ status }) => {
  const styles = {
    new: "bg-blue-50 text-blue-700 border-blue-200",
    approved: "bg-green-50 text-green-700 border-green-200",
    rejected: "bg-red-50 text-red-700 border-red-200",
    sent: "bg-gray-100 text-gray-600 border-gray-200",
    responded: "bg-purple-50 text-purple-700 border-purple-200",
  };

  // Словарь для перевода
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
  const [selectedCompany, setSelectedCompany] = useState(null);

  const [filters, setFilters] = useState({
    status: "",
    industry: "",
  });

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    setLoading(true);
    let res;

    if (!filters.status && !filters.industry) {
      res = await api.getTopCompanies();
    } else {
      res = await api.getCompanies(filters);
    }

    if (res.status === "success") {
      setCompanies(res.data);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Компании</h2>
          <p className="text-gray-500 mt-1">
            {filters.status || filters.industry
              ? "Результаты поиска"
              : "Топ-20 наиболее подходящих"}
          </p>
        </div>

        {/* Панель фильтров */}
        <div className="flex gap-3 bg-white p-2 rounded-lg border border-gray-200 shadow-sm">
          <div className="flex items-center px-3 text-gray-400">
            <Filter size={16} />
          </div>
          <select
            className="bg-transparent text-sm outline-none border-r pr-3 text-gray-700 cursor-pointer"
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          >
            <option value="">Все статусы</option>
            <option value="new">Новая</option>
            <option value="approved">Одобрено</option>
            <option value="rejected">Отказ</option>
            <option value="sent">Отправлено</option>
          </select>
          <input
            type="text"
            placeholder="Индустрия (IT, Fintech...)"
            className="text-sm outline-none px-2 w-40"
            value={filters.industry}
            onChange={(e) =>
              setFilters({ ...filters, industry: e.target.value })
            }
          />
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 text-gray-400">
          Загрузка данных...
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 font-semibold">Компания</th>
                <th className="px-6 py-4 font-semibold">Индустрия</th>
                <th className="px-6 py-4 font-semibold">Баллы</th>
                <th className="px-6 py-4 font-semibold">Навыки</th>
                <th className="px-6 py-4 font-semibold">Статус</th>
                <th className="px-6 py-4 font-semibold text-right">Действие</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {companies.map((company) => (
                <tr
                  key={company.id}
                  className="hover:bg-gray-50 transition-colors group"
                >
                  <td className="px-6 py-4">
                    {/* Ссылка на детальную страницу */}
                    <Link
                      to={`/company/${company.id}`}
                      className="font-bold text-gray-900 hover:text-blue-600 block"
                    >
                      {company.name}
                    </Link>
                    <a
                      href={company.url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-blue-500 flex items-center gap-1 hover:underline mt-1 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      Открыть на HH <ExternalLink size={10} />
                    </a>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {company.industry}
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`font-bold ${
                        company.score >= 85
                          ? "text-green-600"
                          : "text-yellow-600"
                      }`}
                    >
                      {company.score}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {company.main_skills.slice(0, 3).map((skill) => (
                        <span
                          key={skill}
                          className="px-2 py-0.5 bg-slate-100 text-slate-600 text-[10px] font-medium rounded border border-slate-200"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={company.status} />
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => setSelectedCompany(company)}
                      className="px-3 py-1.5 bg-white border border-gray-300 text-gray-700 text-sm rounded-lg hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 transition-all shadow-sm flex items-center gap-2 ml-auto"
                    >
                      <Mail size={14} /> Письмо
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {companies.length === 0 && (
            <div className="p-8 text-center text-gray-500">
              Ничего не найдено
            </div>
          )}
        </div>
      )}
    </div>
  );
};
