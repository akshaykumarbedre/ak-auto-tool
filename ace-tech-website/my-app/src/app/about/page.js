export const metadata = {
  title: "About Us - Ace Tech Solutions",
  description: "Learn about Ace Tech Solutions, a Bangalore-based AI automation company helping businesses modernize operations through intelligent automation.",
  openGraph: {
    title: "About Us - Ace Tech Solutions",
    description: "Learn about our mission, values, and team at Ace Tech Solutions.",
  },
};

export default function About() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Who We Are
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto">
              Ace Tech Solutions is a Bangalore-based AI automation company helping businesses modernize their operations through intelligent automation.
            </p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16 lg:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Company Description */}
          <div className="prose prose-lg mx-auto mb-16">
            <p className="text-xl text-gray-600 leading-relaxed">
              We're a lean team of engineers, product thinkers, and problem solvers — passionate about delivering results, not complexity. Our focus is on creating practical AI solutions that make a real difference in how businesses operate.
            </p>
          </div>

          {/* Values Section */}
          <div className="mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">
              Our Values
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Client First</h3>
                <p className="text-gray-600">Your goals guide everything we build. We listen, understand, and deliver solutions that truly address your needs.</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Practical AI</h3>
                <p className="text-gray-600">No hype. Just real solutions. We focus on AI that works, not AI that just sounds impressive.</p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Affordable Impact</h3>
                <p className="text-gray-600">Enterprise-grade results, startup-friendly pricing. Quality AI automation shouldn't break the bank.</p>
              </div>
            </div>
          </div>

          {/* Story Section */}
          <div className="mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8 text-center">
              Our Story
            </h2>
            <div className="bg-gray-50 rounded-2xl p-8 md:p-12">
              <p className="text-lg text-gray-700 leading-relaxed mb-6">
                Founded in Bangalore by a team with deep startup and enterprise experience, Ace Tech Solutions began with a simple mission: bring the power of automation to businesses that need it most — without the expensive overhead or bloated platforms.
              </p>
              <p className="text-lg text-gray-700 leading-relaxed">
                We saw too many companies struggling with repetitive tasks that could be automated, but lacking access to affordable, practical AI solutions. That's when we decided to bridge that gap with our client-focused approach to AI automation.
              </p>
            </div>
          </div>

          {/* Team Section */}
          <div className="mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12 text-center">
              Meet the Team
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-white">R</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Rohan</h3>
                <p className="text-blue-600 font-medium mb-3">Founder & AI Engineer</p>
                <p className="text-gray-600">Leading AI development and strategic vision for automation solutions.</p>
              </div>
              
              <div className="text-center">
                <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-white">P</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Priya</h3>
                <p className="text-blue-600 font-medium mb-3">Product & Customer Success</p>
                <p className="text-gray-600">Ensuring our solutions perfectly align with client needs and goals.</p>
              </div>
              
              <div className="text-center">
                <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-white">A</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Ankit</h3>
                <p className="text-blue-600 font-medium mb-3">Automation Architect</p>
                <p className="text-gray-600">Designing and implementing scalable automation workflows.</p>
              </div>
            </div>
          </div>

          {/* CTA Section */}
          <div className="text-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl p-8 md:p-12">
            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Want to work with us or learn more?
            </h3>
            <p className="text-blue-100 mb-8 text-lg">
              We'd love to hear about your automation challenges and goals.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a 
                href="/contact" 
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Contact Us
              </a>
              <a 
                href="/contact" 
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                Careers
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}