type Props = { score: number; size?: number; label?: string };

export default function ScoreDial({ score, size = 140, label = "Match Score" }: Props) {
  const clamped = Math.max(0, Math.min(100, Number(score) || 0));
  const stroke = 14;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const filled = (clamped / 100) * c;
  const hue = Math.round((clamped / 100) * 120); // 0 red → 120 green

  return (
    <div style={{ display: "grid", placeItems: "center" }}>
      <svg width={size} height={size} style={{ overflow: "visible" }}>
        <g transform={`translate(${size / 2}, ${size / 2})`}>
          <circle r={r} fill="none" stroke="#eee" strokeWidth={stroke} />
          <circle
            r={r}
            fill="none"
            stroke={`hsl(${hue} 70% 45%)`}
            strokeWidth={stroke}
            strokeDasharray={`${filled} ${c - filled}`}
            strokeLinecap="round"
            transform="rotate(-90)"
          />
          <text
            textAnchor="middle"
            dominantBaseline="central"
            fontWeight={800}
            fontFamily="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
            fontSize={28}
            fill="#111"
          >
            {clamped}
          </text>
        </g>
      </svg>
      <div style={{ marginTop: 8, color: "#555", fontSize: 12 }}>{label}</div>
    </div>
  );
}
