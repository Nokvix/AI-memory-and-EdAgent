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
};