import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = { title: "Accessibility Statement · Morti Capital" };

export default function Accessibility() {
  return (
    <LegalPage title="Accessibility Statement" updated="November 12, 2026">
      <p>
        Morti Capital intends this website to meet the Web Content Accessibility
        Guidelines (WCAG) 2.1 at Level AA, and to be usable with keyboard,
        screen readers, and reduced-motion preferences.
      </p>

      <h2>What we have in place</h2>
      <ul>
        <li>A language attribute on the page and a skip link to the main content.</li>
        <li>Semantic landmarks for the header, navigation, main area, and footer.</li>
        <li>Visible focus styles and controls that can be used with the keyboard alone, including the cookie banner and the “See each seat” disclosure.</li>
        <li>Text alternatives for meaningful graphics, such as the combined equity chart and the team-stance marker.</li>
        <li>Color that is not the only way to read a result: gains, losses, and mood stances are also labeled in words. Key text is specified to meet a contrast ratio of at least 4.5:1.</li>
        <li>Heading levels that follow the page structure, and form-style buttons that have accessible names.</li>
        <li>A reduced-motion setting that turns off non-essential animation when your system asks for it.</li>
      </ul>

      <h2>Known limits</h2>
      <p>
        Some long record files are published as markdown inside expandable
        sections. They are readable, but they can be dense. The archived Morti 2.0
        table is a simple data table; column headers are present. Automated checks
        are used when pages are built or reviewed; they do not replace human
        testing, and they cannot certify full WCAG 2.1 AA conformance on their own.
      </p>
      <p>
        If we find a barrier, we will note it here and work to fix it.
      </p>

      <h2>How to request help or report a barrier</h2>
      <p>
        If you have trouble using this site, need the content in another format,
        or want to report an accessibility problem, please contact us. We will
        try to respond and to provide a usable alternative.
      </p>
      <p>
        Accessibility feedback: email <a href="mailto:legal@morti.capital">legal@morti.capital</a>.
      </p>

      <h2>Compatibility</h2>
      <p>
        The site is designed to work in current, widely used browsers and with
        common assistive technologies. If a specific combination fails, please
        tell us the browser, device, and assistive technology you were using.
      </p>
    </LegalPage>
  );
}
