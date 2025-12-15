import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import {
  ArrowLeft,
  ExternalLink,
  Briefcase,
  XCircle,
  Mail,
  Clock,
  Check,
} from "lucide-react";
import { LetterModal } from "../components/LetterModal";

export const CompanyDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showLetterModal, setShowLetterModal] = useState(false);

  useEffect(() => {
    loadCompany();
  }, [id]);

  const loadCompany = async () => {
    setLoading(true);
    const res = await api.getCompanyById(id);
    if (res.status === "success") {
      setCompany(res.data);
    }
    setLoading(false);
  };

  const handleApproveCompany = async () => {
    setLoading(true);
    await api.approveCompany(id);
    await loadCompany();
    setLoading(false);
  };

  const handleRejectCompany = async () => {
    const reason = prompt("Укажите причину отказа:");
    if (!reason) return;

    setLoading(true);
    await api.rejectCompany(id, reason);
    await loadCompany();
    setLoading(false);
  };

  if (loading && !company)
    return <div className="text-center py-20">Загрузка...</div>;
  if (!company)
    return <div className="text-center py-20">Компания не найдена</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-500 hover:text-blue-600 mb-6 transition"
      >
        <ArrowLeft size={16} /> Назад к списку
      </button>

      {/* Карточка компании */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
        <div className="p-8 border-b border-gray-100 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {company.name}
            </h1>
            <div className="flex gap-4 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <Briefcase size={14} /> {company.industry}
              </span>
              <span className="flex items-center gap-1">
                <Clock size={14} /> Добавлено:{" "}
                {new Date(company.created_at).toLocaleDateString()}
              </span>
              {/* Отображение текущего статуса текстом */}
              <span
                className={`px-2 py-0.5 rounded text-xs font-bold uppercase flex items-center 
                ${
                  company.status === "approved"
                    ? "bg-green-100 text-green-700"
                    : company.status === "rejected"
                    ? "bg-red-100 text-red-700"
                    : "bg-blue-100 text-blue-700"
                }`}
              >
                {company.status === "new"
                  ? "Новая"
                  : company.status === "approved"
                  ? "Одобрено"
                  : company.status === "rejected"
                  ? "Отказ"
                  : company.status}
              </span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-blue-600">
              {company.score}
            </div>
            <div className="text-xs text-gray-400 uppercase font-bold">
              Score
            </div>
          </div>
        </div>

        <div className="p-8 bg-gray-50 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-sm font-bold text-gray-400 uppercase mb-3">
              Основные навыки
            </h3>
            <div className="flex flex-wrap gap-2">
              {company.main_skills.map((skill) => (
                <span
                  key={skill}
                  className="px-3 py-1 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 shadow-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Блок действий */}
          <div>
            <h3 className="text-sm font-bold text-gray-400 uppercase mb-3">
              Действия
            </h3>
            <div className="flex flex-col gap-3">
              <button
                onClick={() => setShowLetterModal(true)}
                className="w-full bg-white border border-blue-200 text-blue-700 hover:bg-blue-50 py-2 rounded-lg font-medium flex justify-center items-center gap-2 transition"
              >
                <Mail size={16} /> Работа с письмом
              </button>

              <div className="flex gap-3">
                {/* Кнопка Одобрить (скрываем, если уже одобрено) */}
                {company.status !== "approved" && (
                  <button
                    onClick={handleApproveCompany}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg font-medium flex justify-center items-center gap-2 transition shadow-sm"
                  >
                    <Check size={16} /> Одобрить
                  </button>
                )}

                {/* Кнопка Отказать (скрываем, если уже отказано) */}
                {company.status !== "rejected" && (
                  <button
                    onClick={handleRejectCompany}
                    className="flex-1 border border-red-200 text-red-600 hover:bg-red-50 py-2 rounded-lg font-medium flex justify-center items-center gap-2 transition"
                  >
                    <XCircle size={16} /> Отказать
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Список вакансий */}
      <h2 className="text-xl font-bold mb-4">
        Найдено вакансий: {company.vacancies?.length || 0}
      </h2>
      <div className="space-y-3">
        {company.vacancies && company.vacancies.length > 0 ? (
          company.vacancies.map((vac) => (
            <div
              key={vac.id}
              className="bg-white p-4 rounded-lg border border-gray-200 flex justify-between items-center hover:shadow-md transition"
            >
              <div>
                <div className="font-bold text-lg text-blue-900">
                  {vac.position}
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  Стек: {vac.skills.join(", ")}
                </div>
              </div>
              <a
                href={vac.url}
                target="_blank"
                rel="noreferrer"
                className="text-blue-600 hover:text-blue-800 p-2 bg-blue-50 rounded-full"
              >
                <ExternalLink size={18} />
              </a>
            </div>
          ))
        ) : (
          <div className="text-gray-400 italic">
            Список вакансий пуст или не загружен
          </div>
        )}
      </div>

      {showLetterModal && (
        <LetterModal
          company={company}
          onClose={() => setShowLetterModal(false)}
          onUpdate={loadCompany}
        />
      )}
    </div>
  );
};
