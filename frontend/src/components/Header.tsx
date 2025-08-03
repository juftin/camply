import * as React from "react";
import { Menu, X, TentTree } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";

interface HeaderProps {
  showLogo?: boolean;
}

export function Header({ showLogo = true }: HeaderProps) {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);
  const [isHeaderVisible, setIsHeaderVisible] = React.useState(true);
  const [lastScrollY, setLastScrollY] = React.useState(0);

  React.useEffect(() => {
    if (location.hash) {
      const element = document.getElementById(location.hash.substring(1));
      if (element) {
        setTimeout(() => {
          element.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
    } else {
      // Scroll to top when navigating to new pages (no hash)
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [location]);

  React.useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;

      // Only apply auto-hide behavior on mobile
      if (window.innerWidth < 768) {
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
          // Scrolling down and past threshold - hide header
          setIsHeaderVisible(false);
        } else if (currentScrollY < lastScrollY) {
          // Scrolling up - show header
          setIsHeaderVisible(true);
        }
      } else {
        // Always show header on desktop
        setIsHeaderVisible(true);
      }

      setLastScrollY(currentScrollY);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [lastScrollY]);

  return (
    <>
      {/* Header */}
      <header
        className={`sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 transition-transform duration-300 ${isHeaderVisible ? "translate-y-0" : "-translate-y-full"}`}
      >
        <div
          className={`container mx-auto px-4 py-4 flex items-center ${showLogo ? "justify-between" : "justify-center relative"}`}
        >
          <div className="flex items-center space-x-2 h-8">
            {showLogo && (
              <Link to="/" className="flex items-center space-x-2">
                <TentTree className="h-8 w-8 text-primary" />
                <span className="text-2xl font-bold">camply</span>
              </Link>
            )}
          </div>
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
            className={`md:hidden p-2 ${!showLogo ? "absolute right-4" : ""}`}
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>
          <div
            className={`hidden md:flex items-center space-x-2 ${!showLogo ? "absolute right-4" : ""}`}
          >
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
    </>
  );
}
