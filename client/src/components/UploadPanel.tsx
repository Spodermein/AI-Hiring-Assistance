import { useState } from "react";
import { analyze } from "../lib/api";

export default function UploadPanel({ onResult }: { onResult: (r:any)=>void }) {
  const [jobText, setJobText] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [loading, setLoading] = useState(false);

  const canRun = jobText.trim().length > 0 && resumeText.trim().length > 0;

  async function run() {
    if (!canRun) return;
    setLoading(true);
    try {
      const data = await analyze(jobText.trim(), resumeText.trim());
      onResult(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <Field label="Job Description" value={jobText} onChange={setJobText} rows={8} placeholder="Paste the JD here…" />
      <Field label="Resume Text" value={resumeText} onChange={setResumeText} rows={10} placeholder="Paste your resume text here…" />
      <button
        onClick={run}
        disabled={!canRun || loading}
        style={{
          padding: "10px 14px",
          borderRadius: 10,
          border: "1px solid #111827",
          background: (!canRun || loading) ? "#9CA3AF" : "#111827",
          color: "white", fontWeight: 700, cursor: (!canRun || loading) ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Analyzing…" : "Analyze"}
      </button>
    </div>
  );
}

function Field({
  label, value, onChange, rows, placeholder,
}: { label: string; value: string; onChange: (v:string)=>void; rows?: number; placeholder?: string }) {
  return (
    <div style={{ display: "grid", gap: 6 }}>
      <label style={{ fontWeight: 800, color: "#111827" }}>{label}</label>
      <textarea
        rows={rows || 8}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{
          width: "100%",
          padding: 12,
          borderRadius: 12,
          border: "1px solid #e5e7eb",
          background: "#fff",   // force light background
          color: "#111",        // dark text
          fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
          fontSize: 13,
          resize: "vertical",
          boxShadow: "0 1px 2px rgba(0,0,0,0.03)",
          outline: "none"
        }}
      />
    </div>
  );
}
