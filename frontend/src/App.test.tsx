import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";

describe("MAYA keyless onboarding", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("[]", { status: 200, headers: { "Content-Type": "application/json" } })));
  });

  it("enters the local demo without credentials and loads the project empty state", async () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: /continue in local demo/i }));
    expect(await screen.findByRole("heading", { name: "Your projects" })).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Start with one room.")).toBeInTheDocument());
  });
});
