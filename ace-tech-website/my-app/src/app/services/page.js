export const metadata = {
  title: "AI Automation Services - Ace Tech Solutions",
  description: "Comprehensive AI automation services including workflow automation, AI agents-as-a-service, and custom AI integrations tailored to your business needs.",
  openGraph: {
    title: "AI Automation Services - Ace Tech Solutions",
    description: "Smart automation solutions tailored to your business needs. Workflow automation, AI agents, and custom integrations.",
  },
};

export default function Services() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Smart Automation.
              <span className="text-blue-600 block">Tailored to Your Business.</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto">
              Comprehensive AI automation solutions designed to eliminate repetitive tasks and scale your operations efficiently.
            </p>
          </div>
        </div>
      </section>

      {/* Services Details */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Workflow Automation */}
          <div className="mb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <div className="text-6xl mb-6">🔁</div>
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                  Workflow Automation
                </h2>
                <p className="text-xl text-gray-600 mb-8">
                  Automate recurring business processes — from onboarding to invoice handling. Transform manual, time-consuming tasks into streamlined, automated workflows.
                </p>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Use Cases:</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-blue-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">CRM updates</span>
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-blue-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Email triage</span>
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-blue-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Document processing</span>
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-blue-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Task assignments</span>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 rounded-xl p-8">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Benefits</h4>
                <ul className="space-y-3">
                  <li className="text-gray-700">• Reduce manual errors by up to 95%</li>
                  <li className="text-gray-700">• Save 10-20 hours per week per team member</li>
                  <li className="text-gray-700">• Ensure consistent process execution</li>
                  <li className="text-gray-700">• Free up team for strategic work</li>
                </ul>
              </div>
            </div>
          </div>

          {/* AI Agents */}
          <div className="mb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div className="order-2 lg:order-1 bg-gray-50 rounded-xl p-8">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Example Agents</h4>
                <div className="space-y-4">
                  <div className="border-l-4 border-blue-600 pl-4">
                    <h5 className="font-semibold text-gray-900">HR Assistant</h5>
                    <p className="text-gray-600 text-sm">Scheduling, document collection, onboarding workflows</p>
                  </div>
                  <div className="border-l-4 border-blue-600 pl-4">
                    <h5 className="font-semibold text-gray-900">Finance Bot</h5>
                    <p className="text-gray-600 text-sm">Report generation, data entry, expense processing</p>
                  </div>
                  <div className="border-l-4 border-blue-600 pl-4">
                    <h5 className="font-semibold text-gray-900">Support Agent</h5>
                    <p className="text-gray-600 text-sm">Auto-reply, ticket categorization, knowledge base queries</p>
                  </div>
                </div>
              </div>
              <div className="order-1 lg:order-2">
                <div className="text-6xl mb-6">🤖</div>
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                  AI Agents-as-a-Service
                </h2>
                <p className="text-xl text-gray-600 mb-8">
                  Custom AI agents that function like digital employees — answering questions, handling requests, and integrating across your tools with human-like intelligence.
                </p>
                <p className="text-gray-700 mb-6">
                  Our AI agents learn your business processes, understand context, and can handle complex multi-step tasks while maintaining consistency and accuracy.
                </p>
                <div className="bg-blue-50 rounded-lg p-6">
                  <h4 className="font-semibold text-blue-900 mb-2">🎯 Available 24/7</h4>
                  <p className="text-blue-800 text-sm">Never miss a customer query or internal request</p>
                </div>
              </div>
            </div>
          </div>

          {/* Custom AI Solutions */}
          <div className="mb-20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                <div className="text-6xl mb-6">🛠️</div>
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                  Custom AI Solutions
                </h2>
                <p className="text-xl text-gray-600 mb-8">
                  We integrate AI into your existing workflows and tools — building LLM-driven applications, RAG systems, and smart APIs customized to your exact needs.
                </p>
                
                <div className="bg-gray-900 text-white rounded-lg p-6 mb-6">
                  <h4 className="font-semibold mb-3">💻 Tech Stack</h4>
                  <div className="flex flex-wrap gap-2">
                    <span className="bg-blue-600 px-3 py-1 rounded text-sm">OpenAI</span>
                    <span className="bg-blue-600 px-3 py-1 rounded text-sm">LangChain</span>
                    <span className="bg-blue-600 px-3 py-1 rounded text-sm">Pinecone</span>
                    <span className="bg-blue-600 px-3 py-1 rounded text-sm">NestJS</span>
                    <span className="bg-blue-600 px-3 py-1 rounded text-sm">FastAPI</span>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-8">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Custom Solutions Include:</h4>
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-blue-600 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">LLM-driven tools for content generation and analysis</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-blue-600 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">RAG applications for intelligent document search</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-blue-600 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Smart APIs that adapt to your business logic</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-blue-600 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Integration with existing systems and databases</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Engagement Options */}
          <div className="bg-gray-50 rounded-2xl p-8 md:p-12 mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8 text-center">
              Engagement Options
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">One-time Implementation</h3>
                <p className="text-gray-600">Fixed-scope projects with clear deliverables and timelines. Perfect for specific automation needs.</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Retainer-based Optimization</h3>
                <p className="text-gray-600">Ongoing partnership for continuous improvement and scaling of your automation systems.</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">API/SDK Access</h3>
                <p className="text-gray-600">
                  <span className="text-blue-600 font-semibold">(Coming Soon)</span><br />
                  Direct access to our AI automation platform through APIs and SDKs.
                </p>
              </div>
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl p-8 md:p-12">
            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Let's automate your hardest workflows.
            </h3>
            <p className="text-blue-100 mb-8 text-lg">
              Ready to see how AI automation can transform your business operations?
            </p>
            <a 
              href="/contact" 
              className="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl"
            >
              Request a Free Assessment
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}