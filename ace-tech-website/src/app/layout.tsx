import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Ace Tech Solutions - AI Automation for Business Growth",
  description: "AI automation built for growth. Ace Tech Solutions helps businesses eliminate repetitive tasks and streamline operations — fast, affordable, and custom to your needs.",
  keywords: "AI automation, business automation, workflow automation, AI agents, Bangalore, India",
  authors: [{ name: "Ace Tech Solutions" }],
  openGraph: {
    title: "Ace Tech Solutions - AI Automation for Business Growth",
    description: "AI automation built for growth. Eliminate repetitive tasks and streamline operations with our affordable, custom AI solutions.",
    url: "https://www.acetechsolutions.in",
    siteName: "Ace Tech Solutions",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Ace Tech Solutions - AI Automation for Business Growth",
    description: "AI automation built for growth. Eliminate repetitive tasks and streamline operations with our affordable, custom AI solutions.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <Header />
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
