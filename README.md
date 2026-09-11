Markdown
# 📚 O'quv Markaz ERP/CRM Backend

O'quv markazlarining kundalik faoliyatini to'liq avtomatlashtirish uchun mo'ljallangan zamonaviy va kengaytirilgan **ERP va CRM tizimi** backend qismi. 

---

## 🚀 Texnologiyalar (Tech Stack)
* **Programming Language:** Python 3.10+
* **Framework:** FastAPI
* **Database Management System:** MySQL
* **ORM & Migrations:** SQLAlchemy, Alembic
* **Data Validation:** Pydantic
* **Server:** Uvicorn

---

## 🗄️ Tizim Modul Arxitekturasi (ERD 36 ta jadval)
Loyihaning ma'lumotlar bazasi arxitekturasi quyidagi **7 ta asosiy modulga** bo'lingan:

1. **🏢 Tashkilot:** Filiallar (`branches`), xonalar (`rooms`).
2. **📖 O'quv jarayoni:** Kurslar, guruhlar, talabalar, dars jadvallari, davomat, imtihonlar, sertifikatlar va o'qishga qabul qilish (`enrollments`).
3. **🎯 CRM & Lidlar:** Potentsial mijozlar (`leads`), lid manbalari, statuslari, sinov darslari (`trial_lessons`), vazifalar (`tasks`) va lid faoliyatlari.
4. **💰 Moliya:** Hisob-fakturalar (`invoices`), to'lovlar (`payments`), xarajatlar (`expenses`), oylik maoshlar (`payrolls`) va chegirmalar.
5. **👥 Xodim va Ruxsatlar:** Xodimlar (`employees`), rollar (`roles`), o'qituvchi profillari (`teacher_profiles`).
6. **📨 Kommunikatsiya:** SMS shablonlar, SMS loglari va bildirishnomalar (`notifications`).
7. **⚙️ Tizim:** Fayl ilovalari (`attachments`) va audit loglari (`audit_logs`).

---

Tayyor bo`lishi bilan barcha qadamlari yuklanadi va yanada to`liqroq tushuntiriladi, ungacha sizdan sabr qilishingizni so`rab qolamiz, tez orada tayyor bo`ladi
