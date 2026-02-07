import { useEffect, useMemo, useState } from "react";
import { apiFetch } from "../api/client";
import type { ClassroomPublic, PhrasePublic, UserPublic } from "../api/types";
import { PhraseCard } from "./PhraseCard";

type Health = { ok: boolean };

export function App() {
  const lastClassroomIdKey = "ltc:lastClassroomId";

  const [health, setHealth] = useState<Health | null>(null);
  const [me, setMe] = useState<UserPublic | null>(null);
  const [myClassrooms, setMyClassrooms] = useState<ClassroomPublic[]>([]);
  const [phrases, setPhrases] = useState<PhrasePublic[]>([]);
  const [classroom, setClassroom] = useState<ClassroomPublic | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [email, setEmail] = useState("teacher@example.com");
  const [password, setPassword] = useState("password123");
  const [role, setRole] = useState<"teacher" | "student">("teacher");

  const [classroomName, setClassroomName] = useState("Chinese 101");
  const [inviteCode, setInviteCode] = useState("");

  const [newChinese, setNewChinese] = useState("你好");
  const [newPinyin, setNewPinyin] = useState("nǐ hǎo");
  const [newEnglish, setNewEnglish] = useState("Hello");

  function rememberClassroomId(id: number) {
    try {
      localStorage.setItem(lastClassroomIdKey, String(id));
    } catch {
      // ignore
    }
  }

  function readRememberedClassroomId(): number | null {
    try {
      const v = localStorage.getItem(lastClassroomIdKey);
      if (!v) return null;
      const n = Number(v);
      return Number.isFinite(n) ? n : null;
    } catch {
      return null;
    }
  }

  async function loadSessionAndClassrooms() {
    const meData = await apiFetch<UserPublic>("/api/me");
    setMe(meData);

    const cls = await apiFetch<ClassroomPublic[]>("/api/classrooms");
    setMyClassrooms(cls);

    // Restore last selected classroom if possible.
    const rememberedId = readRememberedClassroomId();
    const toSelect =
      (rememberedId ? cls.find((c) => c.id === rememberedId) : undefined) ?? (cls.length === 1 ? cls[0] : undefined);
    if (toSelect) {
      setClassroom(toSelect);
      await refreshPhrases(toSelect.id);
    }
  }

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await apiFetch<Health>("/api/health");
        if (!cancelled) setHealth(data);
        try {
          await loadSessionAndClassrooms();
        } catch {
          if (!cancelled) setMe(null);
          if (!cancelled) setMyClassrooms([]);
        }
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

  async function refreshPhrases(nextClassroomId: number) {
    const items = await apiFetch<PhrasePublic[]>(`/api/classrooms/${nextClassroomId}/phrases`);
    setPhrases(items);
  }

  async function onSignup() {
    setError(null);
    await apiFetch<UserPublic>("/api/auth/signup", {
      method: "POST",
      body: JSON.stringify({ email, password, role }),
    });
    await loadSessionAndClassrooms();
  }

  async function onLogin() {
    setError(null);
    await apiFetch<UserPublic>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    await loadSessionAndClassrooms();
  }

  async function onLogout() {
    setError(null);
    await apiFetch<{ ok: boolean }>("/api/auth/logout", { method: "POST", body: JSON.stringify({}) });
    setMe(null);
    setClassroom(null);
    setMyClassrooms([]);
    setPhrases([]);
  }

  async function onCreateClassroom() {
    setError(null);
    const c = await apiFetch<ClassroomPublic>("/api/classrooms", {
      method: "POST",
      body: JSON.stringify({ name: classroomName }),
    });
    setClassroom(c);
    rememberClassroomId(c.id);
    const cls = await apiFetch<ClassroomPublic[]>("/api/classrooms");
    setMyClassrooms(cls);
    await refreshPhrases(c.id);
  }

  async function onJoinClassroom() {
    setError(null);
    const res = await apiFetch<{ ok: boolean; classroom_id: number }>("/api/classrooms/join", {
      method: "POST",
      body: JSON.stringify({ invite_code: inviteCode }),
    });
    rememberClassroomId(res.classroom_id);
    const cls = await apiFetch<ClassroomPublic[]>("/api/classrooms");
    setMyClassrooms(cls);
    const joined = cls.find((c) => c.id === res.classroom_id);
    if (joined) setClassroom(joined);
    await refreshPhrases(res.classroom_id);
  }

  async function onCreatePhrase() {
    if (!classroom) return;
    setError(null);
    await apiFetch<PhrasePublic>(`/api/classrooms/${classroom.id}/phrases`, {
      method: "POST",
      body: JSON.stringify({ chinese: newChinese, pinyin: newPinyin, english: newEnglish, notes: null }),
    });
    await refreshPhrases(classroom.id);
  }

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: 24, maxWidth: 800 }}>
      <h1>Chinese Practice Studio</h1>
      <p style={{ color: "#444" }}>
        This is a learning repo. Start at <code>lessons/00-orientation.md</code>.
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

      {!me ? (
        <div>
          <h2>Log in / sign up</h2>
          <div style={{ display: "grid", gap: 8, maxWidth: 420 }}>
            <label>
              Email
              <input value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: "100%" }} />
            </label>
            <label>
              Password
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                style={{ width: "100%" }}
              />
            </label>
            <label>
              Role (for signup)
              <select value={role} onChange={(e) => setRole(e.target.value as any)} style={{ width: "100%" }}>
                <option value="teacher">teacher</option>
                <option value="student">student</option>
              </select>
            </label>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={onLogin}>Login</button>
              <button onClick={onSignup}>Sign up</button>
            </div>
            <p style={{ color: "#555", marginTop: 8 }}>
              Tip: use a real email format, password 8+ chars.
            </p>
          </div>
        </div>
      ) : (
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              Logged in as <code>{me.email}</code> (<code>{me.role}</code>)
            </div>
            <button onClick={onLogout}>Logout</button>
          </div>

          <h2 style={{ marginTop: 16 }}>Classroom</h2>
          {!classroom ? (
            <div style={{ display: "grid", gap: 10, maxWidth: 520 }}>
              {myClassrooms.length > 0 ? (
                <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
                  <h3>Pick an existing classroom</h3>
                  <div style={{ display: "grid", gap: 8 }}>
                    {myClassrooms.map((c) => (
                      <button
                        key={c.id}
                        onClick={async () => {
                          setClassroom(c);
                          rememberClassroomId(c.id);
                          await refreshPhrases(c.id);
                        }}
                        style={{ textAlign: "left" }}
                      >
                        {c.name} (id {c.id})
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
              {me.role === "teacher" ? (
                <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
                  <h3>Create classroom</h3>
                  <label>
                    Name
                    <input
                      value={classroomName}
                      onChange={(e) => setClassroomName(e.target.value)}
                      style={{ width: "100%" }}
                    />
                  </label>
                  <div style={{ marginTop: 8 }}>
                    <button onClick={onCreateClassroom}>Create</button>
                  </div>
                </div>
              ) : null}

              <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
                <h3>Join classroom</h3>
                <label>
                  Invite code
                  <input value={inviteCode} onChange={(e) => setInviteCode(e.target.value)} style={{ width: "100%" }} />
                </label>
                <div style={{ marginTop: 8 }}>
                  <button onClick={onJoinClassroom}>Join</button>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
              <div>
                Current classroom: <code>{classroom.id}</code>
              </div>
              {classroom.invite_code ? (
                <div>
                  Invite code: <code>{classroom.invite_code}</code>
                </div>
              ) : null}
              <div style={{ marginTop: 8 }}>
                <button
                  onClick={async () => {
                    setClassroom(null);
                    setPhrases([]);
                  }}
                >
                  Switch classroom
                </button>
              </div>
            </div>
          )}

          {classroom ? (
            <div style={{ marginTop: 16 }}>
              <h2>Phrases</h2>
              {me.role === "teacher" ? (
                <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginBottom: 12 }}>
                  <h3>Create phrase</h3>
                  <div style={{ display: "grid", gap: 8 }}>
                    <label>
                      Chinese
                      <input value={newChinese} onChange={(e) => setNewChinese(e.target.value)} style={{ width: "100%" }} />
                    </label>
                    <label>
                      Pinyin
                      <input value={newPinyin} onChange={(e) => setNewPinyin(e.target.value)} style={{ width: "100%" }} />
                    </label>
                    <label>
                      English
                      <input value={newEnglish} onChange={(e) => setNewEnglish(e.target.value)} style={{ width: "100%" }} />
                    </label>
                    <div>
                      <button onClick={onCreatePhrase}>Create</button>
                    </div>
                  </div>
                </div>
              ) : null}

              <div style={{ display: "grid", gap: 8 }}>
                {phrases.map((p) => (
                  <PhraseCard key={p.id} phrase={p} me={me} classroomId={classroom.id} />
                ))}
                {phrases.length === 0 ? <div style={{ color: "#666" }}>No phrases yet.</div> : null}
              </div>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}

