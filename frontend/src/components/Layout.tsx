import * as React from "react";
import { Tent, Github, Menu, X } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";

interface LayoutProps {
  children: React.ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  React.useEffect(() => {
    if (location.hash) {
      const element = document.getElementById(location.hash.substring(1));
      if (element) {
        setTimeout(() => {
          element.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
    }
  }, [location]);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <Tent className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold">camply</span>
          </Link>
          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-6">
            <Link
              to="/"
              className={`text-muted-foreground hover:text-foreground ${
                location.pathname === "/" ? "text-foreground" : ""
              }`}
            >
              Home
            </Link>
            <Link
              to="/providers"
              className={`text-muted-foreground hover:text-foreground ${
                location.pathname === "/providers" ? "text-foreground" : ""
              }`}
            >
              Providers
            </Link>
            <Link
              to="/#features"
              className="text-muted-foreground hover:text-foreground"
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  document
                    .getElementById("features")
                    ?.scrollIntoView({ behavior: "smooth" });
                }
              }}
            >
              Features
            </Link>
            <Link
              to="/#how-it-works"
              className="text-muted-foreground hover:text-foreground"
              onClick={(e) => {
                if (location.pathname === "/") {
                  e.preventDefault();
                  document
                    .getElementById("how-it-works")
                    ?.scrollIntoView({ behavior: "smooth" });
                }
              }}
            >
              How it works
            </Link>
            <Link
              to="/contribute"
              className={`text-muted-foreground hover:text-foreground ${
                location.pathname === "/contribute" ? "text-foreground" : ""
              }`}
            >
              Contribute
            </Link>
          </nav>

          {/* Mobile Navigation Toggle */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>
          <div className="hidden md:flex items-center space-x-2">
            <ThemeToggle />
            <Button variant="outline" asChild>
              <Link to="/auth">Sign In</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden sticky top-[73px] z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <nav className="container mx-auto px-4 py-4 space-y-4">
            <Link
              to="/"
              className={`block text-muted-foreground hover:text-foreground ${
                location.pathname === "/" ? "text-foreground" : ""
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/providers"
              className={`block text-muted-foreground hover:text-foreground ${
                location.pathname === "/providers" ? "text-foreground" : ""
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Providers
            </Link>
            <Link
              to="/#features"
              className="block text-muted-foreground hover:text-foreground"
              onClick={(e) => {
                setIsMobileMenuOpen(false);
                if (location.pathname === "/") {
                  e.preventDefault();
                  document
                    .getElementById("features")
                    ?.scrollIntoView({ behavior: "smooth" });
                }
              }}
            >
              Features
            </Link>
            <Link
              to="/#how-it-works"
              className="block text-muted-foreground hover:text-foreground"
              onClick={(e) => {
                setIsMobileMenuOpen(false);
                if (location.pathname === "/") {
                  e.preventDefault();
                  document
                    .getElementById("how-it-works")
                    ?.scrollIntoView({ behavior: "smooth" });
                }
              }}
            >
              How it works
            </Link>
            <Link
              to="/contribute"
              className={`block text-muted-foreground hover:text-foreground ${
                location.pathname === "/contribute" ? "text-foreground" : ""
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Contribute
            </Link>
            <div className="pt-4 border-t flex items-center justify-between">
              <ThemeToggle />
              <Button variant="outline" asChild>
                <Link to="/auth" onClick={() => setIsMobileMenuOpen(false)}>
                  Sign In
                </Link>
              </Button>
            </div>
          </nav>
        </div>
      )}

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="py-12 px-4 border-t">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Tent className="h-6 w-6 text-primary" />
              <span className="text-lg font-semibold">camply</span>
            </div>
            <div className="flex flex-wrap items-center justify-center md:justify-start gap-6 text-sm text-muted-foreground">
              <Link to="/faq" className="hover:text-foreground">
                FAQ
              </Link>
              <Link to="/privacy" className="hover:text-foreground">
                Privacy Policy
              </Link>
              <Link to="/terms" className="hover:text-foreground">
                Terms of Service
              </Link>
              <Link to="/contact" className="hover:text-foreground">
                Contact
              </Link>
              <a
                href="https://github.com/juftin/camply-web"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 hover:text-foreground"
              >
                <Github className="h-4 w-4" />
                Built in Public
              </a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
            © 2025 camply. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
