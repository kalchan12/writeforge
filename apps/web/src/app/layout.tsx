import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RightForge | Writing Analysis & Author-Style Platform",
  description: "Local-first writing analysis and author-style research platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
