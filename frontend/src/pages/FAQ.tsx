import * as React from "react";
import { ChevronDown, ChevronUp, HelpCircle, CircleHelp } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

interface FAQItem {
  id: string;
  question: string;
  answer: string | React.ReactNode;
}

const faqs: FAQItem[] = [
  {
    id: "how-it-works",
    question: "How does camply work?",
    answer:
      "We monitor campsite availability across multiple booking platforms and send you instant notifications when your desired campsites become available. You can set up alerts for specific campgrounds, dates, and site types.",
  },
  {
    id: "is-free",
    question: "Is camply free to use?",
    answer:
      "Yes! camply is completely free and open-source. We operate as a not-for-profit service supported by community contributions. There are no hidden fees or premium subscriptions.",
  },
  {
    id: "make-reservations",
    question: "Do you make reservations for me?",
    answer:
      "No, we don't make reservations. We notify you when campsites become available, and you make the reservation directly through the official booking platform. This ensures you have full control over your bookings.",
  },
  {
    id: "which-campgrounds",
    question: "Which campgrounds do you monitor?",
    answer: (
      <>
        We monitor thousands of campgrounds across national parks, state parks,
        and other recreation areas. Check our{" "}
        <Link
          to="/providers"
          className="text-primary hover:text-primary/80 underline"
        >
          Providers page
        </Link>{" "}
        for a complete list of supported booking platforms and campgrounds.
      </>
    ),
  },
  {
    id: "how-to-contribute",
    question: "How can I contribute to camply?",
    answer: (
      <>
        You can contribute by reporting bugs, suggesting features, submitting
        code, spreading the word, or making financial contributions. Visit our{" "}
        <Link
          to="/contribute"
          className="text-primary hover:text-primary/80 underline"
        >
          Contribute page
        </Link>{" "}
        or{" "}
        <a
          href="https://github.com/juftin/camply"
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:text-primary/80 underline"
        >
          GitHub repository
        </a>{" "}
        to get started.
      </>
    ),
  },
  {
    id: "notification-types",
    question: "What types of notifications do you send?",
    answer:
      "We send email notifications when campsites matching your criteria become available. Notifications include campground details, available dates, site types, and direct links to make reservations.",
  },
  {
    id: "how-often-check",
    question: "How often do you check for availability?",
    answer:
      "We check for campsite availability multiple times per day, with more frequent checks for popular campgrounds during peak seasons. The exact frequency depends on the booking platform and demand.",
  },
  {
    id: "account-required",
    question: "Do I need to create an account?",
    answer:
      "Yes, you'll need to create a free account to set up campsite alerts and receive notifications. This allows us to save your preferences and send personalized availability updates.",
  },
  {
    id: "data-privacy",
    question: "How do you handle my personal data?",
    answer: (
      <>
        We take privacy seriously. We only collect the minimum data necessary to
        provide our service, never sell your information, and operate
        transparently as an open-source project. Check our{" "}
        <Link
          to="/privacy"
          className="text-primary hover:text-primary/80 underline"
        >
          Privacy Policy
        </Link>{" "}
        for full details.
      </>
    ),
  },
  {
    id: "supported-platforms",
    question: "Which booking platforms do you support?",
    answer: (
      <>
        We support major platforms including Recreation.gov, Reserve California,
        various state park systems, and many others. Our{" "}
        <Link
          to="/providers"
          className="text-primary hover:text-primary/80 underline"
        >
          Providers page
        </Link>{" "}
        has the complete list of supported booking platforms.
      </>
    ),
  },
  {
    id: "false-positives",
    question: "What if I get notified but the site isn't actually available?",
    answer:
      "While we strive for accuracy, booking platforms can have delays or errors. We recommend booking quickly when notified, as popular sites get reserved very fast. If you consistently see issues with a specific campground, please report it on GitHub.",
  },
  {
    id: "open-source",
    question: "What does it mean that camply is open-source?",
    answer:
      "Open-source means our code is publicly available on GitHub for anyone to view, contribute to, or learn from. This ensures transparency, allows community contributions, and means the project isn't controlled by a single company.",
  },
];

export function FAQ() {
  const [openItems, setOpenItems] = React.useState<Set<string>>(new Set());

  const toggleItem = (id: string) => {
    const newOpenItems = new Set(openItems);
    if (newOpenItems.has(id)) {
      newOpenItems.delete(id);
    } else {
      newOpenItems.add(id);
    }
    setOpenItems(newOpenItems);
  };

  const toggleAll = () => {
    if (openItems.size === faqs.length) {
      setOpenItems(new Set());
    } else {
      setOpenItems(new Set(faqs.map((faq) => faq.id)));
    }
  };

  return (
    <div className="container mx-auto py-12 px-4 max-w-4xl">
      <div className="text-center mb-12">
        <div className="mb-6">
          <CircleHelp className="h-16 w-16 text-primary mx-auto mb-4" />
        </div>
        <h1 className="text-4xl font-bold mb-4">Frequently Asked Questions</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Find answers to common questions about camply, our campsite monitoring
          service, and how we help you never miss your perfect campsite.
        </p>
      </div>

      <div className="mb-8 flex justify-center">
        <Button variant="outline" onClick={toggleAll} className="gap-2">
          <HelpCircle className="h-4 w-4" />
          {openItems.size === faqs.length ? "Collapse All" : "Expand All"}
        </Button>
      </div>

      <div className="space-y-4">
        {faqs.map((faq) => {
          const isOpen = openItems.has(faq.id);
          return (
            <Card key={faq.id} className="transition-all duration-200">
              <CardHeader
                className="cursor-pointer hover:bg-muted/50 transition-colors"
                onClick={() => toggleItem(faq.id)}
              >
                <CardTitle className="flex items-center justify-between text-left">
                  <span className="text-lg font-medium">{faq.question}</span>
                  {isOpen ? (
                    <ChevronUp className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                  ) : (
                    <ChevronDown className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                  )}
                </CardTitle>
              </CardHeader>
              {isOpen && (
                <CardContent className="pt-0">
                  <div className="text-muted-foreground leading-relaxed">
                    {faq.answer}
                  </div>
                </CardContent>
              )}
            </Card>
          );
        })}
      </div>

      {/* Still have questions section */}
      <section className="mt-16">
        <Card className="bg-primary/5 border-primary/20">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Still have questions?</CardTitle>
            <CardDescription>
              Can't find what you're looking for? We're here to help!
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <p className="text-muted-foreground">
              Check out our GitHub repository for technical questions, or reach
              out through our contact page for general support.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="outline" asChild>
                <a
                  href="https://github.com/juftin/camply/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View GitHub Issues
                </a>
              </Button>
              <Button asChild>
                <Link to="/contact">Contact Us</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
