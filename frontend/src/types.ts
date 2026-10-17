export type Project = { id: string; owner_id: string; name: string; created_at: string };
export type Room = { id: string; project_id: string; name: string; room_type: string; dimensions: Record<string, unknown> };
export type DesignPlan = {
  style: string;
  palette: { name: string; hex: string; role: string }[];
  camera_moves: string[];
  scene_beats: string[];
  narration: string;
  constraints: string[];
};
export type Job = {
  id: string;
  project_id: string;
  status: "queued" | "running" | "succeeded" | "failed" | "cancelled";
  cancellation_requested: boolean;
  provenance: Record<string, unknown>;
  error_json: { code: string; message: string } | null;
  created_at: string;
};
export type Result = {
  id: string;
  job_id: string;
  output_json: { plan: DesignPlan; media: Record<string, unknown> };
  selected_by: string | null;
  created_at: string;
};
