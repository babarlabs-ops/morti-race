import type { NextConfig } from "next";

/**
 * Strict same-origin policy for a site that loads only its own Next.js
 * chunks, self-hosted Geist fonts, /record markdown, and inline SVG.
 * Next.js inlines its hydration bootstrap, and the mission meter uses inline
 * style attributes, so this policy is sent as Content-Security-Policy-Report-Only.
 * Enforcing the same directives blocks those inline scripts (the cookie banner
 * never hydrates) and drops the meter widths.
 * Browsers log violations locally. There is no report endpoint.
 */
const contentSecurityPolicy = [
  "default-src 'self'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  "frame-src 'none'",
  "object-src 'none'",
  "script-src 'self'",
  "style-src 'self'",
  "font-src 'self'",
  "img-src 'self' data:",
  "connect-src 'self'",
  "worker-src 'self'",
  "manifest-src 'self'",
  "media-src 'none'",
].join("; ");

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Permissions-Policy",
    value: [
      "accelerometer=()",
      "autoplay=()",
      "camera=()",
      "display-capture=()",
      "encrypted-media=()",
      "fullscreen=()",
      "geolocation=()",
      "gyroscope=()",
      "hid=()",
      "idle-detection=()",
      "magnetometer=()",
      "microphone=()",
      "midi=()",
      "payment=()",
      "picture-in-picture=()",
      "screen-wake-lock=()",
      "serial=()",
      "usb=()",
      "xr-spatial-tracking=()",
    ].join(", "),
  },
  // Same value https://morti.capital serves today. Vercel adds
  // "; includeSubDomains; preload" only on *.vercel.app.
  { key: "Strict-Transport-Security", value: "max-age=63072000" },
  { key: "Content-Security-Policy-Report-Only", value: contentSecurityPolicy },
];

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};

export default nextConfig;
