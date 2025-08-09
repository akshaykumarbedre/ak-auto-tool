import Link from 'next/link';

export default function ServicesSection() {
  const services = [
    {
      icon: '🔁',
      title: 'Workflow Automation',
      description: 'Automate repetitive business tasks across teams and tools.',
      features: ['CRM updates', 'Email triage', 'Document processing', 'Task assignments']
    },
    {
      icon: '🤖',
      title: 'AI Agents-as-a-Service',
      description: 'Digital workers trained to handle support, HR, finance, and more.',
      features: ['HR Assistant', 'Finance Bot', 'Support Agent', 'Custom Agents']
    },
    {
      icon: '🛠️',
      title: 'Custom AI Integration',
      description: 'Seamless integration of AI into your existing systems.',
      features: ['LLM-driven tools', 'RAG applications', 'Smart APIs', 'Custom solutions']
    }
  ];

  return (
    <section className="py-16 lg:py-24 bg-background-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-text-dark mb-4">
            Services Snapshot
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Comprehensive AI automation solutions tailored to your business needs
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {services.map((service, index) => (
            <div key={index} className="card card--light">
              <div className="text-4xl mb-4">{service.icon}</div>
              <h3 className="text-xl font-semibold text-text-dark mb-3">
                {service.title}
              </h3>
              <p className="text-gray-600 mb-6">
                {service.description}
              </p>
              <ul className="space-y-2">
                {service.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center text-sm text-gray-700">
                    <svg className="w-4 h-4 text-accent mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Why Ace Tech Section */}
        <div className="card card--light bg-accent/5 border border-accent/20">
          <h3 className="text-2xl md:text-3xl font-bold text-text-dark mb-8 text-center">
            Why Ace Tech?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex flex-col items-center">
              <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary-dark" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <h4 className="text-lg font-semibold text-text-dark mb-2">100% Client-focused solutions</h4>
              <p className="text-gray-600 text-center">Your goals guide everything we build</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary-dark" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <h4 className="text-lg font-semibold text-text-dark mb-2">Built for speed and scale</h4>
              <p className="text-gray-600 text-center">Fast implementation, scalable solutions</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary-dark" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <h4 className="text-lg font-semibold text-text-dark mb-2">Based in Bangalore, serving global clients</h4>
              <p className="text-gray-600 text-center">Local expertise, global reach</p>
            </div>
          </div>
        </div>

        {/* Case Study */}
        <div className="text-center mt-16">
          <div className="bg-primary-dark text-text-primary rounded-lg p-8 md:p-12 card">
            <blockquote className="text-xl md:text-2xl font-medium mb-4">
              "Cut processing time by 85% for a logistics firm in under 3 weeks."
            </blockquote>
            <p className="text-primary-light">Real results, delivered fast</p>
          </div>
        </div>

        {/* Final CTA */}
        <div className="text-center mt-16">
          <h3 className="text-2xl md:text-3xl font-bold text-text-dark mb-4">
            Let's build your AI edge.
          </h3>
          <Link 
            href="/contact" 
            className="btn btn--primary text-lg px-8 py-4"
          >
            Book a Free Consultation
          </Link>
        </div>
      </div>
    </section>
  );
}