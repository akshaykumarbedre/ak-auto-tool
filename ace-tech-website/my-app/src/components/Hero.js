import Link from 'next/link';

export default function Hero() {
  return (
    <section className="bg-primary-dark py-16 lg:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-text-primary mb-6">
            Automate the Busywork.
            <span className="text-accent block">Scale What Matters.</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-primary-light mb-8 max-w-4xl mx-auto">
            AI automation built for growth. Ace Tech Solutions helps businesses eliminate repetitive tasks and streamline operations — fast, affordable, and custom to your needs.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Link 
              href="/contact" 
              className="btn btn--primary text-lg px-8 py-4"
            >
              Get a Free Demo
            </Link>
            <Link 
              href="/contact" 
              className="btn btn--secondary text-lg px-8 py-4"
            >
              Talk to an Expert
            </Link>
          </div>

          <div className="text-center text-primary-light">
            <p className="text-lg font-medium mb-4">
              We believe that intelligent automation should be accessible to every business — not just the big players.
            </p>
            <p className="text-base">
              That's why we provide tailored AI solutions that deliver real impact without draining your budget.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}