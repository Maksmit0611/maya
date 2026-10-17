import { useCallback, useEffect, useMemo, useState, type ChangeEvent, type FormEvent } from "react";
import { ArrowLeft, Check, Circle, FileImage, LoaderCircle, Plus, RefreshCw, Sparkles, UploadCloud } from "lucide-react";
import { API_BASE, api } from "../lib/api";
import type { DesignPlan, Job, Project, Result, Room } from "../types";

type Props = { project: Project; token?: string; onBack: () => void };
type BriefData = { room_type: string; style: string; budget: string; constraints: string; occupants: string };
type UploadLink = { asset_id: string; upload_url: string; method: "PUT"; headers: Record<string, string> };

const emptyBrief: BriefData = { room_type: "Living room", style: "Warm contemporary", budget: "", constraints: "", occupants: "" };

export function Workspace({ project, token, onBack }: Props) {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [results, setResults] = useState<Result[]>([]);
  const [brief, setBrief] = useState<BriefData>(emptyBrief);
  const [roomName, setRoomName] = useState("");
  const [roomId, setRoomId] = useState("");
  const [plan, setPlan] = useState<DesignPlan | null>(null);
  const [briefStep, setBriefStep] = useState<1 | 2>(1);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const hasActiveJobs = useMemo(() => jobs.some((job) => job.status === "queued" || job.status === "running"), [jobs]);

  const refresh = useCallback(async () => {
    try {
      const [nextRooms, nextJobs, nextResults] = await Promise.all([
        api<Room[]>(`/projects/${project.id}/rooms`, token),
        api<Job[]>(`/jobs?project_id=${project.id}`, token),
        api<Result[]>(`/projects/${project.id}/results`, token),
      ]);
      setRooms(nextRooms); setJobs(nextJobs); setResults(nextResults);
      setRoomId((current) => current || nextRooms[0]?.id || "");
      setError("");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not load the studio"); }
  }, [project.id, token]);

  useEffect(() => { void refresh(); }, [refresh]);
  useEffect(() => {
    if (!hasActiveJobs) return;
    const timer = window.setInterval(() => { void refresh(); }, 1800);
    return () => window.clearInterval(timer);
  }, [hasActiveJobs, refresh]);

  async function addRoom(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!roomName.trim()) return;
    setBusy(true); setError("");
    try {
      const room = await api<Room>(`/projects/${project.id}/rooms`, token, { method: "POST", body: JSON.stringify({ name: roomName.trim(), room_type: brief.room_type.toLowerCase() }) });
      setRooms((current) => [room, ...current]); setRoomId(room.id); setRoomName(""); setNotice("Room added to your project.");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not add room"); }
    finally { setBusy(false); }
  }

  async function uploadFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    setBusy(true); setNotice(""); setError("");
    try {
      const signed = await api<UploadLink>(`/projects/${project.id}/assets/upload-url`, token, {
        method: "POST", body: JSON.stringify({ room_id: roomId || null, filename: file.name, mime_type: file.type, size_bytes: file.size }),
      });
      const url = signed.upload_url.startsWith("http") ? signed.upload_url : `${API_BASE}${signed.upload_url}`;
      const response = await fetch(url, { method: signed.method, headers: signed.headers, body: file });
      if (!response.ok) throw new Error("Photo upload failed");
      setNotice(`${file.name} is safely uploaded to this project.`);
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Photo upload failed"); }
    finally { setBusy(false); }
  }

  async function createPlan(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setNotice(""); setError("");
    const fullBrief = { ...brief, room_id: roomId || null };
    try {
      await api(`/projects/${project.id}/briefs`, token, { method: "POST", body: JSON.stringify({ room_id: roomId || null, content: fullBrief }) });
      const response = await api<{ plan: DesignPlan }>("/chat", token, {
        method: "POST", body: JSON.stringify({ project_id: project.id, brief: fullBrief, message: `Create a visual direction for this ${brief.room_type.toLowerCase()}.` }),
      });
      setPlan(response.plan); setNotice("Your design direction is ready. Review assumptions before creating a visual preview.");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not create the brief"); }
    finally { setBusy(false); }
  }

  async function enqueuePreview() {
    setBusy(true); setError(""); setNotice("");
    const input = { ...brief, room_id: roomId || null, plan: plan ?? undefined };
    try {
      const job = await api<Job>("/jobs", token, { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() }, body: JSON.stringify({ project_id: project.id, room_id: roomId || null, brief: input }) });
      setJobs((current) => [job, ...current.filter((item) => item.id !== job.id)]);
      setNotice("Preview queued. You can keep working while the worker prepares it.");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not queue preview"); }
    finally { setBusy(false); }
  }

  async function selectResult(result: Result) {
    try {
      const updated = await api<Result>(`/results/${result.id}/select`, token, { method: "POST", body: JSON.stringify({ selected: true }) });
      setResults((current) => current.map((item) => item.id === updated.id ? updated : item));
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Could not select result"); }
  }

  return (
    <main className="app-shell">
      <header className="topbar"><button className="back-link" onClick={onBack}><ArrowLeft size={16} /> Projects</button><a className="brand-mark" href="#home"><Sparkles size={18} /><span>MAYA</span></a><span className="topbar-note">LOCAL MOCK PROVIDERS <i /> PRIVATE WORKSPACE</span><span className="user-chip">DEV MODE</span></header>
      <section className="workspace-wrap">
        <div className="workspace-title"><div><p className="eyebrow">PROJECT WORKSPACE</p><h1>{project.name}</h1><p className="muted">A considered space starts with a clear brief.</p></div><button className="button subtle" onClick={() => void refresh()} aria-label="Refresh workspace"><RefreshCw size={15} /> Refresh</button></div>
        {error && <p className="error-message" role="alert">{error}</p>}{notice && <p className="notice-message" role="status">{notice}</p>}
        <div className="studio-grid">
          <section className="studio-main">
            <div className="panel section-panel">
              <div className="panel-heading"><div><p className="eyebrow">01 / THE ROOM</p><h2>Bring a little context</h2></div><span className="step-number">01</span></div>
              <div className="room-row"><form className="room-form" onSubmit={addRoom}><label htmlFor="room-name">Room name</label><div className="inline-input"><input id="room-name" value={roomName} onChange={(event) => setRoomName(event.target.value)} placeholder="e.g. Sunlit living room" /><button className="icon-button" disabled={!roomName.trim() || busy} aria-label="Add room"><Plus size={18} /></button></div></form><label className="room-select-label">Active room<select value={roomId} onChange={(event) => setRoomId(event.target.value)}><option value="">No room selected</option>{rooms.map((room) => <option key={room.id} value={room.id}>{room.name}</option>)}</select></label></div>
              <label className="upload-zone"><input type="file" accept="image/jpeg,image/png,image/webp" onChange={uploadFile} disabled={busy} /><UploadCloud size={20} /><span><strong>{busy ? "Working…" : "Add a room photo"}</strong><small>JPG, PNG or WebP · up to 20 MB · private upload</small></span><span className="upload-action">Choose file</span></label>
            </div>
            <form className="panel section-panel brief-panel" onSubmit={createPlan}>
              <div className="panel-heading"><div><p className="eyebrow">02 / THE BRIEF · STEP {briefStep} OF 2</p><h2>{briefStep === 1 ? "What should it feel like?" : "How does this room work?"}</h2></div><span className="step-number">0{briefStep}</span></div>
              {briefStep === 1 ? <div className="form-grid"><label>Room type<select value={brief.room_type} onChange={(event) => setBrief({ ...brief, room_type: event.target.value })}><option>Living room</option><option>Bedroom</option><option>Kitchen</option><option>Dining room</option><option>Home office</option><option>Bathroom</option></select></label><label>Style direction<input value={brief.style} onChange={(event) => setBrief({ ...brief, style: event.target.value })} placeholder="Warm contemporary" /></label></div> : <div className="form-grid"><label>Budget range <span className="optional">optional</span><input value={brief.budget} onChange={(event) => setBrief({ ...brief, budget: event.target.value })} placeholder="e.g. $5k–$10k" /></label><label>Who uses this room? <span className="optional">optional</span><input value={brief.occupants} onChange={(event) => setBrief({ ...brief, occupants: event.target.value })} placeholder="Everyday routines, pets…" /></label><label className="wide">Non-negotiables or notes <span className="optional">optional</span><textarea rows={3} value={brief.constraints} onChange={(event) => setBrief({ ...brief, constraints: event.target.value })} placeholder="Keep the existing oak floor. Make space for reading." /></label></div>}
              <div className="form-footer"><span><Circle size={8} fill="currentColor" /> This creates an aesthetic concept only.</span>{briefStep === 1 ? <button className="button dark" type="button" onClick={() => setBriefStep(2)}>Next: room details <span aria-hidden="true">↗</span></button> : <div className="wizard-actions"><button className="button subtle" type="button" onClick={() => setBriefStep(1)}>Back</button><button className="button dark" disabled={busy}>{busy ? "Thinking…" : "Create design plan"}<Sparkles size={15} /></button></div>}</div>
            </form>
            {plan && <section className="panel section-panel plan-card"><div className="panel-heading"><div><p className="eyebrow">03 / MAYA'S DIRECTION</p><h2>{plan.style}</h2></div><span className="provider-pill">MOCK PLAN</span></div><p className="plan-narration">{plan.narration}</p><div className="palette-row">{plan.palette.map((color) => <div className="palette-item" key={color.hex}><span style={{ backgroundColor: color.hex }} /><div><strong>{color.name}</strong><small>{color.role}</small></div></div>)}</div><div className="scene-list"><p className="eyebrow">SCENE BEATS</p>{plan.scene_beats.map((beat, index) => <p key={beat}><span>0{index + 1}</span>{beat}</p>)}</div><ul className="constraints">{plan.constraints.map((constraint) => <li key={constraint}>{constraint}</li>)}</ul><button className="button primary" onClick={enqueuePreview} disabled={busy}>Queue visual preview <ArrowRightIcon /></button></section>}
          </section>
          <aside className="studio-aside">
            <section className="aside-card panel"><div className="aside-heading"><div><p className="eyebrow">JOB HISTORY</p><h2>In progress & recent</h2></div><span className="count-bubble">{jobs.length}</span></div>{jobs.length === 0 ? <p className="aside-empty">Your generation jobs will appear here. The worker runs separately from the web app.</p> : <div className="job-list">{jobs.map((job) => <div className="job-row" key={job.id}><span className={`status-dot ${job.status}`} /> <div className="grow"><strong>{job.status === "succeeded" ? "Preview ready" : job.status === "failed" ? "Preview needs attention" : "Design preview"}</strong><small>{job.status}{job.cancellation_requested ? " · cancellation requested" : ""}</small></div>{job.status === "running" && <LoaderCircle className="spin" size={15} />}</div>)}</div>}</section>
            <section className="aside-card panel"><div className="aside-heading"><div><p className="eyebrow">RESULTS</p><h2>Design options</h2></div><span className="count-bubble">{results.length}</span></div>{results.length === 0 ? <div className="result-empty"><FileImage size={22} /><p>Mock and real-provider outputs will live here as reviewable options.</p></div> : <div className="result-list">{results.map((result, index) => { const media = result.output_json.media; return <article className={`result-card ${result.selected_by ? "selected" : ""}`} key={result.id}><div className="result-thumb"><span>OPTION {String(results.length - index).padStart(2, "0")}</span><span className="thumb-star">✳</span><small>{String(media.kind ?? "concept").replaceAll("_", " ")}</small></div><div className="result-meta"><div><strong>{result.output_json.plan.style}</strong><small>Generated with mock providers</small></div><button className="select-button" onClick={() => void selectResult(result)} aria-label="Select design option">{result.selected_by ? <Check size={16} /> : "Select"}</button></div></article>; })}</div>}</section>
            <p className="aside-disclaimer">MAYA concepts are AI visualisations. Confirm measurements, safety, code, and product details with qualified professionals.</p>
          </aside>
        </div>
      </section>
    </main>
  );
}

function ArrowRightIcon() { return <span aria-hidden="true">↗</span>; }
