import { motion } from 'framer-motion';

const Footer = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  const footerSections = [
    {
      title: 'Product',
      links: [
        { label: 'Features', action: () => scrollToSection('features') },
        { label: 'Chat Interface', action: () => window.location.href = '/main' },
        { label: 'Dashboard', action: () => window.location.href = '/about' },
      ],
    },
    {
      title: 'Use Cases',
      links: [
        { label: 'Medical Research', action: () => scrollToSection('use-cases') },
        { label: 'Clinical Support', action: () => scrollToSection('use-cases') },
        { label: 'Patient Education', action: () => scrollToSection('use-cases') },
      ],
    },
    {
      title: 'Resources',
      links: [
        { label: 'Documentation', action: () => scrollToSection('resources') },
        { label: 'API Reference', action: () => scrollToSection('resources') },
        { label: 'Support', action: () => scrollToSection('resources') },
      ],
    },
  ];

  return (
    <footer className="bg-gradient-to-b from-bg to-shade-2 border-t border-border py-12 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Section */}
          <div className="col-span-1">
            <h3 className="text-2xl font-bold bg-gradient-to-b from-shade-3 to-shade-4 bg-clip-text text-transparent mb-2">
              Medical RAG
            </h3>
            <p className="text-sm text-muted-foreground">
              AI-powered medical insights you can trust.
            </p>
          </div>

          {/* Links Sections */}
          {footerSections.map((section, index) => (
            <div key={index}>
              <h4 className="text-sm font-semibold text-foreground mb-4">{section.title}</h4>
              <ul className="space-y-2">
                {section.links.map((link, linkIndex) => (
                  <li key={linkIndex}>
                    <button
                      onClick={link.action}
                      className="text-sm text-primary-text hover:text-primary transition-colors duration-200"
                    >
                      {link.label}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Section */}
        <div className="pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>© 2025 Medical RAG</span>
            <span className="text-primary">•</span>
            <span>All rights reserved</span>
          </div>
          <div className="flex gap-4">
            <a href="#" className="text-sm text-primary-text hover:text-primary transition-colors duration-200">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-primary-text hover:text-primary transition-colors duration-200">
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
