import { useRef, useState } from "react";
import type { FeedbackPublic, PhrasePublic, UserPublic } from "../api/types";
import { apiFetch, apiUpload, apiUploadBlob } from "../api/client";

type SubmissionPublic = { id: number; phrase_id: number; user_id: number; created_at: string };

export function PhraseCard(props: {
  phrase: PhrasePublic;
  me: UserPublic;
  classroomId: number;
}) {
  const { phrase, me } = props;

  const [submissions, setSubmissions] = useState<SubmissionPublic[] | null>(null);
  const [feedback, setFeedback] = useState<Record<number, FeedbackPublic[]>>({});
  const [error, setError] = useState<string | null>(null);
  const [isRecording, setIsRecording] = useState(false);

  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  async function refreshSubmissions() {
    const items = await apiFetch<SubmissionPublic[]>(`/api/phrases/${phrase.id}/submissions`);
    setSubmissions(items);
  }

  async function loadFeedback(submissionId: number) {
    const items = await apiFetch<FeedbackPublic[]>(`/api/submissions/${submissionId}/feedback`);
    setFeedback((prev) => ({ ...prev, [submissionId]: items }));
  }

  async function leaveFeedback(submissionId: number, payload: { comment: string; score_tones: number; score_clarity: number }) {
    await apiFetch<FeedbackPublic>(`/api/submissions/${submissionId}/feedback`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    await loadFeedback(submissionId);
  }

  async function deleteFeedback(feedbackId: number, submissionId: number) {
    await apiFetch<{ ok: boolean }>(`/api/feedback/${feedbackId}`, { method: "DELETE" });
    await loadFeedback(submissionId);
  }

  async function uploadAttemptFile(file: File) {
    await apiUpload(`/api/phrases/${phrase.id}/submissions`, file);
    await refreshSubmissions();
  }

  async function startRecording() {
    setError(null);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef.current = stream;
    chunksRef.current = [];

    const recorder = new MediaRecorder(stream);
    recorderRef.current = recorder;

    recorder.ondataavailable = (evt) => {
      if (evt.data && evt.data.size > 0) chunksRef.current.push(evt.data);
    };
    recorder.onstop = async () => {
      try {
        const blob = new Blob(chunksRef.current, { type: recorder.mimeType || "audio/webm" });
        await apiUploadBlob(`/api/phrases/${phrase.id}/submissions`, blob, "recording.webm");
        await refreshSubmissions();
      } catch (e) {
        setError(String(e));
      } finally {
        stream.getTracks().forEach((t) => t.stop());
        streamRef.current = null;
        recorderRef.current = null;
        chunksRef.current = [];
        setIsRecording(false);
      }
    };

    recorder.start();
    setIsRecording(true);
  }

  async function stopRecording() {
    recorderRef.current?.stop();
  }

  return (
    <div style={{ border: "1px solid #eee", borderRadius: 8, padding: 10 }}>
      <div style={{ fontSize: 18 }}>{phrase.chinese}</div>
      <div style={{ color: "#555" }}>{phrase.pinyin}</div>
      <div>{phrase.english}</div>

      <div style={{ marginTop: 8 }}>
        {phrase.has_model_audio ? (
          <audio controls src={`/api/phrases/${phrase.id}/model-audio`} style={{ width: "100%" }} />
        ) : (
          <div style={{ color: "#666" }}>No model audio yet.</div>
        )}
      </div>

      {me.role === "teacher" ? (
        <div style={{ marginTop: 8 }}>
          <label style={{ display: "block", fontSize: 12, color: "#555" }}>
            Upload model audio
            <input
              type="file"
              accept="audio/*"
              onChange={async (e) => {
                const file = e.target.files?.[0];
                if (!file) return;
                try {
                  setError(null);
                  await apiUpload(`/api/phrases/${phrase.id}/model-audio`, file);
                } catch (err) {
                  setError(String(err));
                } finally {
                  e.target.value = "";
                }
              }}
            />
          </label>
        </div>
      ) : null}

      <hr style={{ margin: "12px 0" }} />

      <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
        <button
          onClick={async () => {
            try {
              setError(null);
              await refreshSubmissions();
            } catch (e) {
              setError(String(e));
            }
          }}
        >
          Load submissions
        </button>

        <label style={{ display: "inline-block" }}>
          <span style={{ fontSize: 12, color: "#555" }}>Upload attempt</span>
          <input
            type="file"
            accept="audio/*"
            onChange={async (e) => {
              const file = e.target.files?.[0];
              if (!file) return;
              try {
                setError(null);
                await uploadAttemptFile(file);
              } catch (err) {
                setError(String(err));
              } finally {
                e.target.value = "";
              }
            }}
          />
        </label>

        {!isRecording ? (
          <button
            onClick={() => {
              startRecording().catch((e) => setError(String(e)));
            }}
          >
            Start recording
          </button>
        ) : (
          <button onClick={stopRecording}>Stop recording</button>
        )}
      </div>

      {error ? (
        <div style={{ marginTop: 8, color: "#b00020" }}>
          <strong>Error:</strong> {error}
        </div>
      ) : null}

      {submissions ? (
        <div style={{ marginTop: 10, display: "grid", gap: 8 }}>
          {submissions.map((s) => (
            <div key={s.id} style={{ border: "1px solid #f0f0f0", borderRadius: 8, padding: 8 }}>
              <div style={{ fontSize: 12, color: "#555" }}>
                Submission <code>{s.id}</code> by user <code>{s.user_id}</code>
              </div>
              <audio controls src={`/api/submissions/${s.id}/audio`} style={{ width: "100%" }} />
              <div style={{ marginTop: 8, display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                <button
                  onClick={() => {
                    loadFeedback(s.id).catch((e) => setError(String(e)));
                  }}
                >
                  Load feedback
                </button>
              </div>
              {feedback[s.id] ? (
                <div style={{ marginTop: 8, display: "grid", gap: 8 }}>
                  <FeedbackComposer
                    onSubmit={(payload) => leaveFeedback(s.id, payload).catch((e) => setError(String(e)))}
                  />
                  {feedback[s.id]!.map((f) => (
                    <div key={f.id} style={{ border: "1px solid #eee", borderRadius: 8, padding: 8 }}>
                      <div style={{ fontSize: 12, color: "#555" }}>
                        By user <code>{f.author_id}</code> — tones {f.score_tones}/5, clarity {f.score_clarity}/5
                      </div>
                      <div style={{ marginTop: 6 }}>{f.comment}</div>
                      <div style={{ marginTop: 8 }}>
                        <button
                          onClick={() => {
                            deleteFeedback(f.id, s.id).catch((e) => setError(String(e)));
                          }}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                  {feedback[s.id]!.length === 0 ? <div style={{ color: "#666" }}>No feedback yet.</div> : null}
                </div>
              ) : null}
            </div>
          ))}
          {submissions.length === 0 ? <div style={{ color: "#666" }}>No submissions yet.</div> : null}
        </div>
      ) : null}
    </div>
  );
}

function FeedbackComposer(props: {
  onSubmit: (payload: { comment: string; score_tones: number; score_clarity: number }) => void;
}) {
  const [comment, setComment] = useState("Nice attempt! Try to make the tones clearer on the second syllable.");
  const [tones, setTones] = useState(4);
  const [clarity, setClarity] = useState(4);

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 8 }}>
      <div style={{ fontSize: 12, color: "#555", marginBottom: 6 }}>Leave feedback</div>
      <div style={{ display: "grid", gap: 8 }}>
        <label style={{ display: "grid", gap: 4 }}>
          Comment
          <textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={3} />
        </label>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <label>
            Tones (1–5)
            <input
              type="number"
              min={1}
              max={5}
              value={tones}
              onChange={(e) => setTones(Number(e.target.value))}
              style={{ width: 70, marginLeft: 6 }}
            />
          </label>
          <label>
            Clarity (1–5)
            <input
              type="number"
              min={1}
              max={5}
              value={clarity}
              onChange={(e) => setClarity(Number(e.target.value))}
              style={{ width: 70, marginLeft: 6 }}
            />
          </label>
          <button
            onClick={() => props.onSubmit({ comment, score_tones: tones, score_clarity: clarity })}
            style={{ alignSelf: "end" }}
          >
            Submit feedback
          </button>
        </div>
      </div>
    </div>
  );
}

