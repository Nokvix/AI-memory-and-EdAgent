export const companies = [
    {
        id: 1,
        name: "ООО Контур",
        url: "https://hh.ru/employer/41862",
        industry: "IT",
        score: 92,
        vacancy_count: 12,
        main_skills: ["Python", "JavaScript", "SQL"],
        status: "new",
        created_at: "2025-12-07T14:30:00Z",
        vacancies: [
            { id: 101, position: "Python Developer", url: "https://hh.ru/vacancy/1", skills: ["Python", "Django"] },
            { id: 102, position: "Frontend Dev", url: "https://hh.ru/vacancy/2", skills: ["React", "JS"] }
        ]
    },
    {
        id: 2,
        name: "OZON Tech",
        url: "https://hh.ru/employer/123",
        industry: "E-commerce",
        score: 88,
        vacancy_count: 8,
        main_skills: ["Go", "Kubernetes", "PostgreSQL"],
        status: "approved", // Компания одобрена
        created_at: "2025-12-07T14:31:00Z",
        vacancies: [
            { id: 201, position: "Go Developer", url: "https://hh.ru/vacancy/3", skills: ["Go", "Docker"] }
        ]
    },
    {
        id: 3,
        name: "Яндекс",
        url: "https://hh.ru/employer/456",
        industry: "IT",
        score: 85,
        vacancy_count: 20,
        main_skills: ["C++", "Python", "React"],
        status: "new",
        created_at: "2025-12-07T14:32:00Z",
        vacancies: []
    },
    {
        id: 4,
        name: "СберТех",
        url: "https://hh.ru/employer/789",
        industry: "Fintech",
        score: 72,
        vacancy_count: 5,
        main_skills: ["Java", "Spring", "Kafka"],
        status: "rejected",
        created_at: "2025-12-07T14:33:00Z",
        vacancies: []
    }
];

export const letters = {
    // Ключ - ID компании
    2: {
        id: 501,
        company_id: 2,
        template: "formal",
        subject: "Предложение о сотрудничестве с OZON",
        body: "Здравствуйте! Нам очень нравится ваш стек технологий (Go, K8s). Давайте дружить.",
        status: "approved", // Письмо одобрено
        created_at: "2025-12-07T15:00:00Z",
        approved_at: "2025-12-07T15:30:00Z",
        sent_at: null
    }
};

export const emailStatuses = {
    // Ключ - ID компании
    2: {
        company_id: 2,
        email: "hr@ozon.ru",
        sent_at: "2025-12-07T14:45:00Z",
        delivery_status: "delivered",
        opened_at: null,
        clicked_at: null
    }
};