import type { Metadata } from 'next';
import ContactForm from '@/components/ContactForm';
import { MapPinIcon, EnvelopeIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

export const metadata: Metadata = {
  title: 'Contact Us - Ace Tech Solutions',
  description: 'Get in touch with Ace Tech Solutions. Whether you need automation consulting, AI solutions, or just want to chat about your business needs.',
};

export default function Contact() {
  return (
    <div className="bg-white">
      <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Let&apos;s Talk AI — Without the Buzzwords
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Whether you need a quick automation, a full AI roadmap, or just a consultation, 
            we&apos;re here to help. No sales pressure, just practical solutions.
          </p>
        </div>

        <div className="mx-auto mt-16 grid max-w-lg gap-12 lg:max-w-none lg:grid-cols-2 lg:gap-16">
          {/* Contact Information */}
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-gray-900">Get in touch</h2>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              We respond to all inquiries within 24 hours. For urgent requests, 
              feel free to call or message us directly.
            </p>
            
            <dl className="mt-10 space-y-6">
              <div className="flex gap-x-4">
                <dt className="flex-none">
                  <span className="sr-only">Address</span>
                  <MapPinIcon className="h-7 w-6 text-gray-600" aria-hidden="true" />
                </dt>
                <dd className="text-gray-600">
                  <strong className="font-semibold text-gray-900">Office:</strong><br />
                  Bangalore, India
                </dd>
              </div>
              
              <div className="flex gap-x-4">
                <dt className="flex-none">
                  <span className="sr-only">Email</span>
                  <EnvelopeIcon className="h-7 w-6 text-gray-600" aria-hidden="true" />
                </dt>
                <dd className="text-gray-600">
                  <strong className="font-semibold text-gray-900">Email:</strong><br />
                  <a href="mailto:contact@acetechsolutions.in" className="text-indigo-600 hover:text-indigo-500">
                    contact@acetechsolutions.in
                  </a>
                </dd>
              </div>
              
              <div className="flex gap-x-4">
                <dt className="flex-none">
                  <span className="sr-only">Website</span>
                  <GlobeAltIcon className="h-7 w-6 text-gray-600" aria-hidden="true" />
                </dt>
                <dd className="text-gray-600">
                  <strong className="font-semibold text-gray-900">Website:</strong><br />
                  <a href="https://www.acetechsolutions.in" className="text-indigo-600 hover:text-indigo-500">
                    www.acetechsolutions.in
                  </a>
                </dd>
              </div>
            </dl>

            {/* Social Links */}
            <div className="mt-10">
              <h3 className="text-sm font-semibold leading-6 text-gray-900">Follow us</h3>
              <div className="mt-6 flex gap-x-6">
                <a href="#" className="text-gray-400 hover:text-gray-500">
                  <span className="sr-only">LinkedIn</span>
                  <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path
                      fillRule="evenodd"
                      d="M16.338 16.338H13.67V12.16c0-.995-.017-2.277-1.387-2.277-1.39 0-1.601 1.086-1.601 2.207v4.248H8.014v-8.59h2.559v1.174h.037c.356-.675 1.227-1.387 2.526-1.387 2.703 0 3.203 1.778 3.203 4.092v4.711zM5.005 6.575a1.548 1.548 0 11-.003-3.096 1.548 1.548 0 01.003 3.096zm-1.337 9.763H6.34v-8.59H3.667v8.59zM17.668 1H2.328C1.595 1 1 1.581 1 2.298v15.403C1 18.418 1.595 19 2.328 19h15.34c.734 0 1.332-.582 1.332-1.299V2.298C19 1.581 18.402 1 17.668 1z"
                      clipRule="evenodd"
                    />
                  </svg>
                </a>
              </div>
            </div>

            {/* What to expect */}
            <div className="mt-10">
              <h3 className="text-sm font-semibold leading-6 text-gray-900">What to expect</h3>
              <div className="mt-6 space-y-4">
                <div className="flex gap-x-3">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-white text-xs font-semibold">1</div>
                  <p className="text-sm text-gray-600">
                    <strong>Initial response</strong> within 24 hours to schedule a call
                  </p>
                </div>
                <div className="flex gap-x-3">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-white text-xs font-semibold">2</div>
                  <p className="text-sm text-gray-600">
                    <strong>Discovery call</strong> to understand your needs and challenges
                  </p>
                </div>
                <div className="flex gap-x-3">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-white text-xs font-semibold">3</div>
                  <p className="text-sm text-gray-600">
                    <strong>Custom proposal</strong> with timeline and investment details
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <ContactForm />
        </div>

        {/* FAQ Section */}
        <div className="mx-auto mt-24 max-w-2xl">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900 text-center mb-12">
            Frequently Asked Questions
          </h2>
          <dl className="space-y-8">
            <div>
              <dt className="text-lg font-semibold leading-7 text-gray-900">
                How quickly can you implement an automation solution?
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Simple workflow automations can often be implemented within 1-2 weeks. 
                More complex AI agents and custom solutions typically take 3-6 weeks, 
                depending on scope and integration requirements.
              </dd>
            </div>
            
            <div>
              <dt className="text-lg font-semibold leading-7 text-gray-900">
                Do you work with companies outside of India?
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Absolutely! While we&apos;re based in Bangalore, we work with clients globally. 
                We&apos;re experienced in remote collaboration and can work across different time zones.
              </dd>
            </div>
            
            <div>
              <dt className="text-lg font-semibold leading-7 text-gray-900">
                What&apos;s included in a free consultation?
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                We&apos;ll discuss your current processes, identify automation opportunities, 
                and provide a high-level roadmap. There&apos;s no obligation, and you&apos;ll leave 
                with actionable insights regardless of whether we work together.
              </dd>
            </div>
            
            <div>
              <dt className="text-lg font-semibold leading-7 text-gray-900">
                Do you provide ongoing support after implementation?
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Yes! All implementations include 30 days of support. We also offer 
                retainer-based ongoing optimization and maintenance services.
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
}