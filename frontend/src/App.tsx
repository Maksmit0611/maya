import { useEffect, useState } from "react";
import { LogOut } from "lucide-react";
import { Login } from "./components/Login";
import { Projects } from "./components/Projects";
import { Workspace } from "./components/Workspace";
import { supabase } from "./lib/auth";
import type { Project } from "./types";
import "./styles.css";

export default function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [token, setToken] = useState<string | undefined>();
  const [project, setProject] = useState<Project | null>(null);

  useEffect(() => {
    if (!supabase) return;
    void supabase.auth.getSession().then(({ data }) => {
      if (data.session) { setToken(data.session.access_token); setAuthenticated(true); }
    });
    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session) { setToken(session.access_token); setAuthenticated(true); }
      else { setToken(undefined); setAuthenticated(false); }
    });
    return () => data.subscription.unsubscribe();
  }, []);

  async function signOut() {
    if (supabase) await supabase.auth.signOut();
    setProject(null); setToken(undefined); setAuthenticated(false);
  }

  if (!authenticated) return <Login onLogin={(nextToken) => { setToken(nextToken); setAuthenticated(true); }} />;
  if (project) return <><Workspace project={project} token={token} onBack={() => setProject(null)} /><button className="floating-logout" onClick={() => void signOut()} aria-label="Sign out"><LogOut size={15} /></button></>;
  return <><Projects token={token} onOpen={setProject} /><button className="floating-logout" onClick={() => void signOut()} aria-label="Sign out"><LogOut size={15} /></button></>;
}
