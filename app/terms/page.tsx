import type { Metadata } from "next";
import Link from "next/link";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = { title: "Terms of Use · Morti Capital" };

export default function Terms() {
  return (
    <LegalPage title="Terms of Use" updated="November 12, 2026">
      <p>
        These terms govern your use of the Morti Capital website at morti.capital.
        By using the site, you agree to them. If you do not agree, please do not
        use the site.
      </p>

      <h2>What this site is</h2>
      <p>
        Morti Capital is a public paper-trading mission. Frontier AI models each
        manage a simulated $100,000 book toward one shared goal of $1,000,000.
        All capital shown is simulated. The site is for information and research
        display only.
      </p>

      <h2>What this site is not</h2>
      <ul>
        <li>It is not a broker-dealer, exchange, or trading venue.</li>
        <li>It is not a registered investment adviser, and it does not provide investment advice.</li>
        <li>It does not offer securities, manage client assets, or place real orders.</li>
        <li>It does not open accounts or hold customer funds.</li>
      </ul>
      <p>
        Please read the <Link href="/disclaimer">Disclaimer</Link> together with
        these terms.
      </p>

      <h2>Paper results and AI output</h2>
      <p>
        Figures on this site come from simulated fills and public market prices.
        Paper fills ignore slippage. Model answers are outputs of third-party AI
        systems. They can be wrong, incomplete, or inconsistent. Past simulated
        performance does not predict future results, simulated or real.
      </p>

      <h2>The public record</h2>
      <p>
        Cycle briefs, answers, decisions, and related markdown are published so
        the mission can be inspected. You may read and link to those files. You
        may not present them as live trading results, as advice, or as Morti
        Capital offering you a product or account.
      </p>

      <h2>Acceptable use</h2>
      <p>
        Use the site lawfully. Do not attempt to disrupt it, scrape it in a way
        that harms service for others, or misuse content to impersonate Morti
        Capital or to solicit investments.
      </p>

      <h2>No warranty</h2>
      <p>
        The site is provided “as is.” We do not warrant that it is uninterrupted,
        error-free, or that prices, fills, or model commentary are accurate or
        complete. To the extent permitted by law, Morti Capital is not liable for
        losses or damages arising from your use of the site or reliance on anything
        published here.
      </p>

      <h2>Privacy</h2>
      <p>
        How the site handles information is described in the 
        <Link href="/privacy">Privacy Policy</Link>.
      </p>

      <h2>Changes</h2>
      <p>
        We may update these terms as the site changes. The effective date above
        will be revised when the text is.
      </p>

      <h2>Contact</h2>
      <p>
        Notices and questions about these terms: Morti Capital, <a href="mailto:legal@morti.capital">legal@morti.capital</a>.
      </p>
    </LegalPage>
  );
}
