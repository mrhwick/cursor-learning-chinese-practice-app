import { useEffect, useMemo, useState } from "react";
import { apiFetch } from "../api/client";

type Health = { ok: boolean };

export function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await apiFetch<Health>("/api/health");
        if (!cancelled) setHealth(data);
      } catch (e) {
        if (!cancelled) setError(String(e));
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const statusText = useMemo(() => {
    if (error) return `API error: ${error}`;
    if (!health) return "Loading...";
    return health.ok ? "API OK" : "API not ok";
  }, [health, error]);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: 24, maxWidth: 800 }}>
      <h1>Chinese Practice Studio</h1>
      <p style={{ color: "#444" }}>
        This is a learning repo. Start at <code>lessons/00-orientation.md</code>, then build features step-by-step.
      </p>
      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: 8,
          padding: 12,
          background: "#fafafa",
        }}
      >
        <strong>Backend status:</strong> {statusText}
      </div>

      {error ? (
        <div style={{ marginTop: 12, color: "#b00020" }}>
          <strong>Error:</strong> {error}
        </div>
      ) : null}

      <hr style={{ margin: "16px 0" }} />
      <h2>Next step</h2>
      <p>
        Open <code>lessons/00-orientation.md</code> and follow it. The lessons will guide you to build features into this
        app.
      </p>
    </div>
  );
}

