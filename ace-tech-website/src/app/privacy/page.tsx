import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy - Ace Tech Solutions',
  description: 'Privacy policy for Ace Tech Solutions. Learn how we protect and handle your personal information.',
};

export default function Privacy() {
  return (
    <div className="bg-white">
      <div className="mx-auto max-w-4xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Privacy Policy
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Last updated: January 2024
          </p>
        </div>

        <div className="mx-auto mt-16 max-w-none prose prose-lg prose-gray">
          <h2>Our Commitment to Privacy</h2>
          <p>
            Ace Tech Solutions is committed to protecting your privacy. We only collect 
            personal information necessary to contact you or deliver services. We do not 
            sell or share your data with third parties.
          </p>

          <h2>Information We Collect</h2>
          <p>
            When you contact us through our website or request our services, we may collect:
          </p>
          <ul>
            <li>Your name and email address</li>
            <li>Company name and job title (if provided)</li>
            <li>Information about your business needs and requirements</li>
            <li>Communication preferences</li>
          </ul>

          <h2>How We Use Your Information</h2>
          <p>
            We use the information you provide to:
          </p>
          <ul>
            <li>Respond to your inquiries and provide customer support</li>
            <li>Deliver our automation and AI services</li>
            <li>Send you information about our services (only if requested)</li>
            <li>Improve our website and services</li>
            <li>Comply with legal obligations</li>
          </ul>

          <h2>Information Sharing</h2>
          <p>
            We do not sell, trade, or otherwise transfer your personal information to third 
            parties without your consent, except in the following circumstances:
          </p>
          <ul>
            <li>When required by law or legal process</li>
            <li>To protect our rights, property, or safety</li>
            <li>With trusted service providers who assist in our operations (under strict confidentiality agreements)</li>
          </ul>

          <h2>Data Security</h2>
          <p>
            We implement appropriate security measures to protect your personal information 
            against unauthorized access, alteration, disclosure, or destruction. This includes:
          </p>
          <ul>
            <li>Encrypted data transmission (SSL/TLS)</li>
            <li>Secure data storage with access controls</li>
            <li>Regular security assessments and updates</li>
            <li>Employee training on data protection</li>
          </ul>

          <h2>Data Retention</h2>
          <p>
            We retain your personal information only as long as necessary to fulfill the 
            purposes for which it was collected and to comply with legal requirements.
          </p>

          <h2>Your Rights</h2>
          <p>
            You have the right to:
          </p>
          <ul>
            <li>Access the personal information we hold about you</li>
            <li>Request correction of inaccurate information</li>
            <li>Request deletion of your personal information</li>
            <li>Object to or restrict processing of your information</li>
            <li>Withdraw consent where processing is based on consent</li>
          </ul>

          <h2>Cookies and Tracking</h2>
          <p>
            Our website may use cookies and similar technologies to improve user experience 
            and analyze website traffic. You can control cookie settings through your browser.
          </p>

          <h2>Children&apos;s Privacy</h2>
          <p>
            Our services are not intended for children under 13 years of age. We do not 
            knowingly collect personal information from children under 13.
          </p>

          <h2>International Data Transfers</h2>
          <p>
            Your information may be transferred to and processed in countries other than 
            your country of residence. We ensure appropriate safeguards are in place to 
            protect your information.
          </p>

          <h2>Changes to This Policy</h2>
          <p>
            We may update this privacy policy from time to time. We will notify you of 
            any significant changes by posting the new policy on our website with an 
            updated revision date.
          </p>

          <h2>Contact Us</h2>
          <p>
            If you have any questions about this privacy policy or our data practices, 
            please contact us at:
          </p>
          <p>
            <strong>Email:</strong> <a href="mailto:contact@acetechsolutions.in" className="text-indigo-600 hover:text-indigo-500">contact@acetechsolutions.in</a><br />
            <strong>Address:</strong> Bangalore, India
          </p>

          <h2>Data Protection Officer</h2>
          <p>
            For data protection inquiries, you may also contact our Data Protection Officer 
            at the email address above.
          </p>

          <div className="mt-12 p-6 bg-gray-50 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Request Data Deletion</h3>
            <p className="text-gray-600 mb-4">
              You may request deletion of your data at any time by contacting us at 
              contact@acetechsolutions.in. We will respond to your request within 30 days.
            </p>
            <a 
              href="mailto:contact@acetechsolutions.in?subject=Data Deletion Request"
              className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
            >
              Request Data Deletion
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}