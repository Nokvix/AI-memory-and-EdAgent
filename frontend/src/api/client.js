import { companies } from './mockData';

const USE_MOCK = true;
const BASE_URL = 'http://localhost:8000/api';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const api = {
    // Получить Топ-20
    getTopCompanies: async () => {
        if (USE_MOCK) {
            await delay(500);
            // Сортируем и берем первые 20
            const top20 = [...companies].sort((a, b) => b.score - a.score).slice(0, 20);
            return { status: 'success', data: top20, total: top20.length };
        }
        const res = await fetch(`${BASE_URL}/companies/top-20`);
        return res.json();
    },

    getCompanyById: async (id) => {
        if (USE_MOCK) {
            await delay(300);
            const company = companies.find(c => c.id === Number(id));
            if (!company) return { status: 'error', error_code: 'COMPANY_NOT_FOUND', message: 'Компания не найдена' };
            return { status: 'success', data: company };
        }
        const res = await fetch(`${BASE_URL}/companies/${id}`);
        return res.json();
    },

    getCompanies: async (params = {}) => {
        if (USE_MOCK) {
            await delay(500);
            let data = [...companies];

            if (params.status) data = data.filter(c => c.status === params.status);
            if (params.industry) data = data.filter(c => c.industry === params.industry);
            if (params.min_score) data = data.filter(c => c.score >= params.min_score);

            // Сортировка
            if (params.sort_by === 'score_desc') data.sort((a, b) => b.score - a.score);
            if (params.sort_by === 'score_asc') data.sort((a, b) => a.score - b.score);

            return {
                status: 'success',
                data: data,
                total: data.length,
                page: params.page || 1,
                limit: params.limit || 20
            };
        }
        const query = new URLSearchParams(params).toString();
        const res = await fetch(`${BASE_URL}/companies?${query}`);
        return res.json();
    },
};