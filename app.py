import streamlit as st
import pandas as pd
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import time

# ----------------- COMPATIBLE RERUN -----------------
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# ----------------- PAGE & SESSION -----------------
st.set_page_config(page_title="Smart Paper Generator", page_icon="📝", layout="wide")

if "lang" not in st.session_state:
    st.session_state.lang = "kz"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "is_registered" not in st.session_state:
    st.session_state.is_registered = False
if "fig_count" not in st.session_state:
    st.session_state.fig_count = 1
if "tab_count" not in st.session_state:
    st.session_state.tab_count = 1
if "eq_count" not in st.session_state:
    st.session_state.eq_count = 1

# ----------------- LOCALES (shortened to essentials) -----------------
locales = {
    "ru": {
        "title": "📝 Умный генератор научных статей",
        "subtitle": "Вестник ЕНУ им. Л.Н. Гумилева · Химия / География · 2025",
        "btn_theme_dark": "🌙 Тёмная тема",
        "btn_theme_light": "☀️ Светлая тема",
        "nav_gen": "📄 Генератор статей",
        "nav_reg": "👤 Регистрация",
        "sidebar_title": "⚙️ Настройки",
        "lbl_lang": "Язык статьи",
        "lbl_sec": "Секция",
        "lbl_type": "Тип статьи",
        "lbl_mrnti": "МРНТИ / IRSTI",
        "sec_meta": "1. Основные метаданные",
        "lbl_title": "Название статьи",
        "lbl_authors": "Авторы",
        "lbl_authors_help": "Имя Фамилия1, Имя Фамилия2",
        "lbl_affil": "Аффилиации",
        "lbl_affil_help": "1 Университет, Город, Страна; email",
        "lbl_email": "Email для корреспонденции",
        "sec_text": "2. Текст статьи (IMRAD)",
        "lbl_abstract": "Аннотация (до 300 слов)",
        "lbl_kw": "Ключевые слова",
        "lbl_kw_help": "Слово 1; слово 2; слово 3",
        "lbl_intro": "Введение (.txt/.docx)",
        "lbl_methods": "Материалы и методы (.txt/.docx)",
        "lbl_results": "Результаты (.txt/.docx)",
        "lbl_discussion": "Обсуждение (.txt/.docx)",
        "lbl_conclusion": "Заключение (.txt/.docx)",
        "lbl_ref_manager": "📚 Менеджер литературы",
        "lbl_ref_style": "Стиль цитирования",
        "lbl_fig_manager": "📊 Менеджер рисунков",
        "lbl_tab_manager": "📋 Менеджер таблиц",
        "lbl_eq_manager": "➗ Менеджер формул",
        "lbl_add_fig": "➕ Добавить рисунок",
        "lbl_add_tab": "➕ Добавить таблицу",
        "lbl_add_eq": "➕ Добавить формулу",
        "btn_upload_short": "📎 Загрузить",
        "lbl_fig_hint_title": "💡 Подсказка для рисунков",
        "lbl_fig_hint_text": "Используйте тег `[@fig1]` и т.д. в тексте статьи.",
        "lbl_tab_hint_title": "💡 Подсказка для таблиц",
        "lbl_tab_hint_text": "Для сложных таблиц используйте .docx (с объединением ячеек).",
        "lbl_eq_hint_title": "💡 Подсказка для формул",
        "lbl_eq_hint_text": "Используйте тег `[@eq1]` в тексте статьи.",
        "btn_sample_table": "📥 Образец сложной таблицы (Times New Roman)",
        "lbl_samples": "📥 Шаблоны разделов (Times New Roman, выравнивание по ширине)",
        "sec_backmatter": "4. Дополнительная информация (Back Matter)",
        "lbl_supp": "6. Supplementary Materials",
        "lbl_contrib": "7. Author Contributions",
        "lbl_auth_info": "8. Author Information",
        "lbl_funding": "9. Funding",
        "lbl_ack": "10. Acknowledgements",
        "lbl_coi": "11. Conflicts of Interest",
        "sec_trans": "3. Переводы метаданных (кратко)",
        "trans_info": "По требованиям журнала метаданные нужны на 3 языках.",
        "gen_btn": "🚀 Сгенерировать черновик статьи",
        "err_abs_len": "⚠️ Аннотация слишком длинная: {count} слов (макс. 300).",
        "succ_abs_len": "Слов в аннотации: {count}/300",
        "err_fill_req": "Заполните минимум Название и Авторов.",
        "err_gen": "Ошибка при генерации: ",
        "succ_gen": "✅ Черновик успешно собран за {time} сек!",
        "btn_dl_docx": "⬇️ Скачать .docx",
        "reg_header": "📝 Регистрация исследователя",
        "reg_name": "ФИО (Полностью)",
        "reg_email": "Ваш Email",
        "reg_phone": "Номер телефона",
        "reg_submit": "Зарегистрироваться",
        "reg_success": "✅ Регистрация выполнена!",
        "reg_info": "Секция генератора разблокирована.",
        "reg_req_msg": "🔒 Для генерации сначала зарегистрируйтесь.",
        "reg_err_fill": "Заполните имя, email и телефон.",
        "f_author": "Канат Самарханов / Kanat Samarkhanov",
        "f_license": "Лицензия",
        "f_univ": "ЕНУ им. Л.Н. Гумилева",
        "browse_files": "Файл",
        "drag_drop": "Перетащите файл сюда",
        "limit": "Лимит 200MB",
        "fig_prefix": "Рисунок",
        "tab_prefix": "Таблица",
        "fb_header": "💬 Обратная связь",
        "fb_text": "Ваши предложения и замечания",
        "fb_btn": "Отправить",
        "fb_succ": "Спасибо!",
        "preview": "Предпросмотр",
        "col_tag": "Тег в тексте",
        "col_author": "Автор(ы)",
        "col_year": "Год",
        "col_title": "Название",
        "col_journal": "Журнал/Издательство",
        "col_vol": "Том/Стр"
    },
    "kz": {
        "title": "📝 Ғылыми мақалалардың ақылды генераторы",
        "subtitle": "Л.Н. Гумилев атындағы ЕҰУ Хабаршысы · Химия / География · 2025",
        "btn_theme_dark": "🌙 Түнгі режим",
        "btn_theme_light": "☀️ Күндізгі режим",
        "nav_gen": "📄 Мақала генераторы",
        "nav_reg": "👤 Тіркелу",
        "sidebar_title": "⚙️ Баптаулар",
        "lbl_lang": "Мақала тілі",
        "lbl_sec": "Секция",
        "lbl_type": "Мақала түрі",
        "lbl_mrnti": "МРНТИ / IRSTI",
        "sec_meta": "1. Негізгі метадеректер",
        "lbl_title": "Мақаланың атауы",
        "lbl_authors": "Авторлар",
        "lbl_authors_help": "Мысалы: Аты Жөні1, Аты Жөні2",
        "lbl_affil": "Аффилиация",
        "lbl_affil_help": "1 Университет, Қала, Ел; email",
        "lbl_email": "Email",
        "sec_text": "2. Мақала мәтіні (IMRAD)",
        "lbl_abstract": "Аңдатпа (300 сөзге дейін)",
        "lbl_kw": "Түйінді сөздер",
        "lbl_kw_help": "Сөз 1; сөз 2; сөз 3",
        "lbl_intro": "Кіріспе (.txt/.docx)",
        "lbl_methods": "Материалдар мен әдістер (.txt/.docx)",
        "lbl_results": "Нәтижелер (.txt/.docx)",
        "lbl_discussion": "Талдау (.txt/.docx)",
        "lbl_conclusion": "Қорытынды (.txt/.docx)",
        "lbl_ref_manager": "📚 Әдебиеттер менеджері",
        "lbl_ref_style": "Дәйексөз стилі",
        "lbl_fig_manager": "📊 Суреттер менеджері",
        "lbl_tab_manager": "📋 Кестелер менеджері",
        "lbl_eq_manager": "➗ Формулалар менеджері",
        "lbl_add_fig": "➕ Сурет қосу",
        "lbl_add_tab": "➕ Кесте қосу",
        "lbl_add_eq": "➕ Формула қосу",
        "btn_upload_short": "📎 Жүктеу",
        "lbl_fig_hint_title": "💡 Суреттер бойынша кеңес",
        "lbl_fig_hint_text": "Мәтінде `[@fig1]` тегін қолданыңыз.",
        "lbl_tab_hint_title": "💡 Кестелер бойынша кеңес",
        "lbl_tab_hint_text": "Күрделі кестелер үшін .docx пайдаланыңыз.",
        "lbl_eq_hint_title": "💡 Формулалар бойынша кеңес",
        "lbl_eq_hint_text": "Мәтінде `[@eq1]` тегін қолданыңыз.",
        "btn_sample_table": "📥 Times New Roman күрделі кесте үлгісі",
        "lbl_samples": "📥 Times New Roman бөлім үлгілері",
        "sec_backmatter": "4. Қосымша ақпарат",
        "lbl_supp": "6. Supplementary Materials",
        "lbl_contrib": "7. Author Contributions",
        "lbl_auth_info": "8. Author Information",
        "lbl_funding": "9. Funding",
        "lbl_ack": "10. Acknowledgements",
        "lbl_coi": "11. Conflicts of Interest",
        "sec_trans": "3. Метадеректер аудармасы (қысқаша)",
        "trans_info": "Метадеректер үш тілде қажет.",
        "gen_btn": "🚀 Мақала черновигін генерациялау",
        "err_abs_len": "⚠️ Аңдатпа тым ұзын: {count} сөз (макс. 300).",
        "succ_abs_len": "Аңдатпадағы сөз саны: {count}/300",
        "err_fill_req": "Кемінде Атауын және Авторларын енгізіңіз.",
        "err_gen": "Генерация қателігі: ",
        "succ_gen": "✅ Черновик {time} сек ішінде жиналды!",
        "btn_dl_docx": "⬇️ .docx жүктеу",
        "reg_header": "📝 Зерттеушіні тіркеу",
        "reg_name": "Аты-жөні (толық)",
        "reg_email": "Email",
        "reg_phone": "Телефон нөмірі",
        "reg_submit": "Тіркелу",
        "reg_success": "✅ Тіркелу сәтті өтті!",
        "reg_info": "Енді генератор қолжетімді.",
        "reg_req_msg": "🔒 Алдымен тіркеліңіз.",
        "reg_err_fill": "Аты-жөні, email және телефонды толтырыңыз.",
        "f_author": "Канат Самарханов / Kanat Samarkhanov",
        "f_license": "Лицензия",
        "f_univ": "Л.Н. Гумилев атындағы ЕҰУ",
        "browse_files": "Файл",
        "drag_drop": "Файлды осында сүйреңіз",
        "limit": "Шектеу 200MB",
        "fig_prefix": "Сурет",
        "tab_prefix": "Кесте",
        "fb_header": "💬 Кері байланыс",
        "fb_text": "Ұсыныстарыңыз немесе қателер",
        "fb_btn": "Жіберу",
        "fb_succ": "Рақмет!",
        "preview": "Алдын ала қарау",
        "col_tag": "Мәтіндегі тег",
        "col_author": "Автор(лар)",
        "col_year": "Жыл",
        "col_title": "Атауы",
        "col_journal": "Журнал/Баспа",
        "col_vol": "Том/Бет"
    },
    "en": {
        "title": "📝 Smart Paper Generator",
        "subtitle": "L.N. Gumilyov ENU Bulletin · Chemistry / Geography · 2025",
        "btn_theme_dark": "🌙 Dark mode",
        "btn_theme_light": "☀️ Light mode",
        "nav_gen": "📄 Paper Generator",
        "nav_reg": "👤 Registration",
        "sidebar_title": "⚙️ Settings",
        "lbl_lang": "Article language",
        "lbl_sec": "Section",
        "lbl_type": "Paper type",
        "lbl_mrnti": "IRSTI / МРНТИ",
        "sec_meta": "1. Basic metadata",
        "lbl_title": "Article title",
        "lbl_authors": "Authors",
        "lbl_authors_help": "Firstname Lastname1, Firstname Lastname2",
        "lbl_affil": "Affiliations",
        "lbl_affil_help": "1 University, City, Country; email",
        "lbl_email": "Corresponding email",
        "sec_text": "2. Main text (IMRAD)",
        "lbl_abstract": "Abstract (up to 300 words)",
        "lbl_kw": "Keywords",
        "lbl_kw_help": "Word 1; word 2; word 3",
        "lbl_intro": "Introduction (.txt/.docx)",
        "lbl_methods": "Materials and methods (.txt/.docx)",
        "lbl_results": "Results (.txt/.docx)",
        "lbl_discussion": "Discussion (.txt/.docx)",
        "lbl_conclusion": "Conclusion (.txt/.docx)",
        "lbl_ref_manager": "📚 Reference manager",
        "lbl_ref_style": "Citation style",
        "lbl_fig_manager": "📊 Figure manager",
        "lbl_tab_manager": "📋 Table manager",
        "lbl_eq_manager": "➗ Equation manager",
        "lbl_add_fig": "➕ Add figure",
        "lbl_add_tab": "➕ Add table",
        "lbl_add_eq": "➕ Add equation",
        "btn_upload_short": "📎 Upload",
        "lbl_fig_hint_title": "💡 Figures hint",
        "lbl_fig_hint_text": "Use tags like `[@fig1]` in the text.",
        "lbl_tab_hint_title": "💡 Tables hint",
        "lbl_tab_hint_text": "Use .docx for complex tables.",
        "lbl_eq_hint_title": "💡 Equations hint",
        "lbl_eq_hint_text": "Use tags `[@eq1]`, `[@eq2]` in text.",
        "btn_sample_table": "📥 Complex table sample (Times New Roman)",
        "lbl_samples": "📥 Section samples (Times New Roman, justified)",
        "sec_backmatter": "4. Back matter",
        "lbl_supp": "6. Supplementary materials",
        "lbl_contrib": "7. Author contributions",
        "lbl_auth_info": "8. Author information",
        "lbl_funding": "9. Funding",
        "lbl_ack": "10. Acknowledgements",
        "lbl_coi": "11. Conflicts of interest",
        "sec_trans": "3. Translations (short)",
        "trans_info": "Journal requires metadata in three languages.",
        "gen_btn": "🚀 Generate draft article",
        "err_abs_len": "⚠️ Abstract too long: {count} words (max 300).",
        "succ_abs_len": "Words in abstract: {count}/300",
        "err_fill_req": "Please fill Title and Authors.",
        "err_gen": "Generation error: ",
        "succ_gen": "✅ Draft assembled in {time} sec!",
        "btn_dl_docx": "⬇️ Download .docx",
        "reg_header": "📝 Registration",
        "reg_name": "Full name",
        "reg_email": "Email",
        "reg_phone": "Phone",
        "reg_submit": "Register",
        "reg_success": "✅ Registration successful!",
        "reg_info": "Generator is now unlocked.",
        "reg_req_msg": "🔒 Please register first.",
        "reg_err_fill": "Fill name, email, phone.",
        "f_author": "Kanat Samarkhanov",
        "f_license": "License",
        "f_univ": "L.N. Gumilyov ENU",
        "browse_files": "File",
        "drag_drop": "Drag & drop here",
        "limit": "Limit 200MB",
        "fig_prefix": "Figure",
        "tab_prefix": "Table",
        "fb_header": "💬 Feedback",
        "fb_text": "Your suggestions or issues",
        "fb_btn": "Submit",
        "fb_succ": "Thank you!",
        "preview": "Preview",
        "col_tag": "Tag in text",
        "col_author": "Author(s)",
        "col_year": "Year",
        "col_title": "Title",
        "col_journal": "Journal/Publisher",
        "col_vol": "Volume/Pages"
    }
}
l = locales[st.session_state.lang]

# ----------------- THEME from CHECKER -----------------
dark_css = (
    "<style>"
    "html,body,[class*='css'],.stApp{background-color:#0d1b2e !important;color:#c9d8ee !important;"
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif !important;}"
    "h1,h2,h3,h4,h5,h6,[data-testid='stMarkdownContainer'] h1,[data-testid='stMarkdownContainer'] h2,"
    "[data-testid='stMarkdownContainer'] h3{color:#e2edf7 !important;font-weight:600 !important;}"
    "p,span,label,div,li,[data-testid='stMarkdownContainer'] p,"
    "[data-testid='stCaptionContainer'],.stCaption{color:#c9d8ee !important;}"
    "[data-testid='block-container'],[data-testid='stVerticalBlock'],"
    "section[data-testid='stSidebar']{background-color:#0d1b2e !important;}"
    "[data-testid='stMetric']{background:#0f2340 !important;border:1px solid #1e3a5f !important;"
    "border-radius:6px !important;padding:12px 16px !important;}"
    "[data-testid='stMetricValue']{color:#e2edf7 !important;}"
    "[data-testid='stMetricLabel']{color:#7b96b8 !important;}"
    ".stButton>button{background-color:#0f2340 !important;color:#c9d8ee !important;"
    "border:1px solid #1e3a5f !important;border-radius:6px !important;}"
    ".stButton>button:hover{background-color:#1e3a5f !important;color:#e2edf7 !important;}"
    "[data-testid='stDownloadButton']>button{background-color:#238636 !important;color:#fff !important;"
    "border:1px solid #2ea043 !important;border-radius:6px !important;}"
    "[data-testid='stDownloadButton']>button:hover{background-color:#2ea043 !important;}"
    "[data-testid='stFileUploader']{background-color:#0f2340 !important;border-radius:8px !important;}"
    "[data-testid='stFileUploadDropzone']{background-color:#0f2340 !important;"
    "border:2px dashed #1e3a5f !important;border-radius:8px !important;padding:24px 16px !important;}"
    "[data-testid='stFileUploadDropzone']:hover{background-color:#112850 !important;border-color:#2f5f9e !important;}"
    "[data-testid='stFileUploader'] *,[data-testid='stFileUploadDropzone'] *{color:#c9d8ee !important;}"
    "[data-testid='stFileUploadDropzone'] button{background-color:#1e3a5f !important;"
    "color:#c9d8ee !important;border:1px solid #2f5f9e !important;border-radius:6px !important;"
    "padding:5px 16px !important;font-size:13px !important;font-weight:500 !important;}"
    "[data-testid='stFileUploadDropzone'] button:hover{background-color:#2f5f9e !important;"
    "border-color:#58a6ff !important;color:#e2edf7 !important;}"
    "[data-testid='stFileUploaderFile']{background-color:#112240 !important;"
    "border:1px solid #1e3a5f !important;border-radius:6px !important;}"
    "[data-testid='stFileUploaderDeleteBtn'] button{color:#7b96b8 !important;}"
    "[data-testid='stFileUploaderDeleteBtn'] button:hover{color:#f85149 !important;}"
    "[data-testid='stDataFrame'],.stDataFrame iframe{border:1px solid #1e3a5f !important;"
    "border-radius:8px !important;overflow:hidden !important;"
    "box-shadow:0 2px 8px rgba(0,0,0,0.4) !important;}"
    "[data-testid='stAlert']{background-color:#0f2340 !important;border:1px solid #1f6feb !important;"
    "color:#c9d8ee !important;border-radius:6px !important;}"
    ".stSpinner>div{color:#c9d8ee !important;}"
    "hr{border-color:#1e3a5f !important;}"
    "input,textarea,select{background-color:#0f2340 !important;color:#c9d8ee !important;"
    "border:1px solid #1e3a5f !important;}"
    "[data-testid='stSelectbox']>div>div{background-color:#0f2340 !important;"
    "border:1px solid #1e3a5f !important;border-radius:6px !important;color:#c9d8ee !important;}"
    ".title-block h1{font-size:1.5rem !important;margin:0 !important;}"
    ".title-block p{font-size:0.85rem !important;margin:0 !important;opacity:0.8;}"
    "</style>"
)

light_css = (
    "<style>"
    "[data-testid='stMetric']{background:#fff;padding:12px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,.08);}"
    "h1,h2,h3{color:#1a3a5c;}"
    "[data-testid='stDownloadButton']>button{background-color:#2ea043;color:#fff;border-radius:6px;}"
    "[data-testid='stDataFrame'],.stDataFrame iframe{border:1px solid #d0d7de;"
    "border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.08);}"
    ".title-block h1{font-size:1.5rem !important;margin:0 !important;}"
    ".title-block p{font-size:0.85rem !important;margin:0 !important;opacity:0.8;}"
    "</style>"
)

st.markdown(dark_css if st.session_state.theme == "dark" else light_css,
            unsafe_allow_html=True)

# ----------------- SAMPLE DOCX GENERATORS (Times New Roman) -----------------
def create_sample_section_docx(title_text):
    doc = docx.Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style._element.rPr.rFonts.set(docx.oxml.ns.qn("w:eastAsia"), "Times New Roman")
    style.font.size = docx.shared.Pt(12)

    h = doc.add_heading(title_text, level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph(
        "This is a sample section in Times New Roman. Replace this text with your real content. "
        "All paragraphs are justified to match the journal template. "
    )
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p2 = doc.add_paragraph(
        "Example of inline tags: Results are shown in [@fig1] and summarized in [@tab1]. "
        "Equation [@eq1] is referenced in the text. Reference example [@ref1]."
    )
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

def create_sample_table_docx():
    doc = docx.Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style._element.rPr.rFonts.set(docx.oxml.ns.qn("w:eastAsia"), "Times New Roman")
    style.font.size = docx.shared.Pt(12)

    p_tag = doc.add_paragraph("[@tab1]")
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title = doc.add_paragraph("Table 1. Example of complex table (merged cells).")
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    table = doc.add_table(rows=3, cols=3)
    table.style = "Table Grid"
    a = table.cell(0, 0)
    b = table.cell(0, 1)
    a.merge(b)
    a.text = "Merged Header (Col 1–2)"
    table.cell(0, 2).text = "Header 3"
    table.cell(1, 0).text = "Data A"
    table.cell(1, 1).text = "Data B"
    table.cell(1, 2).text = "Data C"
    table.cell(2, 0).text = "More A"
    table.cell(2, 1).text = "More B"
    table.cell(2, 2).text = "More C"

    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# ----------------- SIMPLE HELPERS -----------------
def extract_text(uploaded_file):
    if not uploaded_file:
        return ""
    try:
        if uploaded_file.name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".docx"):
            d = docx.Document(uploaded_file)
            return "\n".join(p.text for p in d.paragraphs)
    except Exception:
        return ""
    return ""

def render_live_uploader(label, key, loc_preview, is_locked):
    f = st.file_uploader(label, type=["txt", "docx"], key=key, disabled=is_locked)
    if f:
        txt = extract_text(f)
        with st.expander(f"👀 {loc_preview}", expanded=False):
            bg = "#112240" if st.session_state.theme == "dark" else "#ffffff"
            st.markdown(
                f"<div style='max-height:150px;overflow-y:auto;font-size:12px;"
                f"padding:8px 10px;background:{bg};border-radius:6px;'>"
                f"{txt}</div>",
                unsafe_allow_html=True,
            )
    return f

# ----------------- HEADER -----------------
hc1, hc2, hc3 = st.columns([6, 2, 2])
with hc1:
    st.markdown(
        f"<div class='title-block'><h1>{l['title']}</h1><p>{l['subtitle']}</p></div>",
        unsafe_allow_html=True,
    )
with hc2:
    _lang_labels = {"kz": "🇰🇿 Қазақша", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}
    _sel = st.selectbox(
        "lang",
        list(_lang_labels.keys()),
        index=list(_lang_labels.keys()).index(st.session_state.lang),
        format_func=lambda x: _lang_labels[x],
        label_visibility="collapsed",
    )
    if _sel != st.session_state.lang:
        st.session_state.lang = _sel
        safe_rerun()
with hc3:
    _tbtn = l["btn_theme_light"] if st.session_state.theme == "dark" else l["btn_theme_dark"]
    if st.button(_tbtn, use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        safe_rerun()
st.markdown("---")

# ----------------- NAVIGATION -----------------
app_mode = st.radio("", [l["nav_gen"], l["nav_reg"]],
                    horizontal=True, label_visibility="collapsed")
is_locked = not st.session_state.is_registered

# ================= GENERATOR =================
if app_mode == l["nav_gen"]:
    if is_locked:
        st.error(l["reg_req_msg"], icon="🔒")

    # SETTINGS
    st.subheader(l["sidebar_title"])
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        primary_lang = st.selectbox(l["lbl_lang"], ["Русский", "Қазақша", "English"],
                                    disabled=is_locked)
    with sc2:
        section = st.selectbox(l["lbl_sec"], ["Химия", "География"],
                               disabled=is_locked)
    with sc3:
        paper_type = st.selectbox(l["lbl_type"], ["Article", "Review"],
                                  disabled=is_locked)
    with sc4:
        mrnti = st.text_input(l["lbl_mrnti"], "06.81.23", disabled=is_locked)

    # METADATA
    st.header(l["sec_meta"])
    m1, m2 = st.columns(2)
    with m1:
        title = st.text_area(l["lbl_title"], height=68, disabled=is_locked)
        authors = st.text_area(l["lbl_authors"], height=68,
                               help=l["lbl_authors_help"], disabled=is_locked)
    with m2:
        affiliations = st.text_area(l["lbl_affil"], height=68,
                                    help=l["lbl_affil_help"], disabled=is_locked)
        corr_email = st.text_input(l["lbl_email"], disabled=is_locked)

    # IMRAD
    st.header(l["sec_text"])
    abstract = st.text_area(l["lbl_abstract"], height=100, disabled=is_locked)
    kw = st.text_input(l["lbl_kw"], help=l["lbl_kw_help"], disabled=is_locked)
    abs_wc = len(abstract.split()) if abstract else 0
    if not is_locked and abs_wc:
        if abs_wc > 300:
            st.error(l["err_abs_len"].format(count=abs_wc))
        else:
            st.success(l["succ_abs_len"].format(count=abs_wc))

    st.markdown("##### " + l["lbl_samples"])
    c_s1, c_s2, c_s3, c_s4, c_s5 = st.columns(5)
    with c_s1:
        st.download_button("Intro", create_sample_section_docx("Introduction"),
                           file_name="sample_intro_TNR.docx",
                           use_container_width=True, disabled=is_locked)
    with c_s2:
        st.download_button("Methods", create_sample_section_docx("Materials and Methods"),
                           file_name="sample_methods_TNR.docx",
                           use_container_width=True, disabled=is_locked)
    with c_s3:
        st.download_button("Results", create_sample_section_docx("Results"),
                           file_name="sample_results_TNR.docx",
                           use_container_width=True, disabled=is_locked)
    with c_s4:
        st.download_button("Discussion", create_sample_section_docx("Discussion"),
                           file_name="sample_discussion_TNR.docx",
                           use_container_width=True, disabled=is_locked)
    with c_s5:
        st.download_button("Conclusion", create_sample_section_docx("Conclusion"),
                           file_name="sample_conclusion_TNR.docx",
                           use_container_width=True, disabled=is_locked)

    i1, i2, i3 = st.columns(3)
    with i1:
        file_intro = render_live_uploader(l["lbl_intro"], "up_intro", l["preview"], is_locked)
        file_methods = render_live_uploader(l["lbl_methods"], "up_meth", l["preview"], is_locked)
    with i2:
        file_results = render_live_uploader(l["lbl_results"], "up_res", l["preview"], is_locked)
        file_disc = render_live_uploader(l["lbl_discussion"], "up_disc", l["preview"], is_locked)
    with i3:
        file_concl = render_live_uploader(l["lbl_conclusion"], "up_conc", l["preview"], is_locked)

    st.markdown("---")

    # FIGURES & TABLES
    fcol, tcol = st.columns(2)
    with fcol:
        st.header(l["lbl_fig_manager"])
        with st.expander(l["lbl_fig_hint_title"]):
            st.markdown(l["lbl_fig_hint_text"])
        hf1, hf2, hf3 = st.columns([1.2, 3.2, 3])
        hf1.markdown("**Tag**")
        hf2.markdown("**Caption**")
        hf3.markdown("**File**")

        for i in range(st.session_state.fig_count):
            cf1, cf2, cf3 = st.columns([1.2, 3.2, 3])
            with cf1:
                st.text_input(f"fig_tag_{i}", value=f"[@fig{i+1}]",
                              key=f"f_tag_{i}", label_visibility="collapsed",
                              disabled=is_locked)
            with cf2:
                st.text_input(f"fig_cap_{i}", placeholder="Caption...",
                              key=f"f_cap_{i}", label_visibility="collapsed",
                              disabled=is_locked)
            with cf3:
                st.file_uploader(f"fig_file_{i}", type=["png", "jpg", "jpeg"],
                                 key=f"f_file_{i}", label_visibility="collapsed",
                                 disabled=is_locked)
        if st.button(l["lbl_add_fig"], disabled=is_locked):
            st.session_state.fig_count += 1
            safe_rerun()

    with tcol:
        st.header(l["lbl_tab_manager"])
        with st.expander(l["lbl_tab_hint_title"]):
            st.markdown(l["lbl_tab_hint_text"])
            st.download_button(l["btn_sample_table"],
                               create_sample_table_docx(),
                               file_name="sample_complex_table_TNR.docx",
                               use_container_width=True, disabled=is_locked)
        ht1, ht2, ht3 = st.columns([1.2, 3.2, 3])
        ht1.markdown("**Tag**")
        ht2.markdown("**Caption**")
        ht3.markdown("**File**")
        for i in range(st.session_state.tab_count):
            ct1, ct2, ct3 = st.columns([1.2, 3.2, 3])
            with ct1:
                st.text_input(f"tab_tag_{i}", value=f"[@tab{i+1}]",
                              key=f"t_tag_{i}", label_visibility="collapsed",
                              disabled=is_locked)
            with ct2:
                st.text_input(f"tab_cap_{i}", placeholder="Caption...",
                              key=f"t_cap_{i}", label_visibility="collapsed",
                              disabled=is_locked)
            with ct3:
                st.file_uploader(f"tab_file_{i}",
                                 type=["docx", "xlsx", "csv", "txt"],
                                 key=f"t_file_{i}", label_visibility="collapsed",
                                 disabled=is_locked)
        if st.button(l["lbl_add_tab"], disabled=is_locked):
            st.session_state.tab_count += 1
            safe_rerun()

    st.markdown("---")

    # EQUATION MANAGER
    st.header(l["lbl_eq_manager"])
    with st.expander(l["lbl_eq_hint_title"]):
        st.markdown(l["lbl_eq_hint_text"])
    he1, he2 = st.columns([1.2, 8.8])
    he1.markdown("**Tag**")
    he2.markdown("**Equation / Formula**")
    for i in range(st.session_state.eq_count):
        ce1, ce2 = st.columns([1.2, 8.8])
        with ce1:
            st.text_input(f"eq_tag_{i}", value=f"[@eq{i+1}]",
                          key=f"e_tag_{i}", label_visibility="collapsed",
                          disabled=is_locked)
        with ce2:
            st.text_input(f"eq_val_{i}", placeholder="E = mc^2 ...",
                          key=f"e_val_{i}", label_visibility="collapsed",
                          disabled=is_locked)
    if st.button(l["lbl_add_eq"], disabled=is_locked):
        st.session_state.eq_count += 1
        safe_rerun()

    st.markdown("---")

    # REFERENCE MANAGER
    st.header(l["lbl_ref_manager"])
    ref_style = st.selectbox(l["lbl_ref_style"], ["GOST", "APA", "IEEE"],
                             disabled=is_locked)
    ref_df = pd.DataFrame([{
        l["col_tag"]: "[@ref1]",
        l["col_author"]: "",
        l["col_year"]: "",
        l["col_title"]: "",
        l["col_journal"]: "",
        l["col_vol"]: ""
    }])
    if not is_locked:
        refs_edited = st.data_editor(ref_df, num_rows="dynamic",
                                     use_container_width=True)
    else:
        refs_edited = ref_df
        st.dataframe(ref_df, use_container_width=True)

    st.markdown("---")

    # BACK MATTER (short)
    st.header(l["sec_backmatter"])
    st.text_area(l["lbl_supp"], height=60, disabled=is_locked)
    st.text_area(l["lbl_contrib"], height=80, disabled=is_locked)
    st.text_area(l["lbl_auth_info"], height=70, disabled=is_locked)
    st.text_area(l["lbl_funding"], height=60, disabled=is_locked)
    st.text_area(l["lbl_ack"], height=60, disabled=is_locked)
    st.text_area(l["lbl_coi"], height=70, disabled=is_locked)

    # TRANSLATIONS NOTE
    st.header(l["sec_trans"])
    st.info(l["trans_info"])

    st.markdown("---")

    # GENERATE DRAFT (placeholder)
    gen_btn = st.button(l["gen_btn"], type="primary",
                        use_container_width=True, disabled=is_locked)
    if gen_btn and not is_locked:
        if not title or not authors:
            st.warning(l["err_fill_req"])
        elif abs_wc > 300:
            st.error(l["err_abs_len"].format(count=abs_wc))
        else:
            with st.spinner("Assembling draft (no template yet)..."):
                time.sleep(1.5)
            st.success(l["succ_gen"].format(time=1.5))
            # TODO: here you plug your DocxTemplate rendering as before

# ================= REGISTRATION =================
elif app_mode == l["nav_reg"]:
    st.header(l["reg_header"])
    if st.session_state.is_registered:
        st.success(l["reg_success"])
        st.info(l["reg_info"])
    else:
        with st.form("reg_form"):
            name = st.text_input(l["reg_name"])
            email = st.text_input(l["reg_email"])
            phone = st.text_input(l["reg_phone"])
            submitted = st.form_submit_button(l["reg_submit"], type="primary")
            if submitted:
                if name and email and phone:
                    st.session_state.is_registered = True
                    safe_rerun()
                else:
                    st.error(l["reg_err_fill"])

# ----------------- FEEDBACK -----------------
st.markdown("---")
st.subheader(l["fb_header"])
with st.expander(l["fb_text"], expanded=True):
    with st.form("fb_form", clear_on_submit=True):
        st.text_input("Email (optional)")
        fb_text = st.text_area(l["fb_text"], height=80)
        if st.form_submit_button(l["fb_btn"]):
            if fb_text.strip():
                st.success(l["fb_succ"])

# ----------------- FOOTER -----------------
st.markdown("---")
fc = "#7b96b8" if st.session_state.theme == "dark" else "#555"
st.markdown(
    f"<div style='text-align:center;font-size:11px;color:{fc};padding:15px;'>"
    f"© 2025 {l['f_author']} · {l['f_univ']}</div>",
    unsafe_allow_html=True,
)
