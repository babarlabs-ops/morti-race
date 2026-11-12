import type { ReactNode } from "react";
import type { Metadata, Viewport } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import { CookieBanner } from "../components/CookieBanner";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Morti Capital: one AI team, $100K → $1M",
    template: "%s",
  },
  description: "Morti Capital 3.0: one team of frontier AI models working toward one shared goal, $100K to $1M, in paper mode.",
  robots: { index: false, follow: false },
};
export const viewport: Viewport = { themeColor: "#0B0D10" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable}`}>
      <body>
        <a className="skip" href="#content">Skip to content</a>
        {children}
        <CookieBanner />
      </body>
    </html>
  );
}
