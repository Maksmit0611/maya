import { useCallback, useEffect, useState, type FormEvent } from "react";
import { ArrowUpRight, Plus, Sparkles } from "lucide-react";
import { api } from "../lib/api";
import type { Project } from "../types";

type Props = { token?: string; onOpen: (project: Project) => void };

export function Projects({ token, onOpen }: Props) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    try { setProjects(await api<Project[]>("/projects", token)); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Could not load projects"); }
  }, [token]);
  useEffect(() => { void refresh(); }, [refresh]);

  async function createProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!name.trim()) return;
    setBusy(true); setError("");
    try {
      const project = await api<Project>("/projects", token, { method: "POST", body: JSON.stringify({ name: name.trim() }) });
      setName("");
      onOpen(project);
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not create project"); }
    finally { setBusy(false); }
  }

  return (
    <main className="app-shell">
      <header className="topbar"><a className="brand-mark" href="#home"><Sparkles size={18} /><span>MAYA</span></a><span className="topbar-note">DESIGN STUDIO <i /> PHASE 01</span><span className="user-chip">Local workspace</span></header>
      <section className="page-wrap">
        <div className="page-heading"><div><p className="eyebrow">A GOOD PLACE TO BEGIN</p><h1>Your projects</h1><p className="muted">Collect the rooms, ideas, and decisions that make a place yours.</p></div><span className="heading-count">{projects.length.toString().padStart(2, "0")} <small>PROJECTS</small></span></div>
        <form className="create-project panel" onSubmit={createProject}><div className="icon-tile"><Plus size={18} /></div><div className="grow"><label htmlFor="project-name">Start with a project name</label><input id="project-name" placeholder="e.g. The Hawthorne House" value={name} onChange={(event) => setName(event.target.value)} /></div><button className="button dark" disabled={!name.trim() || busy}>{busy ? "Creating…" : "Create project"}<ArrowUpRight size={16} /></button></form>
        {error && <p className="error-message" role="alert">{error}</p>}
        <div className="section-label"><span>RECENT WORK</span><span>{projects.length} {projects.length === 1 ? "PROJECT" : "PROJECTS"}</span></div>
        {projects.length === 0 ? <div className="empty-state panel"><div className="empty-illustration">✳</div><h2>Start with one room.</h2><p>Give your first project a name. You can add rooms, photos, and the details that help MAYA shape a plan.</p></div> : <div className="project-grid">{projects.map((project, index) => <button key={project.id} className={`project-card panel tone-${index % 3}`} onClick={() => onOpen(project)}><span className="project-index">PROJECT {String(index + 1).padStart(2, "0")}</span><span className="project-orb">{index % 2 === 0 ? "✳" : "◌"}</span><span className="project-name">{project.name}</span><span className="project-open">OPEN STUDIO <ArrowUpRight size={14} /></span></button>)}</div>}
      </section>
    </main>
  );
}
