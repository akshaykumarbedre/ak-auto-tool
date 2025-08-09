import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-primary-dark shadow-sm border-b border-primary-light/20">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="text-2xl font-bold text-accent">
              Ace Tech Solutions
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <Link 
                href="/" 
                className="text-primary-light hover:text-accent px-3 py-2 text-sm font-medium transition-all duration-300"
              >
                Home
              </Link>
              <Link 
                href="/about" 
                className="text-primary-light hover:text-accent px-3 py-2 text-sm font-medium transition-all duration-300"
              >
                About
              </Link>
              <Link 
                href="/services" 
                className="text-primary-light hover:text-accent px-3 py-2 text-sm font-medium transition-all duration-300"
              >
                Services
              </Link>
              <Link 
                href="/contact" 
                className="text-primary-light hover:text-accent px-3 py-2 text-sm font-medium transition-all duration-300"
              >
                Contact
              </Link>
            </div>
          </div>

          {/* CTA Button */}
          <div className="hidden md:block">
            <Link 
              href="/contact" 
              className="btn btn--primary"
            >
              Get a Free Demo
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              type="button"
              className="bg-primary-dark inline-flex items-center justify-center p-2 rounded-md text-primary-light hover:text-accent hover:bg-primary-light/10 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-accent transition-all duration-300"
              aria-controls="mobile-menu"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {/* Menu icon */}
              <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu - hidden by default */}
        <div className="md:hidden" id="mobile-menu">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link 
              href="/" 
              className="text-primary-light hover:text-accent block px-3 py-2 text-base font-medium transition-all duration-300"
            >
              Home
            </Link>
            <Link 
              href="/about" 
              className="text-primary-light hover:text-accent block px-3 py-2 text-base font-medium transition-all duration-300"
            >
              About
            </Link>
            <Link 
              href="/services" 
              className="text-primary-light hover:text-accent block px-3 py-2 text-base font-medium transition-all duration-300"
            >
              Services
            </Link>
            <Link 
              href="/contact" 
              className="text-primary-light hover:text-accent block px-3 py-2 text-base font-medium transition-all duration-300"
            >
              Contact
            </Link>
            <Link 
              href="/contact" 
              className="btn btn--primary mt-4"
            >
              Get a Free Demo
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}