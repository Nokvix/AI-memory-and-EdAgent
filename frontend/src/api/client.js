import { companies, letters, emailStatuses } from './mockData';

const USE_MOCK = false; // false = Работаем с реальным API (FastAPI)
const BASE_URL = 'http://localhost:8000/api';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Вспомогательная функция для обработки ошибок
const handleResponse = async (res) => {
    if (!res.ok) {
        let errorMessage = 'Ошибка сервера';
        try {
            const errorData = await res.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (e) {
            console.error("Не удалось прочитать ошибку:", e);
        }
        return { status: 'error', message: errorMessage, error_code: res.status };
    }
    return null; // Нет ошибки
};

export const api = {
    // GET /api/companies/top-20
    getTopCompanies: async () => {
        if (USE_MOCK) {
            await delay(500);
            const top20 = [...companies].sort((a, b) => b.score - a.score).slice(0, 20);
            return { status: 'success', data: top20, total: top20.length };
        }

        try {
            const res = await fetch(`${BASE_URL}/companies/top-20`);
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data, total: data.length };
        } catch (error) {
            console.error(error);
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // GET /api/companies/{id}
    getCompanyById: async (id) => {
        if (USE_MOCK) {
            await delay(300);
            const company = companies.find(c => c.id === Number(id));
            if (!company) return { status: 'error', error_code: 'COMPANY_NOT_FOUND', message: 'Компания не найдена' };
            return { status: 'success', data: company };
        }

        try {
            const res = await fetch(`${BASE_URL}/companies/${id}`);
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // GET /api/companies (Фильтрация и поиск)
    getCompanies: async (params = {}) => {
        if (USE_MOCK) {
            await delay(500);
            let data = [...companies];
            if (params.status) data = data.filter(c => c.status === params.status);
            if (params.industry) data = data.filter(c => c.industry === params.industry);
            if (params.min_score) data = data.filter(c => c.score >= params.min_score);
            return {
                status: 'success',
                data: data,
                total: data.length,
                page: params.page || 1,
                limit: params.limit || 20
            };
        }

        const query = new URLSearchParams(params).toString();
        try {
            const res = await fetch(`${BASE_URL}/companies?${query}`);
            const error = await handleResponse(res);
            if (error) return error;

            const json = await res.json();
            return {
                status: 'success',
                data: json.data,
                total: json.total,
                page: json.page,
                limit: json.limit
            };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // POST /api/companies/{id}/approve
    approveCompany: async (id, comment = "") => {
        if (USE_MOCK) {
            await delay(400);
            const company = companies.find(c => c.id === Number(id));
            if (company) company.status = 'approved';
            return { status: 'success', data: company };
        }

        try {
            const res = await fetch(`${BASE_URL}/companies/${id}/approve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comment })
            });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // POST /api/companies/{id}/reject
    rejectCompany: async (id, reason = "") => {
        if (USE_MOCK) {
            await delay(400);
            const company = companies.find(c => c.id === Number(id));
            if (company) company.status = 'rejected';
            return { status: 'success', data: company };
        }

        try {
            const res = await fetch(`${BASE_URL}/companies/${id}/reject`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ reason })
            });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // GET /api/letters/{company_id}
    getLetter: async (companyId) => {
        if (USE_MOCK) {
            await delay(300);
            const letter = letters[companyId];
            if (!letter) return { status: 'success', data: null };
            return { status: 'success', data: letter };
        }

        try {
            const res = await fetch(`${BASE_URL}/letters/${companyId}`);

            if (res.status === 404) {
                return { status: 'success', data: null };
            }

            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // POST /api/letters/generate/{company_id}
    generateLetter: async (companyId, template = 'formal') => {
        if (USE_MOCK) {
            await delay(800);
            return { status: 'success', data: {}, message: 'Mock generated' };
        }

        try {
            const res = await fetch(`${BASE_URL}/letters/generate/${companyId}?template=${template}`, { method: 'POST' });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // POST /api/letters/{letter_id}/approve
    approveLetter: async (letterId, bodyText) => {
        if (USE_MOCK) { return { status: 'success' }; }

        try {
            const res = await fetch(`${BASE_URL}/letters/${letterId}/approve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body: bodyText })
            });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // POST /api/letters/{letter_id}/reject
    rejectLetter: async (letterId, reason = "") => {
        if (USE_MOCK) { return { status: 'success' }; }

        try {
            const res = await fetch(`${BASE_URL}/letters/${letterId}/reject`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ reason })
            });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // PUT /api/letters/{letter_id}
    updateLetter: async (letterId, body) => {
        if (USE_MOCK) { return { status: 'success' }; }

        try {
            const res = await fetch(`${BASE_URL}/letters/${letterId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },

    // POST /api/emails/send/{company_id}
    sendEmail: async (companyId, email) => {
        if (USE_MOCK) { return { status: 'success' }; }

        try {
            const res = await fetch(`${BASE_URL}/emails/send/${companyId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            const error = await handleResponse(res);
            if (error) return error;

            const data = await res.json();
            return { status: 'success', data: data };
        } catch (error) {
            return { status: 'error', message: 'Ошибка сети' };
        }
    },
};