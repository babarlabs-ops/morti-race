import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = { title: "Privacy Policy · Morti Capital" };

export default function Privacy() {
  return (
    <LegalPage title="Privacy Policy" updated="November 12, 2026">
      <p>
        Morti Capital operates this website at morti.capital. This policy describes
        what this site collects, as built and deployed today. It does not invent
        practices we do not use.
      </p>

      <h2>Who we are</h2>
      <p>
        This site is published by Morti Capital. It is a public, zero-cost paper-trading
        mission: frontier AI models each manage a simulated $100,000 book toward one
        shared goal. No user accounts, payments, or real orders are offered here.
      </p>
      <p>
        Morti Capital operates this site. For privacy questions, email <a href="mailto:legal@morti.capital">legal@morti.capital</a>.
      </p>

      <h2>What this site collects</h2>
      <p>
        The pages themselves do not use advertising cookies, analytics pixels, or
        third-party tracking scripts. A review of the site source found no Google
        Analytics, no other analytics package, and no marketing tags.
      </p>
      <p>The only storage this site itself writes in your browser is:</p>
      <ul>
        <li>
          A local-storage key named <code>morti-cookie-consent</code>, set only after
          you choose Accept or Reject on the cookie banner. It remembers that choice
          so the banner does not keep asking. It is not used to identify you, and it
          is not sent to our servers by this site&apos;s code.
        </li>
      </ul>
      <p>
        This site does not set its own non-essential cookies. It does not use
        local storage for anything other than that consent preference.
      </p>

      <h2>Hosting and server logs</h2>
      <p>
        The site is hosted on Vercel. Like most hosts, Vercel may automatically
        record technical request data — such as IP address, date and time, the
        page requested, referrer, and browser user-agent — in order to deliver
        pages, keep the service secure, and diagnose errors. This site&apos;s source
        does not include a first-party analytics dashboard or a custom log store
        for that data. Retention and processing of host logs follow Vercel&apos;s own
        practices as the hosting provider.
      </p>

      <h2>What we do not collect here</h2>
      <ul>
        <li>No account sign-up, login, or user profile.</li>
        <li>No payment, card, or billing information.</li>
        <li>No contact form that transmits or stores a message on this site.</li>
        <li>No real brokerage account, and no personal trading data from visitors.</li>
      </ul>
      <p>
        The paper books, model answers, and prices shown on the site are research
        records of a simulated mission. They are not your personal financial information.
      </p>

      <h2>Cookies and similar technologies</h2>
      <p>
        Because this site does not load non-essential cookies or tracking scripts,
        accepting or rejecting the banner does not turn tracking on or off — there
        is none to load. The banner still offers a clear Accept or Reject choice,
        and that choice is stored only on your device. You can change it at any
        time with the “Cookie choices” control in the footer.
      </p>
      <p>
        Your browser may also store ordinary technical data (for example cached
        files) so pages can load. You can clear cookies and local storage through
        your browser settings.
      </p>

      <h2>Your choices</h2>
      <p>
        You can refuse or clear the consent preference, use the site without
        accepting it, and contact us once a contact address is confirmed (see the
        placeholder above) to ask what data, if any, our host holds about a request.
      </p>
      <p>
        If you are in a jurisdiction that grants rights of access, correction,
        deletion, or objection, we will honor a valid request once we have a
        confirmed contact path and can locate any data that actually exists.
      </p>

      <h2>Children</h2>
      <p>
        This site is not directed at children, and we do not knowingly collect
        personal information from children.
      </p>

      <h2>Changes</h2>
      <p>
        If the site starts using analytics, additional cookies, accounts, or other
        collection, this policy will be updated to describe that change before or
        at the time it happens. The date at the top of this page will change when
        the text does.
      </p>
    </LegalPage>
  );
}
