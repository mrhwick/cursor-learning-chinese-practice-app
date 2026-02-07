export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    credentials: "include",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return (await res.json()) as T;
}

export async function apiUpload(path: string, file: File): Promise<void> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(path, { method: "POST", body: form, credentials: "include" });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
}

export async function apiUploadBlob(path: string, blob: Blob, filename: string): Promise<void> {
  const form = new FormData();
  form.append("file", new File([blob], filename, { type: blob.type || "application/octet-stream" }));
  const res = await fetch(path, { method: "POST", body: form, credentials: "include" });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
}

