import ContactForm from '../../components/ContactForm';

export const metadata = {
  title: "Contact Us - Ace Tech Solutions",
  description: "Get in touch with Ace Tech Solutions for AI automation consulting. Let's discuss how we can automate your business processes and scale your operations.",
  openGraph: {
    title: "Contact Us - Ace Tech Solutions",
    description: "Ready to automate your business? Contact our AI automation experts in Bangalore.",
  },
};

export default function Contact() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Let's Talk AI — Without the Buzzwords
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto">
              Whether you need a quick automation, a full AI roadmap, or just a consultation, we're here to help.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Content */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
            
            {/* Contact Form */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">
                Send us a message
              </h2>
              <ContactForm />
            </div>

            {/* Contact Information */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">
                Get in touch
              </h2>
              
              <div className="space-y-8">
                {/* Office Location */}
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Office</h3>
                    <p className="text-gray-600">Bangalore, India</p>
                    <p className="text-gray-500 text-sm mt-1">Serving clients globally</p>
                  </div>
                </div>

                {/* Email */}
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Email</h3>
                    <a href="mailto:contact@acetechsolutions.in" className="text-blue-600 hover:text-blue-700 transition-colors">
                      contact@acetechsolutions.in
                    </a>
                    <p className="text-gray-500 text-sm mt-1">We respond within 24 hours</p>
                  </div>
                </div>

                {/* Response Time */}
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Response Time</h3>
                    <p className="text-gray-600">Within 24 hours</p>
                    <p className="text-gray-500 text-sm mt-1">Usually much faster during business hours</p>
                  </div>
                </div>

                {/* Social Links */}
                <div className="pt-8 border-t border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Connect with us</h3>
                  <div className="flex space-x-4">
                    <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors">
                      <span className="sr-only">LinkedIn</span>
                      <svg className="h-8 w-8" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                      </svg>
                    </a>
                    <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors">
                      <span className="sr-only">Twitter</span>
                      <svg className="h-8 w-8" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mt-20">
            <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">
              Frequently Asked Questions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">How quickly can you implement automation?</h3>
                <p className="text-gray-600">Most workflow automations can be implemented within 2-4 weeks. Complex AI agents may take 4-8 weeks depending on requirements.</p>
              </div>
              
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Do you work with small businesses?</h3>
                <p className="text-gray-600">Absolutely! We specialize in making enterprise-grade AI automation accessible to businesses of all sizes with startup-friendly pricing.</p>
              </div>
              
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">What if our current systems are complex?</h3>
                <p className="text-gray-600">We excel at integrating with existing systems. Our team has experience with legacy systems, modern APIs, and everything in between.</p>
              </div>
              
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Do you provide ongoing support?</h3>
                <p className="text-gray-600">Yes! We offer both one-time implementations and ongoing retainer relationships for continuous optimization and support.</p>
              </div>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className="text-center mt-20 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl p-8 md:p-12">
            <h3 className="text-2xl md:text-3xl font-bold mb-4">
              Ready to get started?
            </h3>
            <p className="text-blue-100 mb-8 text-lg">
              Book a free 30-minute consultation to discuss your automation needs.
            </p>
            <a 
              href="mailto:contact@acetechsolutions.in?subject=Free Consultation Request" 
              className="inline-block bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl"
            >
              Book Free Consultation
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}