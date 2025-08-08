import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'About Us - Ace Tech Solutions',
  description: 'Learn about Ace Tech Solutions, a Bangalore-based AI automation company helping businesses modernize their operations through intelligent automation.',
};

export default function About() {
  return (
    <div className="bg-white">
      <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
        {/* Hero Section */}
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Who We Are
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Ace Tech Solutions is a Bangalore-based AI automation company helping businesses 
            modernize their operations through intelligent automation. We&apos;re a lean team of 
            engineers, product thinkers, and problem solvers — passionate about delivering results, not complexity.
          </p>
        </div>

        {/* Values Section */}
        <div className="mx-auto mt-16 max-w-2xl lg:mx-0 lg:max-w-none">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Our Values</h2>
          <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-3">
            <div className="flex flex-col">
              <div className="mb-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-lg font-semibold leading-8 text-gray-900">Client First</h3>
              <p className="mt-2 text-base leading-7 text-gray-600">
                Your goals guide everything we build. We prioritize understanding your unique needs 
                and delivering solutions that drive real business value.
              </p>
            </div>

            <div className="flex flex-col">
              <div className="mb-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423L16.5 15.75l.394 1.183a2.25 2.25 0 001.423 1.423L19.5 18.75l-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-lg font-semibold leading-8 text-gray-900">Practical AI</h3>
              <p className="mt-2 text-base leading-7 text-gray-600">
                No hype. Just real solutions. We focus on AI applications that solve actual 
                business problems and deliver measurable improvements.
              </p>
            </div>

            <div className="flex flex-col">
              <div className="mb-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                  <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-lg font-semibold leading-8 text-gray-900">Affordable Impact</h3>
              <p className="mt-2 text-base leading-7 text-gray-600">
                Enterprise-grade results, startup-friendly pricing. We believe powerful 
                automation should be accessible to businesses of all sizes.
              </p>
            </div>
          </div>
        </div>

        {/* Story Section */}
        <div className="mx-auto mt-16 max-w-2xl lg:mx-0 lg:max-w-none">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Our Story</h2>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Founded in Bangalore by a team with deep startup and enterprise experience, Ace Tech Solutions 
            began with a simple mission: bring the power of automation to businesses that need it most — 
            without the expensive overhead or bloated platforms.
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            We saw too many companies struggling with manual processes, spending countless hours on 
            repetitive tasks that could be automated. Meanwhile, enterprise automation solutions were 
            either too expensive or too complex for growing businesses to implement effectively.
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            That&apos;s why we built Ace Tech Solutions — to bridge that gap with practical, affordable AI 
            automation that grows with your business.
          </p>
        </div>

        {/* Team Section */}
        <div className="mx-auto mt-16 max-w-2xl lg:mx-0 lg:max-w-none">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Meet the Team</h2>
          <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-3">
            <div className="text-center">
              <div className="mx-auto h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                <span className="text-2xl font-bold text-indigo-600">R</span>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">Rohan</h3>
              <p className="text-sm text-gray-600">Founder & AI Engineer</p>
              <p className="mt-2 text-sm text-gray-500">
                Leading AI implementations and technical strategy
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                <span className="text-2xl font-bold text-indigo-600">P</span>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">Priya</h3>
              <p className="text-sm text-gray-600">Product & Customer Success</p>
              <p className="mt-2 text-sm text-gray-500">
                Ensuring our solutions meet real-world business needs
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto h-24 w-24 rounded-full bg-indigo-100 flex items-center justify-center">
                <span className="text-2xl font-bold text-indigo-600">A</span>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900">Ankit</h3>
              <p className="text-sm text-gray-600">Automation Architect</p>
              <p className="mt-2 text-sm text-gray-500">
                Designing and implementing complex automation workflows
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mx-auto mt-16 max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Want to work with us or learn more?
          </h2>
          <div className="mt-8 flex items-center justify-center gap-x-6">
            <Link
              href="/contact"
              className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Contact Us
            </Link>
            <Link href="/services" className="text-sm font-semibold leading-6 text-gray-900">
              View Our Services <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}