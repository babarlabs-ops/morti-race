"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export const CONSENT_KEY = "morti-cookie-consent";
const OPEN_EVENT = "morti:open-consent";

type Choice = "accepted" | "rejected";

function readChoice(): Choice | null {
  try {
    const v = window.localStorage.getItem(CONSENT_KEY);
    if (v === "accepted" || v === "rejected") return v;
  } catch {
    /* localStorage may be blocked */
  }
  return null;
}

function writeChoice(choice: Choice) {
  try {
    window.localStorage.setItem(CONSENT_KEY, choice);
  } catch {
    /* ignore quota / private-mode failures; the banner may reappear */
  }
}

export function CookieBanner() {
  const [ready, setReady] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setOpen(readChoice() === null);
    setReady(true);
    const onOpen = () => setOpen(true);
    window.addEventListener(OPEN_EVENT, onOpen);
    return () => window.removeEventListener(OPEN_EVENT, onOpen);
  }, []);

  useEffect(() => {
    document.body.classList.toggle("consent-open", ready && open);
    return () => document.body.classList.remove("consent-open");
  }, [ready, open]);

  function choose(choice: Choice) {
    writeChoice(choice);
    setOpen(false);
  }

  if (!ready || !open) return null;

  return (
    <div
      className="consent"
      role="region"
      aria-labelledby="consent-title"
      aria-describedby="consent-copy"
    >
      <div className="consent-inner wrap">
        <div className="consent-copy">
          <p id="consent-title" className="consent-title">Cookie choice</p>
          <p id="consent-copy">
            This site does not use non-essential cookies or tracking scripts.
            We only store your choice on this device, in local storage, so we
            do not ask again. You can accept or reject that preference.{" "}
            <Link href="/privacy">Privacy Policy</Link>
          </p>
        </div>
        <div className="consent-actions">
          <button type="button" className="consent-btn primary" onClick={() => choose("accepted")}>
            Accept
          </button>
          <button type="button" className="consent-btn" onClick={() => choose("rejected")}>
            Reject
          </button>
        </div>
      </div>
    </div>
  );
}

export function CookieSettingsButton() {
  return (
    <button
      type="button"
      className="foot-linkbtn"
      onClick={() => window.dispatchEvent(new Event(OPEN_EVENT))}
    >
      Cookie choices
    </button>
  );
}
