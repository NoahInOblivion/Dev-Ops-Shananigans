import { useEffect, useState } from 'react';

const STATUSES = ['TODO', 'IN_PROGRESS', 'DONE'];

async function request(path, options) {
  const response = await fetch(path, {headers: {'Content-Type': 'application/json'}, ...options});
  if (!response.ok) throw new Error((await response.json()).detail || 'Request failed');
  return response.status === 204 ? null : response.json();
}

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const loadTasks = async () => {
    try { setTasks(await request('/api/tasks')); setError(''); }
    catch (reason) { setError(reason.message); }
    finally { setLoading(false); }
  };

  useEffect(() => { loadTasks(); }, []);

  const addTask = async (event) => {
    event.preventDefault();
    if (!title.trim()) return setError('A title is required.');
    try { await request('/api/tasks', {method: 'POST', body: JSON.stringify({title})}); setTitle(''); await loadTasks(); }
    catch (reason) { setError(reason.message); }
  };

  const changeStatus = async (id, status) => {
    try { await request(`/api/tasks/${id}`, {method: 'PUT', body: JSON.stringify({status})}); await loadTasks(); }
    catch (reason) { setError(reason.message); }
  };

  const removeTask = async (id) => {
    try { await request(`/api/tasks/${id}`, {method: 'DELETE'}); await loadTasks(); }
    catch (reason) { setError(reason.message); }
  };

  return <main>
    <header><p className="eyebrow">DEVSECOPS CAPSTONE</p><h1>TaskBoard</h1><p>Ship small work, visibly.</p></header>
    <form onSubmit={addTask} className="new-task"><label htmlFor="title">New task</label><div><input id="title" value={title} onChange={(event) => setTitle(event.target.value)} placeholder="What needs doing?" /><button type="submit">Add task</button></div></form>
    {error && <p role="alert" className="error">{error}</p>}
    {loading ? <p>Loading tasks…</p> : <section className="board" aria-label="Task board">{STATUSES.map((status) => <div className="column" key={status}><h2>{status.replace('_', ' ')}</h2>{tasks.filter((task) => task.status === status).map((task) => <article className="task" key={task.id}><strong>{task.title}</strong>{task.description && <p>{task.description}</p>}<select aria-label={`Status for ${task.title}`} value={task.status} onChange={(event) => changeStatus(task.id, event.target.value)}>{STATUSES.map((option) => <option key={option}>{option}</option>)}</select><button className="delete" onClick={() => removeTask(task.id)} type="button">Delete</button></article>)}</div>)}</section>}
  </main>;
}
