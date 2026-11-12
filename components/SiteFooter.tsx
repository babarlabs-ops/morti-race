import Link from "next/link";
import { CookieSettingsButton } from "./CookieBanner";

type Props = {
  disclaimer?: string;
};

const DEFAULT =
  "Paper trading only. Morti Capital does not offer securities, manage client assets, or place real orders. Nothing here is investment advice. Paper fills ignore slippage.";

export function SiteFooter({ disclaimer = DEFAULT }: Props) {
  return (
    <footer className="foot wrap">
      <p className="foot-disc">
        {disclaimer}{" "}
        <Link href="/disclaimer">Full disclaimer</Link>
      </p>
      <nav className="foot-links" aria-label="Legal">
        <Link href="/privacy">Privacy Policy</Link>
        <Link href="/terms">Terms of Use</Link>
        <Link href="/disclaimer">Disclaimer</Link>
        <Link href="/accessibility">Accessibility</Link>
        <CookieSettingsButton />
      </nav>
    </footer>
  );
}
