import type { Metadata } from 'next';
import Link from 'next/link';
import { 
  ArrowPathIcon, 
  ChatBubbleLeftRightIcon, 
  WrenchScrewdriverIcon,
  CheckIcon
} from '@heroicons/react/24/outline';

export const metadata: Metadata = {
  title: 'Our Services - Ace Tech Solutions',
  description: 'Explore our AI automation services: Workflow Automation, AI Agents-as-a-Service, and Custom AI Solutions. Smart automation tailored to your business needs.',
};

const services = [
  {
    name: 'Workflow Automation',
    description: 'Automate recurring business processes — from onboarding to invoice handling.',
    icon: ArrowPathIcon,
    useCases: [
      'CRM updates and data synchronization',
      'Email triage and response automation',
      'Document processing and classification',
      'Task assignments and follow-ups',
      'Report generation and distribution',
      'Lead scoring and qualification'
    ],
    benefits: [
      'Reduce manual errors by 95%',
      'Save 20+ hours per week per employee',
      'Improve process consistency',
      'Scale operations without hiring'
    ]
  },
  {
    name: 'AI Agents-as-a-Service',
    description: 'Custom AI agents that function like digital employees — answering questions, handling requests, and integrating across your tools.',
    icon: ChatBubbleLeftRightIcon,
    useCases: [
      'HR Assistant (scheduling, document collection)',
      'Finance Bot (report generation, data entry)',
      'Support Agent (auto-reply, ticket categorization)',
      'Sales Assistant (lead qualification, follow-ups)',
      'Knowledge Base Manager (content updates, FAQs)',
      'Compliance Monitor (policy checks, alerts)'
    ],
    benefits: [
      '24/7 availability for your team',
      'Instant responses to common queries',
      'Reduced workload on human staff',
      'Consistent service quality'
    ]
  },
  {
    name: 'Custom AI Solutions',
    description: 'We integrate AI into your existing workflows and tools — building LLM-driven tools, RAG apps, and smart APIs customized to your exact needs.',
    icon: WrenchScrewdriverIcon,
    useCases: [
      'RAG (Retrieval-Augmented Generation) applications',
      'Custom LLM integrations',
      'Intelligent document analysis',
      'Predictive analytics dashboards',
      'Smart API development',
      'AI-powered search and recommendations'
    ],
    benefits: [
      'Tailored to your specific use case',
      'Seamless integration with existing systems',
      'Scalable architecture',
      'Ongoing support and optimization'
    ]
  }
];

const engagementOptions = [
  {
    name: 'One-time Implementation',
    description: 'Perfect for specific automation projects with clear scope and deliverables.',
    features: ['Fixed scope and timeline', 'Comprehensive documentation', '30-day support included', 'Training for your team']
  },
  {
    name: 'Retainer-based Optimization',
    description: 'Ongoing partnership for continuous improvement and new automation opportunities.',
    features: ['Monthly optimization reviews', 'Priority support', 'New automation identification', 'Performance monitoring']
  },
  {
    name: 'API/SDK Access',
    description: 'Direct access to our automation tools and platforms for technical teams.',
    features: ['REST API access', 'SDK documentation', 'Technical support', 'Usage analytics'],
    badge: 'Coming Soon'
  }
];

export default function Services() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Smart Automation. Tailored to Your Business.
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            From workflow automation to custom AI agents, we build solutions that eliminate 
            busywork and amplify your team&apos;s impact.
          </p>
        </div>
      </div>

      {/* Services Detail */}
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="space-y-24">
          {services.map((service, index) => (
            <div key={service.name} className={`grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16 ${index % 2 === 1 ? 'lg:grid-flow-col-dense' : ''}`}>
              <div className={`${index % 2 === 1 ? 'lg:col-start-2' : ''}`}>
                <div className="flex items-center">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-600">
                    <service.icon className="h-8 w-8 text-white" aria-hidden="true" />
                  </div>
                  <h2 className="ml-4 text-3xl font-bold tracking-tight text-gray-900">
                    {service.name}
                  </h2>
                </div>
                <p className="mt-6 text-lg leading-8 text-gray-600">
                  {service.description}
                </p>
                
                <div className="mt-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Benefits:</h3>
                  <ul className="space-y-2">
                    {service.benefits.map((benefit) => (
                      <li key={benefit} className="flex items-center text-gray-600">
                        <CheckIcon className="h-5 w-5 text-green-600 mr-3 flex-shrink-0" />
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div className={`${index % 2 === 1 ? 'lg:col-start-1 lg:row-start-1' : ''}`}>
                <div className="bg-gray-50 rounded-lg p-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Use Cases:</h3>
                  <ul className="space-y-3">
                    {service.useCases.map((useCase) => (
                      <li key={useCase} className="flex items-start text-gray-600">
                        <span className="text-indigo-600 mr-3 mt-1">•</span>
                        {useCase}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <div className="mx-auto max-w-7xl px-6 py-24 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Our Technology Stack
          </h2>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            We use cutting-edge technologies to build robust, scalable automation solutions.
          </p>
        </div>
        <div className="mx-auto mt-16 grid max-w-lg gap-4 lg:max-w-4xl lg:grid-cols-4">
          {['OpenAI', 'LangChain', 'Pinecone', 'NestJS', 'FastAPI', 'React', 'TypeScript', 'Python'].map((tech) => (
            <div key={tech} className="flex items-center justify-center rounded-lg bg-gray-50 px-6 py-4">
              <span className="text-sm font-medium text-gray-900">{tech}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Engagement Options */}
      <div className="bg-gray-50">
        <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Engagement Options
            </h2>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Choose the engagement model that works best for your business needs and timeline.
            </p>
          </div>
          <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 lg:max-w-none lg:grid-cols-3">
            {engagementOptions.map((option) => (
              <div key={option.name} className="rounded-lg bg-white p-8 shadow-sm ring-1 ring-gray-900/10">
                <div className="flex items-center">
                  <h3 className="text-lg font-semibold leading-8 text-gray-900">
                    {option.name}
                  </h3>
                  {option.badge && (
                    <span className="ml-3 inline-flex items-center rounded-full bg-indigo-100 px-2.5 py-0.5 text-xs font-medium text-indigo-800">
                      {option.badge}
                    </span>
                  )}
                </div>
                <p className="mt-4 text-sm leading-6 text-gray-600">
                  {option.description}
                </p>
                <ul className="mt-6 space-y-3">
                  {option.features.map((feature) => (
                    <li key={feature} className="flex items-center text-sm text-gray-600">
                      <CheckIcon className="h-4 w-4 text-green-600 mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Let&apos;s automate your hardest workflows.
          </h2>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Ready to see how AI automation can transform your business? Let&apos;s start with a free assessment.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link
              href="/contact"
              className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Request a Free Assessment
            </Link>
            <Link href="/about" className="text-sm font-semibold leading-6 text-gray-900">
              Learn more about us <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}