import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ResultsPane from "./components/ResultsPane";

export default function App() {
  const [data, setData] = useState<any>(null);

  return (
    // App.tsx
      <div style={{
        width: "100%",
        maxWidth: 960,
        display: "grid",
        gap: 20,
        background: "#fff",
        padding: 28,
        borderRadius: 16,
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)"
      }}>

      <h1 style={{ fontSize: 30, fontWeight: 900, textAlign: "center" }}>
        HireSight — AI Resume ↔ JD Match
      </h1>
      <p style={{ marginTop: -10, color: "#6b7280", fontSize: 14, textAlign: "center" }}>
        Paste a job description and your resume to get a match score, skill coverage, and ATS checks.
      </p>
      <UploadPanel onResult={setData} />
      <ResultsPane data={data} />
    </div>
  );
}
