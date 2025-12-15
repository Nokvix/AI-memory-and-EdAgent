import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { X, Wand2, Check, ArrowLeft, Ban, Save } from "lucide-react";

export const LetterModal = ({ company, onClose, onUpdate }) => {
  const [letter, setLetter] = useState(null);
  const [loading, setLoading] = useState(false);
  const [bodyText, setBodyText] = useState("");

  useEffect(() => {
    fetchLetter();
  }, [company]);

  const fetchLetter = async () => {
    setLoading(true);
    const res = await api.getLetter(company.id);
    if (res.status === "success" && res.data) {
      setLetter(res.data);
      setBodyText(res.data.body);
    } else {
      setLetter(null);
    }
    setLoading(false);
  };

  const handleGenerate = async (template) => {
    setLoading(true);
    const res = await api.generateLetter(company.id, template);
    if (res.status === "success") {
      setLetter(res.data);
      setBodyText(res.data.body);
    }
    setLoading(false);
  };

  // Сохранить как черновик (PUT)
  const handleSaveDraft = async () => {
    if (!letter) return;
    setLoading(true);
    await api.updateLetter(letter.id, bodyText);
    setLoading(false);
    alert("Черновик сохранен");
  };

  const handleApprove = async () => {
    if (!letter) return;
    setLoading(true);
    await api.approveLetter(letter.id, bodyText);
    onUpdate();
    onClose();
    setLoading(false);
  };

  // Отклонить письмо
  const handleReject = async () => {
    if (!letter) return;
    const reason = prompt("Причина отклонения письма:");
    if (!reason) return;

    setLoading(true);
    await api.rejectLetter(letter.id, reason);
    onUpdate();
    onClose();
    setLoading(false);
  };

  const handleBack = () => {
    setLetter(null);
    setBodyText("");
  };

  if (!company) return null;

  return (
    <div className="fixed inset-0 bg-gray-900/40 flex items-center justify-center z-50 backdrop-blur-sm p-4">
      <div className="bg-white rounded-xl w-full max-w-2xl shadow-2xl flex flex-col max-h-[90vh] animate-in fade-in zoom-in duration-200">
        {/* Заголовок */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50 rounded-t-xl">
          <div>
            <h3 className="text-lg font-bold text-gray-800">
              Письмо для {company.name}
            </h3>
            <p className="text-xs text-gray-500 mt-0.5">
              Рейтинг совпадения: {company.score}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white hover:shadow rounded-full transition text-gray-400 hover:text-gray-700"
          >
            <X size={20} />
          </button>
        </div>

        {/* Контент */}
        <div className="p-6 overflow-y-auto flex-1">
          {loading ? (
            <div className="flex flex-col justify-center items-center h-40 gap-3 text-gray-500">
              <div className="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 border-t-transparent"></div>
              <span className="text-sm">Обработка данных...</span>
            </div>
          ) : !letter ? (
            <div className="text-center py-12 space-y-6">
              <div className="text-gray-500">
                Письмо еще не создано. Выберите шаблон:
              </div>
              <div className="flex justify-center gap-4">
                <button
                  onClick={() => handleGenerate("formal")}
                  className="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-200 text-gray-700 rounded-lg hover:border-blue-400 hover:text-blue-600 hover:shadow-md transition-all"
                >
                  <Wand2 size={16} /> Формальный
                </button>
                <button
                  onClick={() => handleGenerate("informal")}
                  className="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-200 text-gray-700 rounded-lg hover:border-purple-400 hover:text-purple-600 hover:shadow-md transition-all"
                >
                  <Wand2 size={16} /> Дружеский
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <button
                onClick={handleBack}
                className="flex items-center gap-1 text-sm text-gray-400 hover:text-blue-600 transition-colors mb-2"
              >
                <ArrowLeft size={16} /> Назад к выбору шаблона
              </button>

              <div>
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                  Тема письма
                </label>
                <div className="font-medium text-gray-900 border-b border-gray-100 pb-2 mt-1">
                  {letter.subject}
                </div>
              </div>
              <div className="flex flex-col h-full">
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                    Текст сообщения
                  </label>
                  <button
                    onClick={handleSaveDraft}
                    className="text-xs text-blue-600 hover:underline flex items-center gap-1"
                  >
                    <Save size={12} /> Сохранить черновик
                  </button>
                </div>
                <textarea
                  value={bodyText}
                  onChange={(e) => setBodyText(e.target.value)}
                  className="w-full h-64 p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:outline-none resize-none font-sans text-sm leading-relaxed text-gray-700 bg-gray-50 focus:bg-white transition-colors"
                />
              </div>
            </div>
          )}
        </div>

        {/* Футер с кнопками */}
        {letter && (
          <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 flex justify-between rounded-b-xl">
            <button
              onClick={handleReject}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg font-medium transition text-sm"
            >
              <Ban size={16} /> Отказать
            </button>

            <div className="flex gap-2">
              <button
                onClick={onClose}
                className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-200 rounded-lg font-medium transition text-sm"
              >
                Отмена
              </button>
              <button
                onClick={handleApprove}
                disabled={loading}
                className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition shadow-sm hover:shadow-blue-200 text-sm"
              >
                <Check size={16} strokeWidth={2.5} /> Одобрить
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
