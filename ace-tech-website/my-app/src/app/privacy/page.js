export const metadata = {
  title: "Privacy Policy - Ace Tech Solutions",
  description: "Privacy Policy for Ace Tech Solutions. Learn how we collect, use, and protect your personal information.",
};

export default function Privacy() {
  return (
    <div className="bg-white">
      <section className="py-16 lg:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8">
            Privacy Policy
          </h1>
          
          <div className="prose prose-lg max-w-none">
            <p className="text-lg text-gray-600 mb-8">
              Last updated: January 2024
            </p>

            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Information We Collect</h2>
                <p className="text-gray-700 leading-relaxed">
                  Ace Tech Solutions is committed to protecting your privacy. We only collect personal information necessary to contact you or deliver services. This includes:
                </p>
                <ul className="list-disc pl-6 mt-4 space-y-2 text-gray-700">
                  <li>Name and email address when you contact us</li>
                  <li>Company information if voluntarily provided</li>
                  <li>Communication preferences</li>
                  <li>Technical information necessary for service delivery</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">How We Use Your Information</h2>
                <p className="text-gray-700 leading-relaxed">
                  We use the information we collect to:
                </p>
                <ul className="list-disc pl-6 mt-4 space-y-2 text-gray-700">
                  <li>Respond to your inquiries and provide customer support</li>
                  <li>Deliver our AI automation services</li>
                  <li>Send you relevant updates about our services (with your consent)</li>
                  <li>Improve our website and services</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Information Sharing</h2>
                <p className="text-gray-700 leading-relaxed">
                  We do not sell, trade, or otherwise transfer your personal information to third parties. We may share information only in the following circumstances:
                </p>
                <ul className="list-disc pl-6 mt-4 space-y-2 text-gray-700">
                  <li>With your explicit consent</li>
                  <li>To comply with legal obligations</li>
                  <li>With trusted service providers who assist in our operations (under strict confidentiality agreements)</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Data Security</h2>
                <p className="text-gray-700 leading-relaxed">
                  We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Rights</h2>
                <p className="text-gray-700 leading-relaxed">
                  You have the right to:
                </p>
                <ul className="list-disc pl-6 mt-4 space-y-2 text-gray-700">
                  <li>Access the personal information we hold about you</li>
                  <li>Request correction of inaccurate information</li>
                  <li>Request deletion of your personal information</li>
                  <li>Withdraw consent for marketing communications</li>
                </ul>
                <p className="text-gray-700 leading-relaxed mt-4">
                  You may request deletion of your data at any time by contacting us at contact@acetechsolutions.in.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Cookies and Tracking</h2>
                <p className="text-gray-700 leading-relaxed">
                  We use essential cookies to ensure our website functions properly. We do not use tracking cookies or analytics that identify individual users without consent.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Changes to This Policy</h2>
                <p className="text-gray-700 leading-relaxed">
                  We may update this privacy policy from time to time. We will notify you of any significant changes by posting the new policy on this page.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Contact Us</h2>
                <p className="text-gray-700 leading-relaxed">
                  If you have any questions about this Privacy Policy, please contact us:
                </p>
                <div className="mt-4 p-6 bg-gray-50 rounded-lg">
                  <p className="text-gray-700">
                    <strong>Ace Tech Solutions</strong><br />
                    Email: contact@acetechsolutions.in<br />
                    Location: Bangalore, India
                  </p>
                </div>
              </section>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}