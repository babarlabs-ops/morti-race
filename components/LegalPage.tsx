import type { ReactNode } from "react";
import { SiteFooter } from "./SiteFooter";
import { SiteHeader } from "./SiteHeader";

type Props = {
  title: string;
  updated: string;
  children: ReactNode;
};

export function LegalPage({ title, updated, children }: Props) {
  return (
    <>
      <SiteHeader current="legal" />
      <main id="content" className="legal wrap">
        <p className="eyebrow">Morti Capital</p>
        <h1>{title}</h1>
        <p className="legal-updated">Effective {updated}. This page describes the morti.capital website as it works today.</p>
        <article className="legal-body">{children}</article>
      </main>
      <SiteFooter />
    </>
  );
}
