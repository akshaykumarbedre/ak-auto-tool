import "./globals.css";
import Header from "../components/Header";
import Footer from "../components/Footer";

export const metadata = {
  title: "Ace Tech Solutions - AI Automation Company",
  description: "Bangalore-based startup focused on affordable, high-impact AI automation services. Automate the busywork, scale what matters.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Header />
        <main>
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
