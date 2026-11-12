import { formatRoundTime, hasAnyMood, type MoodState, type MoodValue } from "../lib/mood";

const ORDER: MoodValue[] = ["risk-off", "neutral", "risk-on"];

function countLine(mood: MoodState): string {
  const c = mood.counts;
  const bits = [
    `${c["risk-on"]} risk-on`,
    `${c.neutral} neutral`,
    `${c["risk-off"]} risk-off`,
  ];
  if (c["not-given"] > 0) bits.push(`${c["not-given"]} not given`);
  return bits.join(" · ");
}

export function TeamMood({ mood }: { mood: MoodState | null }) {
  const ready = hasAnyMood(mood);
  const stance = mood?.stance;
  const label = mood?.stance_label ?? (mood ? "No mood yet" : "No mood yet");
  const when = formatRoundTime(mood?.round_time_et ?? null);
  const stanceClass = stance ? `mood-pill is-${stance}` : "mood-pill is-empty";

  return (
    <section className="mood wrap" id="mood" aria-labelledby="mood-heading">
      <div className="sec-head">
        <h2 id="mood-heading">Team mood</h2>
        <span>
          {when
            ? `From the ${mood?.cycle} round · ${when}`
            : "The latest round’s risk stance, in the models’ own words."}
        </span>
      </div>

      <div className="mood-card">
        {!ready || !mood ? (
          <div className="mood-empty">
            <p className="mood-stance-label" data-stance="empty">
              No mood yet
            </p>
            <p className="mood-empty-copy">
              No mood or hypothesis was given this round. Seats will show here
              after a cycle is parsed; nothing is filled in for them.
            </p>
          </div>
        ) : (
          <>
            <div className="mood-glance">
              <p className={stanceClass}>
                <span className="mood-stance-k">Team stance</span>
                <span className="mood-stance-v">{label}</span>
              </p>
              <div
                className="mood-gauge"
                role="img"
                aria-label={`Stance marker: ${label}. ${countLine(mood)}.`}
              >
                {ORDER.map((m) => (
                  <span
                    key={m}
                    className={`mood-seg is-${m}${stance === m ? " on" : ""}${stance === "mixed" ? " mixed" : ""}`}
                  >
                    <span className="mood-seg-lab">
                      {m === "risk-on" ? "Risk-on" : m === "risk-off" ? "Risk-off" : "Neutral"}
                    </span>
                  </span>
                ))}
              </div>
            </div>
            <p className="mood-counts">{countLine(mood)}</p>
            <p className="mood-hypo">
              {mood.team_hypothesis ? (
                <>
                  <span className="mood-hypo-k">Team hypothesis</span>
                  {mood.team_hypothesis}
                </>
              ) : (
                <span className="mood-hypo-missing">No team hypothesis was given this round.</span>
              )}
            </p>
          </>
        )}

        {mood && mood.seats.length > 0 && (
          <details className="mood-seats">
            <summary>See each seat</summary>
            <ul>
              {mood.seats.map((s) => (
                <li key={s.id}>
                  <span className="mood-seat-name">{s.name}</span>
                  <span className="mood-seat-mood">{s.mood_label}</span>
                  <span className="mood-seat-line">
                    {s.hypothesis ? `“${s.hypothesis}”` : "No hypothesis given."}
                    {s.round_time_et ? (
                      <span className="mood-seat-time"> · {formatRoundTime(s.round_time_et)}</span>
                    ) : null}
                  </span>
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </section>
  );
}
