import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Terms of Service - Ace Tech Solutions',
  description: 'Terms of service for Ace Tech Solutions. Understanding our service terms and conditions.',
};

export default function Terms() {
  return (
    <div className="bg-white">
      <div className="mx-auto max-w-4xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Terms of Service
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Last updated: January 2024
          </p>
        </div>

        <div className="mx-auto mt-16 max-w-none prose prose-lg prose-gray">
          <h2>Agreement to Terms</h2>
          <p>
            By using this website and our services, you agree to the following terms and 
            conditions. If you do not agree with these terms, please do not use our 
            website or services.
          </p>

          <h2>Description of Services</h2>
          <p>
            Ace Tech Solutions provides AI automation and consulting services, including:
          </p>
          <ul>
            <li>Workflow automation solutions</li>
            <li>AI agent development and deployment</li>
            <li>Custom AI integrations</li>
            <li>Consulting and strategy services</li>
            <li>Technical support and maintenance</li>
          </ul>

          <h2>Use of Website</h2>
          <p>
            You may use our website for lawful purposes only. You agree not to:
          </p>
          <ul>
            <li>Use the website in any way that violates applicable laws or regulations</li>
            <li>Transmit or send unsolicited or unauthorized advertising or promotional material</li>
            <li>Attempt to gain unauthorized access to our systems or networks</li>
            <li>Interfere with or disrupt the website or servers</li>
            <li>Use the website to transmit harmful or malicious code</li>
          </ul>

          <h2>Intellectual Property</h2>
          <p>
            All content on this website, including text, graphics, logos, images, and software, 
            is the property of Ace Tech Solutions or its licensors and is protected by 
            copyright and other intellectual property laws.
          </p>

          <h2>Service Terms</h2>
          <p>
            Our professional services are subject to separate contracts and agreements 
            that will be provided when you engage our services. These may include:
          </p>
          <ul>
            <li>Statement of Work (SOW) documents</li>
            <li>Service Level Agreements (SLAs)</li>
            <li>Non-disclosure agreements (NDAs)</li>
            <li>Data processing agreements</li>
          </ul>

          <h2>Payment Terms</h2>
          <p>
            Payment terms for our services will be specified in individual service agreements. 
            Generally:
          </p>
          <ul>
            <li>Invoices are due within 30 days of receipt</li>
            <li>Late payments may incur additional charges</li>
            <li>All fees are non-refundable unless otherwise stated</li>
            <li>Prices are subject to change with notice</li>
          </ul>

          <h2>Confidentiality</h2>
          <p>
            We understand that you may share confidential information with us. We commit to:
          </p>
          <ul>
            <li>Maintaining strict confidentiality of your information</li>
            <li>Using information only for the purpose of providing services</li>
            <li>Implementing appropriate security measures</li>
            <li>Having employees sign confidentiality agreements</li>
          </ul>

          <h2>Warranties and Disclaimers</h2>
          <p>
            While we strive to provide high-quality services, we make no warranties that:
          </p>
          <ul>
            <li>Our services will meet all your requirements</li>
            <li>Our services will be uninterrupted or error-free</li>
            <li>Any results obtained will be accurate or reliable</li>
            <li>Any defects will be corrected</li>
          </ul>

          <h2>Limitation of Liability</h2>
          <p>
            To the fullest extent permitted by law, Ace Tech Solutions shall not be liable 
            for any indirect, incidental, special, or consequential damages arising from 
            the use of our website or services.
          </p>

          <h2>Indemnification</h2>
          <p>
            You agree to indemnify and hold harmless Ace Tech Solutions from any claims, 
            damages, or expenses arising from your use of our website or services, or 
            your violation of these terms.
          </p>

          <h2>Termination</h2>
          <p>
            We may terminate or suspend your access to our website or services at any time, 
            without prior notice, for conduct that we believe violates these terms or is 
            harmful to other users or our business.
          </p>

          <h2>Governing Law</h2>
          <p>
            These terms shall be governed by and construed in accordance with the laws of 
            India. Any disputes arising from these terms shall be subject to the exclusive 
            jurisdiction of courts in Bangalore, India.
          </p>

          <h2>Force Majeure</h2>
          <p>
            We shall not be liable for any delay or failure to perform due to circumstances 
            beyond our reasonable control, including natural disasters, government actions, 
            or technical failures.
          </p>

          <h2>Severability</h2>
          <p>
            If any provision of these terms is found to be unenforceable, the remaining 
            provisions shall continue in full force and effect.
          </p>

          <h2>Changes to Terms</h2>
          <p>
            We reserve the right to change or update these terms without notice. Your 
            continued use of our website after any changes indicates your acceptance 
            of the new terms.
          </p>

          <h2>Contact Information</h2>
          <p>
            For questions about these terms or our services, contact us at:
          </p>
          <p>
            <strong>Email:</strong> <a href="mailto:contact@acetechsolutions.in" className="text-indigo-600 hover:text-indigo-500">contact@acetechsolutions.in</a><br />
            <strong>Address:</strong> Bangalore, India
          </p>

          <div className="mt-12 p-6 bg-gray-50 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Questions About Our Terms?</h3>
            <p className="text-gray-600 mb-4">
              If you have any questions about these terms or need clarification on any 
              aspect of our services, we&apos;re happy to help.
            </p>
            <a 
              href="mailto:contact@acetechsolutions.in?subject=Terms of Service Question"
              className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
            >
              Contact Us
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}