export async function analyze(jobText: string, resumeText: string) {
  try {
    const res = await fetch(import.meta.env.VITE_API_URL + "/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jobText, resumeText }),
    });
    const text = await res.text();
    if (!res.ok) {
      return { error: `HTTP ${res.status}: ${text}` };
    }
    try {
      return JSON.parse(text);
    } catch {
      return { error: "Invalid JSON from server", raw: text };
    }
  } catch (e: any) {
    return { error: e?.message || "Network error" };
  }
}