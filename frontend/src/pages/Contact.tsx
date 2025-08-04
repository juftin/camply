import * as React from "react";
import { Link } from "react-router-dom";
import {
  Mail,
  MessageSquare,
  MessageCircleHeart,
  Github,
  Bug,
  Lightbulb,
  Send,
  HelpCircle,
  Server,
  Heart,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function Contact() {
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Add form submission logic
    console.log("Contact form submitted:", formData);
  };

  return (
    <div className="container mx-auto py-12 px-4 max-w-6xl">
      <div className="text-center mb-12">
        <div className="mb-6">
          <MessageCircleHeart className="h-16 w-16 text-primary mx-auto mb-4" />
        </div>
        <h1 className="text-4xl font-bold mb-4">Get in Touch</h1>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          Have questions about camply? Found a bug? Want to suggest a feature?
          As an open-source project, we'd love to hear from the community.
        </p>
      </div>

      {/* Contact Form */}
      <section className="mb-16">
        <Card className="max-w-2xl mx-auto">
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2 text-2xl">
              <MessageSquare className="h-6 w-6" />
              Send us a Message
            </CardTitle>
            <CardDescription>
              Fill out the form below and we'll get back to you as soon as
              possible.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label htmlFor="name" className="text-sm font-medium">
                    Full Name
                  </label>
                  <Input
                    id="name"
                    name="name"
                    type="text"
                    placeholder="Your full name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="email" className="text-sm font-medium">
                    Email Address
                  </label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="your.email@example.com"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label htmlFor="subject" className="text-sm font-medium">
                  Subject
                </label>
                <Input
                  id="subject"
                  name="subject"
                  type="text"
                  placeholder="What's this about?"
                  value={formData.subject}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="message" className="text-sm font-medium">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows={6}
                  placeholder="Tell us how we can help..."
                  value={formData.message}
                  onChange={handleInputChange}
                  className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none"
                  required
                />
              </div>

              <Button type="submit" className="w-full" size="lg">
                <Send className="h-4 w-4 mr-2" />
                Send Message
              </Button>
            </form>
          </CardContent>
        </Card>
      </section>

      {/* Contact Methods */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Ways to Reach Us
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* GitHub Issues */}
          <Card>
            <CardHeader className="text-center">
              <Github className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">GitHub Issues</CardTitle>
              <CardDescription>
                For bug reports and feature requests
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <a
                  href="https://github.com/juftin/camply/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Open an Issue
                </a>
              </Button>
            </CardContent>
          </Card>

          {/* Email */}
          <Card>
            <CardHeader className="text-center">
              <Mail className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">Email</CardTitle>
              <CardDescription>
                For general questions and support
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <a href="mailto:camply@juftin.com">Send Email</a>
              </Button>
            </CardContent>
          </Card>

          {/* Report Bug */}
          <Card>
            <CardHeader className="text-center">
              <Bug className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">Report Bug</CardTitle>
              <CardDescription>
                Help us improve by reporting issues
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <a
                  href="https://github.com/juftin/camply/issues/new?template=bug_report.md"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Report Bug
                </a>
              </Button>
            </CardContent>
          </Card>

          {/* Feature Request */}
          <Card>
            <CardHeader className="text-center">
              <Lightbulb className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">Feature Request</CardTitle>
              <CardDescription>
                Have an idea to make camply better?
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <a
                  href="https://github.com/juftin/camply/issues/new?template=feature_request.md"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Suggest Feature
                </a>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Quick Links */}
      <section>
        <h2 className="text-3xl font-bold text-center mb-8">Quick Links</h2>
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Card>
            <CardHeader className="text-center">
              <HelpCircle className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">FAQ</CardTitle>
              <CardDescription>
                Find answers to common questions
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <Link to="/faq">View FAQ</Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Server className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">Providers</CardTitle>
              <CardDescription>See all supported campgrounds</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <Link to="/providers">View Providers</Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Heart className="h-12 w-12 text-primary mx-auto mb-4" />
              <CardTitle className="text-lg">Contribute</CardTitle>
              <CardDescription>Support the camply project</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <Button variant="outline" className="w-full" asChild>
                <Link to="/contribute">Contribute</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}
