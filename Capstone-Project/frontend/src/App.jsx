import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import gsap from 'gsap';

const STATUSES = ['TODO', 'IN_PROGRESS', 'DONE'];
const INITIAL_TASKS = [
  { id: 1, title: 'Audit container image layers', status: 'TODO', priority: 'HIGH', owner: 'AK', age: '12m' },
  { id: 2, title: 'Rotate staging credentials', status: 'TODO', priority: 'MED', owner: 'RS', age: '28m' },
  { id: 3, title: 'Add health probe to API', status: 'IN_PROGRESS', priority: 'HIGH', owner: 'NV', age: '1h' },
  { id: 4, title: 'Document rollback path', status: 'IN_PROGRESS', priority: 'LOW', owner: 'AK', age: '2h' },
  { id: 5, title: 'Prometheus scrape verified', status: 'DONE', priority: 'DONE', owner: 'RS', age: '3h' },
  { id: 6, title: 'Frontend image promoted', status: 'DONE', priority: 'DONE', owner: 'NV', age: '5h' },
];
const STATUS_LABELS = { TODO: 'Queue', IN_PROGRESS: 'Active', DONE: 'Shipped' };

export default function App() {
  const [tasks, setTasks] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem('taskboard.tasks'));
      return Array.isArray(saved) ? saved : INITIAL_TASKS;
    } catch {
      return INITIAL_TASKS;
    }
  });
  const [title, setTitle] = useState('');
  const [filter, setFilter] = useState('ALL');
  const boardRef = useRef(null);

  useEffect(() => {
    try {
      localStorage.setItem('taskboard.tasks', JSON.stringify(tasks));
    } catch {
      // Persistence is best-effort when browser storage is unavailable.
    }
  }, [tasks]);

  useLayoutEffect(() => {
    const context = gsap.context(() => {
      gsap.from('.topbar, .workspace-head, .metric-strip, .command-bar, .board-shell', { y: 16, opacity: 0, duration: 0.55, stagger: 0.08, ease: 'power2.out' });
      gsap.from('.task-card', { y: 12, opacity: 0, duration: 0.45, stagger: 0.06, delay: 0.3, ease: 'power2.out' });
      gsap.to('.signal-dot', { opacity: 0.25, repeat: -1, yoyo: true, duration: 1.1, ease: 'sine.inOut' });
      gsap.to('.pulse-line', { scaleX: 0.35, transformOrigin: 'left center', repeat: -1, yoyo: true, duration: 1.4, ease: 'sine.inOut' });
    });
    return () => context.revert();
  }, []);

  const addTask = (event) => {
    event.preventDefault();
    if (!title.trim()) return;
    const newId = Date.now();
    setTasks((current) => [{ id: newId, title: title.trim(), status: 'TODO', priority: 'NEW', owner: 'YOU', age: 'now' }, ...current]);
    setTitle('');
    requestAnimationFrame(() => gsap.from(`[data-task-id="${newId}"]`, { y: -14, opacity: 0, scale: 0.98, duration: 0.45, ease: 'power2.out' }));
  };

  const updateStatus = (id, status) => {
    setTasks((current) => current.map((task) => task.id === id ? { ...task, status } : task));
    requestAnimationFrame(() => gsap.from(`[data-task-id="${id}"]`, { x: 12, opacity: 0, duration: 0.35, ease: 'power2.out' }));
  };

  const removeTask = (id) => {
    const card = document.querySelector(`[data-task-id="${id}"]`);
    if (!card) return;
    gsap.to(card, { height: 0, opacity: 0, marginBottom: 0, paddingTop: 0, paddingBottom: 0, duration: 0.25, onComplete: () => setTasks((current) => current.filter((task) => task.id !== id)) });
  };

  const visibleTasks = filter === 'ALL' ? tasks : tasks.filter((task) => task.status === filter);
  const doneCount = tasks.filter((task) => task.status === 'DONE').length;

  return <main ref={boardRef}>
    <nav className="topbar" aria-label="Primary navigation"><div className="brand"><span className="brand-mark">//</span> TASKBOARD <span className="brand-version">v0.9.4</span></div><div className="system-status"><span className="signal-dot" /> SYSTEM NOMINAL <span className="status-time">14:32:08 UTC</span></div></nav>
    <header className="workspace-head"><div><p className="eyebrow">DEVSECOPS / CONTROL SURFACE / 21</p><h1>Taskboard <em>/</em> <span>Live workstream</span></h1></div><div className="workspace-aside"><span className="prompt">$</span><span>status --all</span><strong>Operational</strong><small>last sync 00:04 ago</small></div></header>
    <section className="metric-strip" aria-label="Board summary"><div><span>OPEN WORK</span><strong>{tasks.length - doneCount}</strong></div><div><span>SHIPPED TODAY</span><strong className="accent-number">{doneCount}</strong></div><div><span>THROUGHPUT</span><strong>87<span className="unit">%</span></strong></div><div className="metric-note"><span className="pulse-line" /> All services responding within threshold</div></section>
    <section className="command-bar"><form onSubmit={addTask} className="new-task"><label htmlFor="title"><span className="prompt">$</span> add-task</label><input id="title" value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Describe the next useful thing…" /><button type="submit">Queue task <span>↗</span></button></form><div className="filters" aria-label="Filter tasks">{['ALL', ...STATUSES].map((option) => <button className={filter === option ? 'filter active' : 'filter'} type="button" key={option} onClick={() => setFilter(option)}>{option === 'ALL' ? 'All work' : STATUS_LABELS[option]}</button>)}</div></section>
    <section className="board-shell" aria-label="Task board"><div className="board-heading"><span>WORKSTREAMS</span><span>{String(visibleTasks.length).padStart(2, '0')} RECORDS / LIVE VIEW</span></div><div className="board">{STATUSES.map((status) => <div className={`column column-${status.toLowerCase()}`} key={status}><div className="column-heading"><h2><span className="column-index">0{STATUSES.indexOf(status) + 1}</span>{STATUS_LABELS[status]}</h2><span className="count">{visibleTasks.filter((task) => task.status === status).length}</span></div><div className="task-list">{visibleTasks.filter((task) => task.status === status).map((task) => <article className="task-card" data-task-id={task.id} key={task.id}><div className="task-meta"><span className={`priority priority-${task.priority.toLowerCase()}`}>{task.priority}</span><span>{task.age}</span></div><h3>{task.title}</h3><div className="task-footer"><span className="avatar">{task.owner}</span><select aria-label={`Status for ${task.title}`} value={task.status} onChange={(event) => updateStatus(task.id, event.target.value)}>{STATUSES.map((option) => <option key={option} value={option}>{STATUS_LABELS[option]}</option>)}</select><button className="delete" type="button" aria-label={`Delete ${task.title}`} onClick={() => removeTask(task.id)}>×</button></div></article>)}{visibleTasks.filter((task) => task.status === status).length === 0 && <p className="empty">No work in this stream.</p>}</div></div>)}</div></section>
    <footer><span>BUILD 21.10.26</span><span>LOCAL / MOCK DATA</span><span>ESC TO EXIT</span></footer>
  </main>;
}
