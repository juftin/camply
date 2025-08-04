import { Link } from "react-router-dom";

export function TermsOfService() {
  return (
    <div className="container mx-auto py-12 px-4 max-w-4xl">
      <h1 className="text-4xl font-bold mb-8">Terms of Service</h1>
      <div className="prose prose-lg max-w-none">
        <p className="text-muted-foreground mb-8">
          <strong>Last updated:</strong> August 2025
        </p>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Acceptance of Terms</h2>
          <p className="mb-4">
            By accessing and using camply's services, you accept and agree to be
            bound by the terms and provision of this agreement. If you do not
            agree to abide by the above, please do not use this service.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">
            Description of Service
          </h2>
          <p className="mb-4">
            camply is a campsite availability monitoring service that helps
            users find available campsites at popular campgrounds. We monitor
            various booking platforms and send notifications when campsites
            become available based on your preferences.
          </p>
          <p className="mb-4 p-4 bg-primary/10 border border-primary/20 rounded-lg">
            <strong>Not-for-Profit Service:</strong> camply is operated as a
            not-for-profit service with a mission to help outdoor enthusiasts
            access nature. We are committed to ethical practices and will never
            monetize your personal data.
          </p>
          <p className="mb-4">
            <strong>Important:</strong> camply is an independent service and is
            not affiliated with any campground booking platforms, national
            parks, or government agencies.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">User Account</h2>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>
              You must provide accurate and complete registration information
            </li>
            <li>
              You are responsible for maintaining the security of your account
            </li>
            <li>
              You must notify us immediately of any unauthorized use of your
              account
            </li>
            <li>One account per user; multiple accounts are not permitted</li>
            <li>You must be at least 13 years old to create an account</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Acceptable Use</h2>
          <p className="mb-4">You agree not to:</p>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>Use the service for any unlawful purpose or activity</li>
            <li>Attempt to gain unauthorized access to our systems</li>
            <li>Interfere with or disrupt the service or servers</li>
            <li>
              Create excessive load on our systems through automated means
            </li>
            <li>
              Reverse engineer, decompile, or disassemble our software for
              commercial purposes or profit
            </li>
            <li>Use the service to compete with or replicate our business</li>
            <li>Share your account credentials with others</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Service Availability</h2>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>
              We strive to provide continuous service but cannot guarantee 100%
              uptime
            </li>
            <li>
              We may temporarily suspend service for maintenance or updates
            </li>
            <li>
              Third-party booking platforms may change their systems, affecting
              our monitoring
            </li>
            <li>
              Notification delivery depends on external services (email, SMS
              providers)
            </li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Disclaimers</h2>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>
              camply does not guarantee campsite availability or successful
              reservations
            </li>
            <li>
              We are not responsible for booking platform errors or changes
            </li>
            <li>Campsite information is provided "as is" without warranties</li>
            <li>
              You are responsible for verifying all campsite details before
              booking
            </li>
            <li>We do not handle actual campsite reservations or payments</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">
            Limitation of Liability
          </h2>
          <p className="mb-4">
            In no event shall camply be liable for any indirect, incidental,
            special, consequential, or punitive damages, including lost profits,
            lost revenue, or lost data, arising from your use of the service.
          </p>
          <p className="mb-4">
            As a not-for-profit service, our liability is limited to the extent
            permitted by law. We provide this service to help the outdoor
            community and operate in good faith to maintain reliable campsite
            monitoring.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Intellectual Property</h2>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>
              camply and its content are protected by copyright and trademark
              laws
            </li>
            <li>
              As a publicly hosted application, reverse engineering for
              educational or non-commercial purposes is acknowledged as
              technically possible
            </li>
            <li>
              However, you may not use any reverse engineered code or knowledge
              to create commercial products or services for profit
            </li>
            <li>
              You may not copy, distribute, or create derivative works for
              commercial purposes without permission
            </li>
            <li>
              User feedback and suggestions may be used to improve our service
            </li>
            <li>You retain ownership of any content you provide to us</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">
            Privacy and Data Ethics
          </h2>
          <p className="mb-4">
            Your privacy is important to us. As a not-for-profit service, we are
            committed to ethical data practices:
          </p>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>
              <strong>We will never sell your personal data</strong> to third
              parties
            </li>
            <li>
              We collect only the minimum data necessary to provide our service
            </li>
            <li>We operate transparently and welcome community oversight</li>
            <li>
              Your data is used solely to help you find available campsites
            </li>
          </ul>
          <p className="mb-4">
            Please review our{" "}
            <Link
              to="/privacy"
              className="text-primary hover:text-primary/80 underline"
            >
              Privacy Policy
            </Link>{" "}
            for complete details on how we collect, use, and protect your
            personal information.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Termination</h2>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>You may terminate your account at any time</li>
            <li>
              We may suspend or terminate accounts for violations of these terms
            </li>
            <li>
              Upon termination, your right to use the service ceases immediately
            </li>
            <li>
              We will delete your personal data in accordance with our{" "}
              <Link
                to="/privacy"
                className="text-primary hover:text-primary/80 underline"
              >
                Privacy Policy
              </Link>
            </li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Changes to Terms</h2>
          <p className="mb-4">
            We reserve the right to modify these terms at any time. We will
            notify users of material changes via email or through the service.
            Continued use after changes constitutes acceptance of the new terms.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Governing Law</h2>
          <p className="mb-4">
            These terms shall be governed by and construed in accordance with
            applicable laws, without regard to conflict of law provisions. As an
            open-source project, we strive to operate in compliance with
            international privacy and data protection standards.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Contact Information</h2>
          <p className="mb-4">
            If you have any questions about these Terms of Service, please
            contact us at:
          </p>
          <ul className="list-none mb-4 space-y-1">
            <li>Email: camply@juftin.com</li>
            <li>
              GitHub:{" "}
              <a
                href="https://github.com/juftin/camply"
                className="text-primary hover:text-primary/80"
              >
                github.com/juftin/camply
              </a>
            </li>
          </ul>
          <p className="mb-4 text-sm text-muted-foreground">
            As an open-source, not-for-profit project, we encourage transparency
            and welcome community feedback on our terms and operations.
          </p>
        </section>
      </div>
    </div>
  );
}
