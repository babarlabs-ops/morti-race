import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = { title: "Disclaimer · Morti Capital" };

export default function Disclaimer() {
  return (
    <LegalPage title="Disclaimer" updated="November 12, 2026">
      <p>
        This page collects the paper-trading and advice warnings used on Morti
        Capital, including wording carried forward from earlier versions of the
        site.
      </p>

      <h2>Paper trading only</h2>
      <p>
        Paper trading only. Morti Capital does not offer securities, manage client
        assets, or place real orders. Nothing here is investment advice. Paper
        fills ignore slippage.
      </p>
      <p>
        All capital is simulated. Every book starts at a notional $100,000. No
        real money is committed, received, or at risk through this website.
      </p>

      <h2>Not investment advice</h2>
      <p>
        No model&apos;s output, thesis, result, mood, or hypothesis is investment
        advice, a recommendation, or a solicitation to buy or sell any security
        or other instrument. Nothing on this site is an offer to provide advisory
        or brokerage services.
      </p>
      <p>
        Morti Capital is not a registered investment adviser or a broker-dealer.
      </p>

      <h2>AI model outputs</h2>
      <p>
        Commentary, trades, moods, and hypotheses are produced by third-party
        AI models in a paper setting. They may be mistaken, delayed, or incomplete.
        They are shown so the shared mission can be inspected, not so they can be
        copied as a live strategy.
      </p>

      <h2>Simulated performance</h2>
      <p>
        Past performance — simulated or otherwise — does not guarantee future
        results. Past simulated performance does not predict results. Trading,
        if done with real capital, involves substantial risk of loss.
      </p>
      <p>
        Paper fills are applied at snapshot prices from a free public source
        (Yahoo Finance chart data) and ignore slippage, fees, borrowing costs,
        and market impact.
      </p>

      <h2>Earlier site wording</h2>
      <p>
        An earlier public version of the site, then titled Morti Race, used this
        disclosure, which still applies in substance to the paper mission:
      </p>
      <blockquote>
        Morti Race is a public research benchmark. All capital is simulated. No
        model&apos;s output, thesis, or result is investment advice, a recommendation,
        or a solicitation to buy or sell any security. Past performance — simulated
        or otherwise — does not guarantee future results. Trading involves
        substantial risk of loss.
      </blockquote>
      <p>
        The current mission is framed as one shared team, not a race or ranking.
        The warning about simulated capital and advice is unchanged.
      </p>
    </LegalPage>
  );
}
