import ScoreDial from "./ScoreDial";

export default function ResultsPane({ data }: { data: any }) {
  if (!data) return <Card><Muted>No data yet. Paste JD + resume and click <b>Analyze</b>.</Muted></Card>;
  if (data.error) return <ErrorBanner text={String(data.error)} />;

  const req: string[] = data.skills?.required || [];
  const have: string[] = data.skills?.present || [];
  const missing: string[] = data.skills?.missing || [];
  const coverage = req.length ? Math.round((have.length / req.length) * 100) : 100;

  return (
    <div style={wrap}>
      {/* Header: Score + Similarities */}
      <div style={grid2}>
        <Card>
          <div style={row}>
            <ScoreDial score={data.overallScore || 0} />
            <div style={{ paddingLeft: 18, flex: 1 }}>
              <H2>Summary</H2>
              <ul style={list}>
                <li>Overall similarity: <b>{fmt(data.similarity?.overall)}</b></li>
                <li>Experience alignment: <b>{fmt(data.similarity?.experience)}</b></li>
                <li>Skills alignment: <b>{fmt(data.similarity?.skills)}</b></li>
              </ul>
              <div style={{ marginTop: 10 }}>
                <LabelRow label="Skills coverage" value={`${have.length}/${req.length || 0} (${coverage}%)`} />
                <Progress value={coverage} />
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <H2>ATS Health {isNum(data.atsHealth?.score) ? `· ${data.atsHealth.score}` : ""}</H2>
          <ul style={list}>
            {(data.atsHealth?.checks || []).map((c: any) => (
              <li key={c.name}>
                <span style={{ marginRight: 6 }}>{c.ok ? "✅" : "❌"}</span>
                {c.name}
              </li>
            ))}
          </ul>
        </Card>
      </div>

      {/* Skills */}
      <div style={grid3}>
        <Card>
          <H3>Required skills <Count n={req.length} /></H3>
          <ChipGroup items={req} tone="neutral" />
        </Card>
        <Card>
          <H3>Matched skills <Count n={have.length} /></H3>
          <ChipGroup items={have} tone="good" />
        </Card>
        <Card>
          <H3>Missing skills <Count n={missing.length} /></H3>
          <ChipGroup items={missing} tone="bad" />
        </Card>
      </div>

      {/* Recommendations */}
      <Card>
        <H2>Recommendations</H2>
        {(!data.recommendations || data.recommendations.length === 0) ? (
          <Muted>Looks good. Consider quantifying bullets with impact metrics (%, ms, $, users).</Muted>
        ) : (
          <ul style={list}>
            {data.recommendations.map((r: string, i: number) => <li key={i}>{r}</li>)}
          </ul>
        )}
      </Card>
    </div>
  );
}

/* --- Bits --- */

function Progress({ value }: { value: number }) {
  const v = Math.max(0, Math.min(100, value || 0));
  const hue = Math.round((v / 100) * 120);
  return (
    <div style={{ height: 10, background: "#eef2f7", borderRadius: 999, overflow: "hidden", border: "1px solid #e5e7eb" }}>
      <div style={{ width: `${v}%`, height: "100%", background: `hsl(${hue} 70% 45%)` }} />
    </div>
  );
}

function ChipGroup({ items, tone }: { items: string[]; tone: "good" | "bad" | "neutral" }) {
  if (!items?.length) return <Muted>None</Muted>;
  const styleMap = {
    good: { bg: "#EAFBE7", fg: "#166534", br: "#CBEFC6" },
    bad: { bg: "#FDECEC", fg: "#8A1C1C", br: "#F7CACA" },
    neutral: { bg: "#F1F5F9", fg: "#0F172A", br: "#E2E8F0" },
  }[tone];
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
      {items.map((s) => (
        <span key={s} style={{
          display: "inline-block", padding: "6px 10px", borderRadius: 999,
          background: styleMap.bg, border: `1px solid ${styleMap.br}`, color: styleMap.fg, fontSize: 12
        }}>{s}</span>
      ))}
    </div>
  );
}

function ErrorBanner({ text }: { text: string }) {
  return (
    <div style={{
      padding: "12px 14px",
      borderRadius: 10,
      background: "#fff4f4",
      border: "1px solid #ffd6d6",
      color: "#b00020",
      fontSize: 14
    }}>
      {text}
    </div>
  );
}

function LabelRow({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, color: "#374151", marginBottom: 6 }}>
      <span>{label}</span><span style={{ fontWeight: 700 }}>{value}</span>
    </div>
  );
}

function Count({ n }: { n: number }) {
  return (
    <span style={{
      marginLeft: 8, fontSize: 12, background: "#f3f4f6", padding: "2px 8px",
      borderRadius: 999, color: "#111", border: "1px solid #e5e7eb"
    }}>{n}</span>
  );
}

function Card({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      background: "#fff", border: "1px solid #e5e7eb", borderRadius: 14, padding: 16,
      boxShadow: "0 1px 2px rgba(0,0,0,0.04)"
    }}>
      {children}
    </div>
  );
}

function Muted({ children }: { children: React.ReactNode }) {
  return <div style={{ color: "#6b7280", fontSize: 13 }}>{children}</div>;
}

function H2({ children }: { children: React.ReactNode }) {
  return <h2 style={{ fontSize: 18, fontWeight: 800, margin: "0 0 10px" }}>{children}</h2>;
}

function H3({ children }: { children: React.ReactNode }) {
  return <h3 style={{ fontSize: 15, fontWeight: 700, margin: "0 0 10px", color: "#0f172a" }}>{children}</h3>;
}

const wrap: React.CSSProperties  = { display: "grid", gap: 16 };
const grid2: React.CSSProperties  = { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 };
const grid3: React.CSSProperties  = { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 };
const row: React.CSSProperties    = { display: "flex", alignItems: "center" };
const list: React.CSSProperties   = { margin: 0, paddingLeft: 18, display: "grid", gap: 6, color: "#1f2937", fontSize: 14 };

function isNum(n: any) { return typeof n === "number" && !isNaN(n); }
function fmt(n: any) { return (typeof n === "number") ? n.toFixed(3) : "—"; }
