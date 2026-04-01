import "./globals.css";

import type { Metadata } from "next";


export const metadata: Metadata = {
  title: "AI News Briefing MVP",
  description: "Personalized daily and on-demand AI news briefings"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="mx-auto min-h-screen max-w-6xl px-4 py-8 sm:px-6">{children}</main>
      </body>
    </html>
  );
}
