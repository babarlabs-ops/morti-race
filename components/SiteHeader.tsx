import Link from "next/link";

type Props = { current?: "home" | "legal" | "archive" };

export function SiteHeader({ current = "home" }: Props) {
  const onHome = current === "home";
  return (
    <header className="top wrap">
      <Link href="/" className="brand">
        <svg viewBox="0 0 32 32" aria-hidden="true">
          <path d="M7 22 L13 15 L18 18 L25 9" />
        </svg>
        Morti Capital
      </Link>
      <nav className="top-nav" aria-label="Primary">
        {onHome ? (
          <>
            <a href="#mood">Mood</a>
            <a href="#team">Team</a>
            <a href="#mandate">Mandate</a>
            <a href="#record">Record</a>
          </>
        ) : current === "archive" ? (
          <Link href="/">← 3.0 mission</Link>
        ) : (
          <>
            <Link href="/">Mission</Link>
            <Link href="/#mood">Mood</Link>
            <Link href="/#team">Team</Link>
          </>
        )}
      </nav>
    </header>
  );
}
