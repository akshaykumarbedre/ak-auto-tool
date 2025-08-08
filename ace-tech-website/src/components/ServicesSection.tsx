import Link from 'next/link';
import { 
  ArrowPathIcon, 
  ChatBubbleLeftRightIcon, 
  WrenchScrewdriverIcon 
} from '@heroicons/react/24/outline';

const services = [
  {
    name: 'Workflow Automation',
    description: 'Automate repetitive business tasks across teams and tools.',
    icon: ArrowPathIcon,
    features: ['CRM updates', 'Email triage', 'Document processing', 'Task assignments'],
  },
  {
    name: 'AI Agents-as-a-Service',
    description: 'Digital workers trained to handle support, HR, finance, and more.',
    icon: ChatBubbleLeftRightIcon,
    features: ['HR Assistant', 'Finance Bot', 'Support Agent', 'Custom Agents'],
  },
  {
    name: 'Custom AI Integration',
    description: 'Seamless integration of AI into your existing systems.',
    icon: WrenchScrewdriverIcon,
    features: ['LLM-driven tools', 'RAG applications', 'Smart APIs', 'Custom solutions'],
  },
];

export default function ServicesSection() {
  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-indigo-600">Smart Automation</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Tailored to Your Business
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            We believe that intelligent automation should be accessible to every business — not just the big players. 
            That&apos;s why we provide tailored AI solutions that deliver real impact without draining your budget.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-3 lg:gap-y-16">
            {services.map((service) => (
              <div key={service.name} className="relative pl-16">
                <dt className="text-base font-semibold leading-7 text-gray-900">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
                    <service.icon className="h-6 w-6 text-white" aria-hidden="true" />
                  </div>
                  {service.name}
                </dt>
                <dd className="mt-2 text-base leading-7 text-gray-600">
                  {service.description}
                  <ul className="mt-4 space-y-2">
                    {service.features.map((feature) => (
                      <li key={feature} className="flex items-center text-sm text-gray-500">
                        <span className="mr-2">•</span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </dd>
              </div>
            ))}
          </dl>
        </div>
        
        {/* Why Ace Tech section */}
        <div className="mx-auto mt-24 max-w-2xl lg:max-w-4xl">
          <div className="text-center">
            <h3 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
              Why Ace Tech?
            </h3>
            <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-3">
              <div className="rounded-lg bg-gray-50 p-6">
                <div className="text-lg font-semibold text-gray-900">✅ 100% Client-focused</div>
                <div className="mt-2 text-sm text-gray-600">Solutions tailored to your goals</div>
              </div>
              <div className="rounded-lg bg-gray-50 p-6">
                <div className="text-lg font-semibold text-gray-900">✅ Built for speed and scale</div>
                <div className="mt-2 text-sm text-gray-600">Fast implementation, scalable results</div>
              </div>
              <div className="rounded-lg bg-gray-50 p-6">
                <div className="text-lg font-semibold text-gray-900">✅ Bangalore-based, globally focused</div>
                <div className="mt-2 text-sm text-gray-600">Local expertise, international reach</div>
              </div>
            </div>
          </div>
        </div>

        {/* Case Study */}
        <div className="mx-auto mt-24 max-w-2xl text-center">
          <div className="rounded-lg bg-indigo-50 p-8">
            <blockquote className="text-xl font-semibold leading-8 text-gray-900">
              &ldquo;Cut processing time by 85% for a logistics firm in under 3 weeks.&rdquo;
            </blockquote>
            <div className="mt-6">
              <Link
                href="/contact"
                className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-colors"
              >
                Book a Free Consultation
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}