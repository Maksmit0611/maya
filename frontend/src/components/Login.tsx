import { useState, type FormEvent } from "react";
import { ArrowRight, Sparkles } from "lucide-react";
import { supabase } from "../lib/auth";

type Props = { onLogin: (token?: string) => void };

export function Login({ onLogin }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function signIn(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!supabase) return;
    setBusy(true);
    setError("");
    const { data, error: authError } = await supabase.auth.signInWithPassword({ email, password });
    setBusy(false);
    if (authError || !data.session) setError(authError?.message ?? "Sign in failed");
    else onLogin(data.session.access_token);
  }

  return (
    <main className="login-screen">
      <section className="login-card">
        <div className="brand-mark"><Sparkles size={19} /><span>MAYA</span></div>
        <p className="eyebrow">YOUR DESIGN STUDIO</p>
        <h1>Make room for<br /><em>what matters.</em></h1>
        <p className="muted">Turn a room, a few ideas, and a clear brief into a design direction you can explore.</p>
        {!supabase ? (
          <button className="button primary full" onClick={() => onLogin()}>
            Continue in local demo <ArrowRight size={16} />
          </button>
        ) : (
          <form onSubmit={signIn} className="stack">
            <label>Email<input autoComplete="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label>
            <label>Password<input autoComplete="current-password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} required /></label>
            {error && <p className="error-message" role="alert">{error}</p>}
            <button className="button primary full" disabled={busy}>{busy ? "Signing in…" : "Sign in"}<ArrowRight size={16} /></button>
          </form>
        )}
        <p className="login-foot">Your project media stays private. MAYA concepts are visualisations, not construction documents.</p>
      </section>
      <div className="login-art" aria-hidden="true"><div className="art-window" /><div className="art-sofa" /><div className="art-plant">✦</div><div className="art-caption">A softer place to land.</div></div>
    </main>
  );
}
