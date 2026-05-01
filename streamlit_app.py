import React, { useEffect, useMemo, useState } from "react";

const initialSubjects = [ { id: 1, name: "Direito Penal", topics: [ { id: 101, name: "Teoria do Crime", status: "Estudado", studiedAt: "2026-04-30", questions: 20, correct: 14, wrong: 6, }, { id: 102, name: "Culpabilidade", status: "Em andamento", studiedAt: null, questions: 8, correct: 5, wrong: 3, }, { id: 103, name: "Crimes contra a pessoa", status: "Não iniciado", studiedAt: null, questions: 0, correct: 0, wrong: 0, }, ], }, { id: 2, name: "Português", topics: [ { id: 201, name: "Interpretação de Texto", status: "Estudado", studiedAt: "2026-04-29", questions: 30, correct: 24, wrong: 6, }, { id: 202, name: "Concordância Verbal", status: "Não iniciado", studiedAt: null, questions: 0, correct: 0, wrong: 0, }, ], }, { id: 3, name: "Informática", topics: [ { id: 301, name: "Redes de Computadores", status: "Em andamento", studiedAt: null, questions: 12, correct: 7, wrong: 5, }, ], }, ];

const initialErrors = [ { id: 1, subject: "Direito Penal", topic: "Culpabilidade", question: "Questão sobre elementos da culpabilidade.", marked: "Imputabilidade apenas", correct: "Imputabilidade, potencial consciência da ilicitude e exigibilidade de conduta diversa", reason: "Confundi o conceito completo de culpabilidade com apenas um de seus elementos.", explanation: "A culpabilidade é formada por três elementos: imputabilidade, potencial consciência da ilicitude e exigibilidade de conduta diversa.", reviewDate: "2026-05-07", }, ];

const statusStyles = { "Não iniciado": "bg-slate-100 text-slate-700 border-slate-200", "Em andamento": "bg-amber-100 text-amber-700 border-amber-200", Estudado: "bg-emerald-100 text-emerald-700 border-emerald-200", };

const icons = { dashboard: "▦", edital: "▤", revisoes: "◷", questoes: "☑", erros: "✕", estudo: "⏱", book: "▣", target: "◎", plus: "+", check: "✓", trash: "🗑", cap: "◉", };

function IconBox({ children, dark = true, small = false }) { return ( <span className={inline-flex items-center justify-center shrink-0 font-black ${ small ? "h-9 w-9 rounded-xl text-base" : "h-12 w-12 rounded-2xl text-xl" } ${dark ? "bg-slate-900 text-white" : "bg-white/10 text-white"}} aria-hidden="true" > {children} </span> ); }

function Button({ children, onClick, variant = "primary", className = "", type = "button" }) { const variants = { primary: "bg-slate-900 text-white hover:bg-slate-700", light: "bg-white text-slate-950 hover:bg-slate-200", outline: "bg-white text-slate-700 border border-slate-200 hover:bg-slate-50", ghostDark: "bg-transparent text-white border border-white/30 hover:bg-white/10", };

return ( <button type={type} onClick={onClick} className={inline-flex items-center justify-center gap-2 rounded-2xl px-4 py-3 text-sm font-bold transition active:scale-[0.98] ${variants[variant]} ${className}} > {children} </button> ); }

function Card({ children, className = "" }) { return <div className={rounded-3xl border border-slate-200 bg-white shadow-sm ${className}}>{children}</div>; }

function CardContent({ children, className = "" }) { return <div className={className}>{children}</div>; }

function addDays(dateString, days) { if (!dateString) return ""; const date = new Date(${dateString}T00:00:00); date.setDate(date.getDate() + Number(days)); return date.toISOString().slice(0, 10); }

function formatDate(dateString) { if (!dateString) return "—"; const [year, month, day] = dateString.split("-"); if (!year || !month || !day) return "—"; return ${day}/${month}/${year}; }

function calculateAccuracy(correct, questions) { const total = Number(questions || 0); if (!total) return 0; return Math.round((Number(correct || 0) / total) * 100); }

function formatSeconds(totalSeconds) { const safeSeconds = Math.max(0, Number(totalSeconds || 0)); const hours = Math.floor(safeSeconds / 3600); const minutes = Math.floor((safeSeconds % 3600) / 60); const seconds = safeSeconds % 60; const pad = (value) => String(value).padStart(2, "0"); return ${pad(hours)}:${pad(minutes)}:${pad(seconds)}; }

function flattenTopics(subjects) { return subjects.flatMap((subject) => subject.topics.map((topic) => ({ ...topic, subject: subject.name })) ); }

function createReviewCycles(topic) { if (!topic.studiedAt) return []; return [ { ...topic, cycle: "7 dias", reviewDate: addDays(topic.studiedAt, 7) }, { ...topic, cycle: "14 dias", reviewDate: addDays(topic.studiedAt, 14) }, { ...topic, cycle: "21 dias", reviewDate: addDays(topic.studiedAt, 21) }, ]; }

function calculateSubjectSummary(subject, studyHistory = [], errors = []) { const topics = subject.topics || []; const studied = topics.filter((topic) => topic.status === "Estudado").length; const questions = topics.reduce((sum, topic) => sum + Number(topic.questions || 0), 0); const correct = topics.reduce((sum, topic) => sum + Number(topic.correct || 0), 0); const wrong = topics.reduce((sum, topic) => sum + Number(topic.wrong || 0), 0); const progress = topics.length ? Math.round((studied / topics.length) * 100) : 0; const accuracy = calculateAccuracy(correct, questions); const studySeconds = studyHistory .filter((session) => session.subject === subject.name) .reduce((sum, session) => sum + Number(session.durationSeconds || 0), 0); const errorCount = errors.filter((error) => error.subject === subject.name).length; const correctedErrors = errors.filter((error) => error.subject === subject.name && error.corrected).length; const improvementScore = Math.max(0, Math.min(100, Math.round(progress * 0.4 + accuracy * 0.4 + (correctedErrors / Math.max(1, errorCount)) * 20)));

return { name: subject.name, topics: topics.length, studied, questions, correct, wrong, progress, accuracy, studySeconds, errorCount, correctedErrors, improvementScore, }; }

function getTopicNeeds(topic) { const accuracy = calculateAccuracy(topic.correct, topic.questions); if (topic.status !== "Estudado") return "Estudar conteúdo"; if (topic.questions === 0) return "Fazer questões"; if (accuracy < 60) return "Reforçar teoria e corrigir erros"; if (accuracy < 75) return "Aumentar questões"; return "Manter revisão"; }

function loadFromStorage(key, fallback) { try { if (typeof window === "undefined") return fallback; const saved = window.localStorage.getItem(key); return saved ? JSON.parse(saved) : fallback; } catch (error) { console.warn(Não foi possível carregar ${key}., error); return fallback; } }

function saveToStorage(key, value) { try { if (typeof window === "undefined") return; window.localStorage.setItem(key, JSON.stringify(value)); } catch (error) { console.warn(Não foi possível salvar ${key}., error); } }

function runSmartBookTests() { console.assert(createReviewCycles({ studiedAt: "2026-04-30" }).slice(0, 3).length === 3, "O painel deve conseguir limitar a visualização para as 3 próximas revisões."); console.assert(addDays("2026-04-30", 7) === "2026-05-07", "addDays deve somar 7 dias corretamente."); console.assert(addDays("2026-04-30", 14) === "2026-05-14", "addDays deve somar 14 dias corretamente."); console.assert(addDays("2026-04-30", 21) === "2026-05-21", "addDays deve somar 21 dias corretamente."); console.assert(formatDate("2026-05-07") === "07/05/2026", "formatDate deve formatar para dd/mm/aaaa."); console.assert(formatDate(null) === "—", "formatDate deve retornar travessão para data vazia."); console.assert(calculateAccuracy(7, 10) === 70, "calculateAccuracy deve calcular 70%."); console.assert(calculateAccuracy(0, 0) === 0, "calculateAccuracy não deve dividir por zero."); console.assert(flattenTopics(initialSubjects).length === 6, "flattenTopics deve retornar todos os assuntos cadastrados."); console.assert(createReviewCycles({ studiedAt: "2026-04-30" }).length === 3, "createReviewCycles deve criar 3 revisões."); console.assert(formatSeconds(0) === "00:00:00", "formatSeconds deve formatar zero segundo."); console.assert(formatSeconds(3661) === "01:01:01", "formatSeconds deve formatar horas, minutos e segundos."); const penalSummary = calculateSubjectSummary(initialSubjects[0], [], initialErrors); console.assert(penalSummary.questions === 28, "calculateSubjectSummary deve somar as questões da matéria."); console.assert(penalSummary.progress === 33, "calculateSubjectSummary deve calcular o progresso por matéria."); console.assert(getTopicNeeds({ status: "Estudado", questions: 10, correct: 5 }) === "Reforçar teoria e corrigir erros", "getTopicNeeds deve indicar reforço quando o aproveitamento é baixo."); }

runSmartBookTests();

function StatCard({ icon, title, value, subtitle }) { return ( <Card className="rounded-2xl"> <CardContent className="p-5"> <div className="flex items-center gap-4"> <IconBox>{icon}</IconBox> <div> <p className="text-sm text-slate-500">{title}</p> <p className="text-2xl font-bold text-slate-900">{value}</p> <p className="text-xs text-slate-400">{subtitle}</p> </div> </div> </CardContent> </Card> ); }

function SectionTitle({ icon, title, description }) { return ( <div className="mb-5 flex items-start gap-3"> <IconBox small={false}>{icon}</IconBox> <div> <h2 className="text-2xl font-bold text-slate-900">{title}</h2> <p className="mt-1 text-sm text-slate-500">{description}</p> </div> </div> ); }

function EmptyState({ title, text }) { return ( <div className="rounded-3xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center"> <p className="text-lg font-bold text-slate-800">{title}</p> <p className="mt-2 text-sm text-slate-500">{text}</p> </div> ); }

export default function SmartBookSite() { const [activeTab, setActiveTab] = useState("dashboard"); const [subjects, setSubjects] = useState(() => loadFromStorage("smartbook_subjects", initialSubjects)); const [errors, setErrors] = useState(() => loadFromStorage("smartbook_errors", initialErrors)); const [newSubject, setNewSubject] = useState(""); const [newTopic, setNewTopic] = useState(""); const [selectedSubjectId, setSelectedSubjectId] = useState(1); const [selectedDashboardSubjectId, setSelectedDashboardSubjectId] = useState(1); const [questionForm, setQuestionForm] = useState({ subject: "Direito Penal", topic: "Teoria do Crime", questions: 10, correct: 7, wrong: 3, reason: "", explanation: "", }); const [studySession, setStudySession] = useState({ subject: "Direito Penal", topic: "Teoria do Crime", seconds: 0, running: false, pausedSeconds: 0, pauses: 0, startedAt: null, }); const [studyHistory, setStudyHistory] = useState(() => loadFromStorage("smartbook_study_history", [ { id: 1, subject: "Português", topic: "Interpretação de Texto", durationSeconds: 2700, pauses: 1, date: "2026-04-30", }, ]) );

const allTopics = useMemo(() => flattenTopics(subjects), [subjects]); const studiedTopics = allTopics.filter((topic) => topic.status === "Estudado"); const totalQuestions = allTopics.reduce((sum, topic) => sum + Number(topic.questions || 0), 0); const totalCorrect = allTopics.reduce((sum, topic) => sum + Number(topic.correct || 0), 0); const totalWrong = allTopics.reduce((sum, topic) => sum + Number(topic.wrong || 0), 0); const progress = allTopics.length ? Math.round((studiedTopics.length / allTopics.length) * 100) : 0; const accuracy = calculateAccuracy(totalCorrect, totalQuestions); const reviews = studiedTopics.flatMap(createReviewCycles); const totalStudySeconds = studyHistory.reduce((sum, item) => sum + Number(item.durationSeconds || 0), 0) + studySession.seconds; const subjectSummaries = subjects.map((subject) => calculateSubjectSummary(subject, studyHistory, errors)); const selectedDashboardSubject = subjects.find((subject) => subject.id === Number(selectedDashboardSubjectId)) || subjects[0]; const selectedSubjectSummary = selectedDashboardSubject ? calculateSubjectSummary(selectedDashboardSubject, studyHistory, errors) : null; const selectedSubjectErrors = errors.filter((error) => error.subject === selectedDashboardSubject?.name); const selectedSubjectReviews = reviews.filter((review) => review.subject === selectedDashboardSubject?.name); const strongestSubject = subjectSummaries.length ? subjectSummaries.reduce((best, current) => (current.accuracy > best.accuracy ? current : best), subjectSummaries[0]) : null; const attentionSubject = subjectSummaries.length ? subjectSummaries.reduce((worst, current) => (current.improvementScore < worst.improvementScore ? current : worst), subjectSummaries[0]) : null;

const currentSubject = subjects.find((subject) => subject.name === questionForm.subject) || subjects[0]; const topicOptions = currentSubject?.topics || []; const currentStudySubject = subjects.find((subject) => subject.name === studySession.subject) || subjects[0]; const studyTopicOptions = currentStudySubject?.topics || [];

useEffect(() => { saveToStorage("smartbook_subjects", subjects); }, [subjects]);

useEffect(() => { saveToStorage("smartbook_errors", errors); }, [errors]);

useEffect(() => { saveToStorage("smartbook_study_history", studyHistory); }, [studyHistory]);

useEffect(() => { if (!studySession.running) return; const intervalId = window.setInterval(() => { setStudySession((current) => ({ ...current, seconds: current.seconds + 1 })); }, 1000); return () => window.clearInterval(intervalId); }, [studySession.running]);

function addSubject() { const name = newSubject.trim(); if (!name) return; const nextSubject = { id: Date.now(), name, topics: [] }; setSubjects((current) => [...current, nextSubject]); setSelectedSubjectId(nextSubject.id); setNewSubject(""); setQuestionForm((current) => ({ ...current, subject: name, topic: "" })); }

function addTopic() { const name = newTopic.trim(); if (!name) return; setSubjects((current) => current.map((subject) => subject.id === Number(selectedSubjectId) ? { ...subject, topics: [ ...subject.topics, { id: Date.now(), name, status: "Não iniciado", studiedAt: null, questions: 0, correct: 0, wrong: 0, }, ], } : subject ) ); const subjectName = subjects.find((subject) => subject.id === Number(selectedSubjectId))?.name || questionForm.subject; setQuestionForm((current) => ({ ...current, subject: subjectName, topic: name })); setNewTopic(""); }

function markAsStudied(subjectId, topicId) { const today = new Date().toISOString().slice(0, 10); setSubjects((current) => current.map((subject) => subject.id === subjectId ? { ...subject, topics: subject.topics.map((topic) => topic.id === topicId ? { ...topic, status: "Estudado", studiedAt: today } : topic ), } : subject ) ); }

function registerQuestions() { const wrong = Math.max(0, Number(questionForm.wrong || 0)); const questionCount = Math.max(0, Number(questionForm.questions || 0)); const correct = Math.max(0, Number(questionForm.correct || 0)); const selectedTopicName = questionForm.topic || topicOptions[0]?.name;

if (!questionForm.subject || !selectedTopicName || questionCount === 0) return;

setSubjects((current) =>
  current.map((subject) =>
    subject.name === questionForm.subject
      ? {
          ...subject,
          topics: subject.topics.map((topic) =>
            topic.name === selectedTopicName
              ? {
                  ...topic,
                  questions: Number(topic.questions || 0) + questionCount,
                  correct: Number(topic.correct || 0) + correct,
                  wrong: Number(topic.wrong || 0) + wrong,
                }
              : topic
          ),
        }
      : subject
  )
);

if (wrong > 0) {
  setErrors((current) => [
    {
      id: Date.now(),
      subject: questionForm.subject,
      topic: selectedTopicName,
      question: "Registro de questão errada inserido pelo aluno.",
      marked: "Resposta marcada pelo aluno",
      correct: "Resposta correta a preencher",
      reason: questionForm.reason || "Descrever por que errou.",
      explanation: questionForm.explanation || "Adicionar explicação correta.",
      reviewDate: addDays(new Date().toISOString().slice(0, 10), 7),
    },
    ...current,
  ]);
}

setQuestionForm((current) => ({ ...current, reason: "", explanation: "" }));

}

function removeError(id) { setErrors((current) => current.filter((error) => error.id !== id)); }

function updateStudySubject(subjectName) { const subject = subjects.find((item) => item.name === subjectName); setStudySession((current) => ({ ...current, subject: subjectName, topic: subject?.topics?.[0]?.name || "", })); }

function startStudySession() { if (!studySession.subject || !studySession.topic) return; setStudySession((current) => ({ ...current, running: true, startedAt: current.startedAt || new Date().toISOString(), })); }

function pauseStudySession() { setStudySession((current) => ({ ...current, running: false, pauses: current.pauses + 1, })); }

function resetStudySession() { setStudySession((current) => ({ ...current, seconds: 0, running: false, pauses: 0, startedAt: null, })); }

function saveStudySession() { if (!studySession.subject || !studySession.topic || studySession.seconds === 0) return; const today = new Date().toISOString().slice(0, 10); setStudyHistory((current) => [ { id: Date.now(), subject: studySession.subject, topic: studySession.topic, durationSeconds: studySession.seconds, pauses: studySession.pauses, date: today, }, ...current, ]); resetStudySession(); }

function updateQuestionSubject(subjectName) { const subject = subjects.find((item) => item.name === subjectName); setQuestionForm((current) => ({ ...current, subject: subjectName, topic: subject?.topics?.[0]?.name || "", })); }

function resetAllData() { const confirmReset = window.confirm("Tem certeza que deseja apagar os dados salvos e voltar ao exemplo inicial?"); if (!confirmReset) return; setSubjects(initialSubjects); setErrors(initialErrors); setStudyHistory([ { id: 1, subject: "Português", topic: "Interpretação de Texto", durationSeconds: 2700, pauses: 1, date: "2026-04-30", }, ]); resetStudySession(); }

const tabs = [ { id: "dashboard", label: "Painel", icon: icons.dashboard }, { id: "edital", label: "Meu Edital", icon: icons.edital }, { id: "estudo", label: "Sessão de Estudo", icon: icons.estudo }, { id: "revisoes", label: "Revisões", icon: icons.revisoes }, { id: "questoes", label: "Questões", icon: icons.questoes }, { id: "erros", label: "Caderno de Erros", icon: icons.erros }, ];

return ( <div className="min-h-screen bg-slate-50 text-slate-900"> <header className="overflow-hidden bg-slate-950 text-white"> <div className="mx-auto grid max-w-7xl items-center gap-10 px-5 py-10 md:grid-cols-2 md:py-16"> <div> <div className="mb-5 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-sm"> <span>{icons.cap}</span> Método de revisão inteligente </div> <h1 className="text-4xl font-black leading-tight tracking-tight md:text-6xl">SmartBook</h1> <p className="mt-3 text-xl text-slate-300 md:text-2xl">Estude com método, revise com inteligência.</p>

<div className="mt-7 flex flex-wrap gap-3">
          <Button onClick={() => setActiveTab("edital")} variant="light" className="px-6 py-4">
            Meu edital
          </Button>
          <Button onClick={resetAllData} variant="ghostDark" className="px-6 py-4">
            Reiniciar dados
          </Button>
        </div>
      </div>

      <Card className="border-0 bg-white text-slate-900 shadow-2xl">
        <CardContent className="p-6 md:p-8">
          <p className="text-sm font-semibold text-slate-500">Resumo inteligente</p>
          <div className="mt-5 space-y-5">
            <div>
              <div className="mb-2 flex justify-between text-sm">
                <span>Progresso</span>
                <span className="font-bold">{progress}%</span>
              </div>
              <div className="h-3 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-slate-900 transition-all" style={{ width: `${progress}%` }} />
              </div>
            </div>
            <div className="grid grid-cols-4 gap-3">
              <div className="rounded-2xl bg-slate-100 p-4 text-center">
                <p className="text-2xl font-bold">{subjects.length}</p>
                <p className="text-xs text-slate-500">matérias</p>
              </div>
              <div className="rounded-2xl bg-slate-100 p-4 text-center">
                <p className="text-2xl font-bold">{reviews.length}</p>
                <p className="text-xs text-slate-500">revisões</p>
              </div>
              <div className="rounded-2xl bg-slate-100 p-4 text-center">
                <p className="text-2xl font-bold">{errors.length}</p>
                <p className="text-xs text-slate-500">erros</p>
              </div>
              <div className="rounded-2xl bg-slate-100 p-4 text-center">
                <p className="text-2xl font-bold">{formatSeconds(totalStudySeconds).slice(0, 5)}</p>
                <p className="text-xs text-slate-500">estudo</p>
              </div>
            </div>
            <div className="rounded-2xl border border-slate-200 p-4">
              <p className="text-sm text-slate-500">Hoje o foco é:</p>
              <p className="mt-1 font-semibold">Revisar conteúdos pendentes e corrigir o caderno de erros.</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </header>

  <main className="mx-auto max-w-7xl px-5 py-8">
    <nav className="mb-7 flex gap-2 overflow-x-auto pb-3">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`flex items-center gap-2 whitespace-nowrap rounded-2xl px-4 py-3 text-sm font-semibold transition ${
            activeTab === tab.id
              ? "bg-slate-900 text-white shadow"
              : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
          }`}
        >
          <span className="font-black">{tab.icon}</span> {tab.label}
        </button>
      ))}
    </nav>

    {activeTab === "dashboard" && (
      <section>
        <SectionTitle icon={icons.dashboard} title="Painel de Estudos" description="Acompanhe o edital como um todo e depois veja a evolução separada por matéria e assunto." />
        <div className="mb-7 grid gap-4 md:grid-cols-5">
          <StatCard icon={icons.book} title="Assuntos" value={allTopics.length} subtitle={`${studiedTopics.length} estudados`} />
          <StatCard icon={icons.target} title="Progresso" value={`${progress}%`} subtitle="" />
          <StatCard icon={icons.estudo} title="Tempo" value={formatSeconds(totalStudySeconds).slice(0, 5)} subtitle="estudado" />
          <StatCard icon={icons.questoes} title="Questões" value={totalQuestions} subtitle={`${accuracy}% de acerto`} />
          <StatCard icon={icons.erros} title="Erros" value={totalWrong} subtitle="para corrigir" />
        </div>

        <div className="mb-7 grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <CardContent className="p-6">
              <div className="mb-5 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="text-xl font-bold">Dashboard do edital</h3>
                  <p className="text-sm text-slate-500">Visão geral da sua preparação.</p>
                </div>
                <span className="rounded-full bg-slate-900 px-4 py-2 text-sm font-bold text-white">{progress}% concluído</span>
              </div>
              <div className="mb-5 h-4 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-slate-900 transition-all" style={{ width: `${progress}%` }} />
              </div>
              <div className="grid gap-3 md:grid-cols-4">
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Matérias</p>
                  <p className="text-2xl font-black">{subjects.length}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Tempo total</p>
                  <p className="text-2xl font-black">{formatSeconds(totalStudySeconds).slice(0, 5)}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Acertos</p>
                  <p className="text-2xl font-black">{totalCorrect}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Erros</p>
                  <p className="text-2xl font-black">{totalWrong}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Leitura inteligente</h3>
              <div className="space-y-3">
                <div className="rounded-2xl bg-emerald-50 p-4 text-sm">
                  <p className="font-bold text-emerald-800">Melhor desempenho</p>
                  <p className="mt-1 text-slate-700">{strongestSubject ? `${strongestSubject.name} • ${strongestSubject.accuracy}% de acerto` : "Sem dados suficientes"}</p>
                </div>
                <div className="rounded-2xl bg-amber-50 p-4 text-sm">
                  <p className="font-bold text-amber-800">Ponto de atenção</p>
                  <p className="mt-1 text-slate-700">{attentionSubject ? `${attentionSubject.name} precisa de mais revisão e questões.` : "Sem dados suficientes"}</p>
                </div>
                <div className="rounded-2xl bg-slate-50 p-4 text-sm">
                  <p className="font-bold text-slate-800">Progresso real</p>
                  <p className="mt-1 text-slate-700">O painel combina avanço no edital, tempo estudado, questões, acertos, erros e correções.</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="mb-7 grid gap-6 lg:grid-cols-2">
          <Card>
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Dashboard por matéria</h3>
              <div className="space-y-4">
                {subjectSummaries.map((summary) => (
                  <button
                    key={summary.name}
                    onClick={() => setSelectedDashboardSubjectId(subjects.find((subject) => subject.name === summary.name)?.id || selectedDashboardSubjectId)}
                    className={`w-full rounded-3xl border p-4 text-left transition hover:bg-slate-50 ${selectedDashboardSubject?.name === summary.name ? "border-slate-900 bg-slate-50" : "border-slate-200 bg-white"}`}
                  >
                    <div className="mb-3 flex items-center justify-between gap-3">
                      <div>
                        <p className="font-bold">{summary.name}</p>
                        <p className="text-sm text-slate-500">{summary.studied}/{summary.topics} assuntos estudados</p>
                      </div>
                      <span className="rounded-full bg-slate-900 px-3 py-2 text-sm font-bold text-white">{summary.progress}%</span>
                    </div>
                    <div className="mb-3 h-2 overflow-hidden rounded-full bg-slate-200">
                      <div className="h-full rounded-full bg-slate-900" style={{ width: `${summary.progress}%` }} />
                    </div>
                    <div className="grid grid-cols-4 gap-2 text-center text-xs">
                      <div className="rounded-xl bg-slate-100 p-2">
                        <p className="font-black text-slate-900">{summary.questions}</p>
                        <p className="text-slate-500">questões</p>
                      </div>
                      <div className="rounded-xl bg-slate-100 p-2">
                        <p className="font-black text-slate-900">{summary.accuracy}%</p>
                        <p className="text-slate-500">acerto</p>
                      </div>
                      <div className="rounded-xl bg-slate-100 p-2">
                        <p className="font-black text-slate-900">{formatSeconds(summary.studySeconds).slice(0, 5)}</p>
                        <p className="text-slate-500">tempo</p>
                      </div>
                      <div className="rounded-xl bg-slate-100 p-2">
                        <p className="font-black text-slate-900">{summary.improvementScore}%</p>
                        <p className="text-slate-500">melhoria</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="mb-4 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="text-xl font-bold">Detalhe da matéria</h3>
                  <p className="text-sm text-slate-500">{selectedDashboardSubject?.name}</p>
                </div>
                <select
                  value={selectedDashboardSubjectId}
                  onChange={(event) => setSelectedDashboardSubjectId(Number(event.target.value))}
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm"
                >
                  {subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}
                </select>
              </div>

              {selectedSubjectSummary && (
                <div className="mb-5 grid grid-cols-2 gap-3 md:grid-cols-4">
                  <div className="rounded-2xl bg-slate-50 p-4">
                    <p className="text-xs text-slate-500">Questões</p>
                    <p className="text-xl font-black">{selectedSubjectSummary.questions}</p>
                  </div>
                  <div className="rounded-2xl bg-slate-50 p-4">
                    <p className="text-xs text-slate-500">Acertos</p>
                    <p className="text-xl font-black">{selectedSubjectSummary.correct}</p>
                  </div>
                  <div className="rounded-2xl bg-slate-50 p-4">
                    <p className="text-xs text-slate-500">Erros</p>
                    <p className="text-xl font-black">{selectedSubjectSummary.wrong}</p>
                  </div>
                  <div className="rounded-2xl bg-slate-50 p-4">
                    <p className="text-xs text-slate-500">Corrigidos</p>
                    <p className="text-xl font-black">{selectedSubjectSummary.correctedErrors}</p>
                  </div>
                </div>
              )}

              <h4 className="mb-3 font-bold">Assuntos da matéria</h4>
              <div className="space-y-3">
                {selectedDashboardSubject?.topics.map((topic) => {
                  const topicAccuracy = calculateAccuracy(topic.correct, topic.questions);
                  return (
                    <div key={topic.id} className="rounded-2xl border border-slate-200 p-4">
                      <div className="mb-2 flex items-center justify-between gap-3">
                        <div>
                          <p className="font-semibold">{topic.name}</p>
                          <p className="text-xs text-slate-500">{getTopicNeeds(topic)}</p>
                        </div>
                        <span className={`rounded-full border px-3 py-2 text-xs font-bold ${statusStyles[topic.status]}`}>{topic.status}</span>
                      </div>
                      <div className="grid grid-cols-4 gap-2 text-center text-xs">
                        <div className="rounded-xl bg-slate-100 p-2"><strong>{topic.questions}</strong><br />questões</div>
                        <div className="rounded-xl bg-slate-100 p-2"><strong>{topic.correct}</strong><br />acertos</div>
                        <div className="rounded-xl bg-slate-100 p-2"><strong>{topic.wrong}</strong><br />erros</div>
                        <div className="rounded-xl bg-slate-100 p-2"><strong>{topicAccuracy}%</strong><br />acerto</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Próximas revisões</h3>
              {reviews.length === 0 ? (
                <EmptyState title="Nenhuma revisão ainda" text="Marque um assunto como estudado para gerar ciclos de 7, 14 e 21 dias." />
              ) : (
                <div className="space-y-3">
                  {reviews.slice(0, 3).map((review, index) => (
                    <div key={`${review.id}-${review.cycle}-${index}`} className="flex items-center justify-between rounded-2xl bg-slate-100 p-4">
                      <div>
                        <p className="font-semibold">{review.name}</p>
                        <p className="text-sm text-slate-500">{review.subject} • ciclo de {review.cycle}</p>
                      </div>
                      <span className="text-sm font-bold">{formatDate(review.reviewDate)}</span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Caderno de erros</h3>
              {errors.length === 0 ? (
                <EmptyState title="Nenhum erro registrado" text="Quando uma questão tiver erro, ela aparecerá aqui automaticamente." />
              ) : (
                <div className="space-y-3">
                  {errors.slice(0, 4).map((error) => (
                    <div key={error.id} className="rounded-2xl border border-slate-200 p-4">
                      <p className="font-semibold">{error.topic}</p>
                      <p className="text-sm text-slate-500">{error.subject}</p>
                      <p className="mt-2 text-sm">{error.reason}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </section>
    )}

    {activeTab === "edital" && (
      <section>
        <SectionTitle icon={icons.edital} title="Meu Edital" description="Cadastre matérias e assuntos do edital para transformar o conteúdo em plano de estudo." />
        <div className="grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-1">
            <CardContent className="space-y-5 p-6">
              <div>
                <label className="text-sm font-semibold">Nova matéria</label>
                <div className="mt-2 flex gap-2">
                  <input
                    value={newSubject}
                    onChange={(event) => setNewSubject(event.target.value)}
                    placeholder="Ex.: Direito Administrativo"
                    className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:ring-2 focus:ring-slate-900"
                  />
                  <Button onClick={addSubject} className="px-4">
                    {icons.plus}
                  </Button>
                </div>
              </div>
              <div>
                <label className="text-sm font-semibold">Novo assunto</label>
                <select
                  value={selectedSubjectId}
                  onChange={(event) => setSelectedSubjectId(Number(event.target.value))}
                  className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3"
                >
                  {subjects.map((subject) => (
                    <option key={subject.id} value={subject.id}>{subject.name}</option>
                  ))}
                </select>
                <div className="mt-2 flex gap-2">
                  <input
                    value={newTopic}
                    onChange={(event) => setNewTopic(event.target.value)}
                    placeholder="Ex.: Atos Administrativos"
                    className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:ring-2 focus:ring-slate-900"
                  />
                  <Button onClick={addTopic} className="px-4">
                    {icons.plus}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="lg:col-span-2">
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Matérias e assuntos cadastrados</h3>
              <div className="space-y-5">
                {subjects.map((subject) => (
                  <div key={subject.id} className="rounded-3xl border border-slate-200 bg-white p-5">
                    <h4 className="mb-3 text-lg font-bold">{subject.name}</h4>
                    {subject.topics.length === 0 ? (
                      <EmptyState title="Sem assuntos" text="Cadastre os tópicos dessa matéria para iniciar o acompanhamento." />
                    ) : (
                      <div className="space-y-3">
                        {subject.topics.map((topic) => (
                          <div key={topic.id} className="flex flex-col justify-between gap-3 rounded-2xl bg-slate-50 p-4 md:flex-row md:items-center">
                            <div>
                              <p className="font-semibold">{topic.name}</p>
                              <p className="text-sm text-slate-500">Questões: {topic.questions} • Acertos: {topic.correct} • Erros: {topic.wrong}</p>
                            </div>
                            <div className="flex flex-wrap items-center gap-2">
                              <span className={`rounded-full border px-3 py-2 text-xs font-bold ${statusStyles[topic.status]}`}>{topic.status}</span>
                              <Button onClick={() => markAsStudied(subject.id, topic.id)} variant="outline">
                                {icons.check} Estudado
                              </Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    )}

    {activeTab === "estudo" && (
      <section>
        <SectionTitle icon={icons.estudo} title="Sessão de Estudo" description="Escolha a matéria, inicie o cronômetro, pause quando precisar e salve o tempo estudado." />
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardContent className="space-y-5 p-6">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="text-sm font-semibold">Matéria em estudo</label>
                  <select
                    value={studySession.subject}
                    onChange={(event) => updateStudySubject(event.target.value)}
                    disabled={studySession.running}
                    className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 disabled:bg-slate-100"
                  >
                    {subjects.map((subject) => (
                      <option key={subject.id}>{subject.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-sm font-semibold">Assunto</label>
                  <select
                    value={studySession.topic}
                    onChange={(event) => setStudySession({ ...studySession, topic: event.target.value })}
                    disabled={studySession.running}
                    className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 disabled:bg-slate-100"
                  >
                    {studyTopicOptions.length === 0 ? (
                      <option value="">Cadastre um assunto primeiro</option>
                    ) : (
                      studyTopicOptions.map((topic) => <option key={topic.id}>{topic.name}</option>)
                    )}
                  </select>
                </div>
              </div>

              <div className="rounded-3xl bg-slate-950 p-8 text-center text-white">
                <p className="text-sm text-slate-400">Tempo da sessão</p>
                <p className="mt-3 text-5xl font-black tracking-tight md:text-6xl">{formatSeconds(studySession.seconds)}</p>
                <p className="mt-3 text-sm text-slate-400">
                  {studySession.running ? "Cronômetro em andamento" : studySession.seconds > 0 ? "Sessão pausada" : "Pronto para iniciar"}
                </p>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="rounded-2xl bg-slate-100 p-4 text-center">
                  <p className="text-xl font-bold">{studySession.pauses}</p>
                  <p className="text-xs text-slate-500">pausas</p>
                </div>
                <div className="rounded-2xl bg-slate-100 p-4 text-center">
                  <p className="text-xl font-bold">{studySession.subject}</p>
                  <p className="text-xs text-slate-500">matéria</p>
                </div>
                <div className="rounded-2xl bg-slate-100 p-4 text-center">
                  <p className="text-xl font-bold">{formatSeconds(totalStudySeconds).slice(0, 5)}</p>
                  <p className="text-xs text-slate-500">total</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                {!studySession.running ? (
                  <Button onClick={startStudySession} className="flex-1 py-4" disabled={!studySession.topic}>
                    Iniciar / Retomar
                  </Button>
                ) : (
                  <Button onClick={pauseStudySession} className="flex-1 py-4">
                    Pausar
                  </Button>
                )}
                <Button onClick={saveStudySession} variant="outline" className="flex-1 py-4">
                  Salvar sessão
                </Button>
                <Button onClick={resetStudySession} variant="outline" className="flex-1 py-4">
                  Zerar
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Histórico de estudo</h3>
              {studyHistory.length === 0 ? (
                <EmptyState title="Nenhuma sessão salva" text="Quando você salvar uma sessão, ela aparecerá aqui com matéria, assunto e duração." />
              ) : (
                <div className="space-y-3">
                  {studyHistory.map((session) => (
                    <div key={session.id} className="rounded-2xl border border-slate-200 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="font-semibold">{session.subject}</p>
                          <p className="text-sm text-slate-500">{session.topic} • {formatDate(session.date)}</p>
                        </div>
                        <span className="rounded-full bg-slate-900 px-3 py-2 text-sm font-bold text-white">{formatSeconds(session.durationSeconds)}</span>
                      </div>
                      <p className="mt-2 text-xs text-slate-500">Pausas registradas: {session.pauses}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </section>
    )}

    {activeTab === "revisoes" && (
      <section>
        <SectionTitle icon={icons.revisoes} title="Revisões 7-14-21" description="Toda vez que um assunto é marcado como estudado, o SmartBook agenda três revisões automáticas." />
        <Card>
          <CardContent className="p-6">
            {reviews.length === 0 ? (
              <EmptyState title="Nenhuma revisão programada" text="Marque um assunto como estudado para o sistema criar as revisões." />
            ) : (
              <div className="grid gap-4 md:grid-cols-3">
                {reviews.map((review, index) => (
                  <div key={`${review.id}-${review.cycle}-${index}`} className="rounded-3xl border border-slate-200 bg-white p-5">
                    <div className="mb-4 flex items-center justify-between">
                      <span className="rounded-full bg-slate-900 px-3 py-2 text-xs font-bold text-white">{review.cycle}</span>
                      <span className="text-xl text-slate-400">{icons.revisoes}</span>
                    </div>
                    <h3 className="text-lg font-bold">{review.name}</h3>
                    <p className="text-sm text-slate-500">{review.subject}</p>
                    <p className="mt-4 text-sm">Revisar em:</p>
                    <p className="text-xl font-black">{formatDate(review.reviewDate)}</p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </section>
    )}

    {activeTab === "questoes" && (
      <section>
        <SectionTitle icon={icons.questoes} title="Questões Feitas" description="Acompanhe seu desempenho por assunto. Na versão com banco de questões, os erros serão enviados automaticamente para o caderno de erros." />
        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardContent className="space-y-4 p-6">
              <div>
                <label className="text-sm font-semibold">Matéria</label>
                <select
                  value={questionForm.subject}
                  onChange={(event) => updateQuestionSubject(event.target.value)}
                  className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3"
                >
                  {subjects.map((subject) => (
                    <option key={subject.id}>{subject.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-semibold">Assunto</label>
                <select
                  value={questionForm.topic}
                  onChange={(event) => setQuestionForm({ ...questionForm, topic: event.target.value })}
                  className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3"
                >
                  {topicOptions.length === 0 ? (
                    <option value="">Cadastre um assunto primeiro</option>
                  ) : (
                    topicOptions.map((topic) => <option key={topic.id}>{topic.name}</option>)
                  )}
                </select>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-sm font-semibold">Questões</label>
                  <input type="number" min="0" value={questionForm.questions} onChange={(event) => setQuestionForm({ ...questionForm, questions: event.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
                </div>
                <div>
                  <label className="text-sm font-semibold">Acertos</label>
                  <input type="number" min="0" value={questionForm.correct} onChange={(event) => setQuestionForm({ ...questionForm, correct: event.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
                </div>
                <div>
                  <label className="text-sm font-semibold">Erros</label>
                  <input type="number" min="0" value={questionForm.wrong} onChange={(event) => setQuestionForm({ ...questionForm, wrong: event.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3" />
                </div>
              </div>
              <div>
                <label className="text-sm font-semibold">Por que errou?</label>
                <textarea
                  value={questionForm.reason}
                  onChange={(event) => setQuestionForm({ ...questionForm, reason: event.target.value })}
                  placeholder="Ex.: confundi o conceito, não li o enunciado, esqueci a regra..."
                  className="mt-2 min-h-24 w-full rounded-2xl border border-slate-200 px-4 py-3"
                />
              </div>
              <div>
                <label className="text-sm font-semibold">Explicação correta</label>
                <textarea
                  value={questionForm.explanation}
                  onChange={(event) => setQuestionForm({ ...questionForm, explanation: event.target.value })}
                  placeholder="Escreva a explicação correta para revisar depois."
                  className="mt-2 min-h-24 w-full rounded-2xl border border-slate-200 px-4 py-3"
                />
              </div>
              <Button onClick={registerQuestions} className="w-full py-4">
                Salvar desempenho
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <h3 className="mb-4 text-xl font-bold">Desempenho por assunto</h3>
              <div className="space-y-3">
                {allTopics.map((topic) => {
                  const topicAccuracy = calculateAccuracy(topic.correct, topic.questions);
                  return (
                    <div key={`${topic.subject}-${topic.id}`} className="rounded-2xl bg-slate-50 p-4">
                      <div className="mb-2 flex justify-between">
                        <div>
                          <p className="font-semibold">{topic.name}</p>
                          <p className="text-sm text-slate-500">{topic.subject}</p>
                        </div>
                        <span className="font-bold">{topicAccuracy}%</span>
                      </div>
                      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
                        <div className="h-full rounded-full bg-slate-900 transition-all" style={{ width: `${topicAccuracy}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    )}

    {activeTab === "erros" && (
      <section>
        <SectionTitle icon={icons.erros} title="Caderno de Erros" description="Aqui ficam as questões erradas, com espaço para explicar o motivo do erro e revisar depois." />
        {errors.length === 0 ? (
          <EmptyState title="Seu caderno de erros está vazio" text="Registre questões com erro para criar revisões direcionadas." />
        ) : (
          <div className="grid gap-5 md:grid-cols-2">
            {errors.map((error) => (
              <Card key={error.id}>
                <CardContent className="p-6">
                  <div className="mb-4 flex items-start justify-between gap-4">
                    <div>
                      <span className="rounded-full bg-red-100 px-3 py-2 text-xs font-bold text-red-700">Erro registrado</span>
                      <h3 className="mt-4 text-xl font-bold">{error.topic}</h3>
                      <p className="text-sm text-slate-500">{error.subject}</p>
                    </div>
                    <button onClick={() => removeError(error.id)} className="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-100 transition hover:bg-red-100 hover:text-red-700">
                      {icons.trash}
                    </button>
                  </div>
                  <div className="space-y-3 text-sm">
                    <div className="rounded-2xl bg-slate-50 p-4">
                      <p className="font-semibold">Questão</p>
                      <p className="mt-1 text-slate-600">{error.question}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div className="rounded-2xl bg-slate-50 p-4">
                        <p className="font-semibold">Marquei</p>
                        <p className="mt-1 text-slate-600">{error.marked}</p>
                      </div>
                      <div className="rounded-2xl bg-slate-50 p-4">
                        <p className="font-semibold">Correto</p>
                        <p className="mt-1 text-slate-600">{error.correct}</p>
                      </div>
                    </div>
                    <div className="rounded-2xl border border-amber-100 bg-amber-50 p-4">
                      <p className="font-semibold">Por que errei?</p>
                      <p className="mt-1 text-slate-700">{error.reason}</p>
                    </div>
                    <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4">
                      <p className="font-semibold">Explicação correta</p>
                      <p className="mt-1 text-slate-700">{error.explanation}</p>
                    </div>
                    <div className="flex items-center justify-between rounded-2xl bg-slate-900 p-4 text-white">
                      <span>Revisar em</span>
                      <strong>{formatDate(error.reviewDate)}</strong>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </section>
    )}
  </main>
</div>

); }
