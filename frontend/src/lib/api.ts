export const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type APIError = { code: string; message: string; details: unknown; request_id: string };

export async function api<T>(path: string, token?: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (init.body && !(init.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${API_BASE}/api/v1${path}`, { ...init, headers });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as APIError | null;
    throw new Error(body?.message ?? `Request failed (${response.status})`);
  }
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}
