export function PrivacyPolicy() {
  return (
    <div className="container mx-auto py-12 px-4 max-w-4xl">
      <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
      <div className="prose prose-lg max-w-none">
        <p className="text-muted-foreground mb-8">
          <strong>Last updated:</strong> August 2025
        </p>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Introduction</h2>
          <p className="mb-4">
            At camply, we respect your privacy and are committed to protecting
            your personal data. This privacy policy explains how we collect,
            use, and safeguard your information when you use our campsite
            availability monitoring service.
          </p>
          <p className="mb-4 p-4 bg-primary/10 border border-primary/20 rounded-lg">
            <strong>Our Commitment:</strong> camply is operated as a
            not-for-profit service. We will{" "}
            <strong>never sell your personal data</strong> to third parties or
            use it for commercial gain. Our mission is to help outdoor
            enthusiasts find campsites, and we are committed to operating
            ethically and transparently.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">
            Information We Collect
          </h2>
          <h3 className="text-xl font-medium mb-3">Personal Information</h3>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>Email address (for account creation and notifications)</li>
            <li>Name (to personalize your experience)</li>
            <li>Phone number (optional, for SMS notifications)</li>
            <li>Campground preferences and search criteria</li>
          </ul>

          <h3 className="text-xl font-medium mb-3">
            Automatically Collected Information
          </h3>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>Usage data and interaction with our service</li>
            <li>Device information and browser type</li>
            <li>IP address and location data (general location only)</li>
            <li>Cookies and similar tracking technologies</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">
            How We Use Your Information
          </h2>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>Monitor campsite availability based on your preferences</li>
            <li>Send notifications about available campsites</li>
            <li>Provide customer support and respond to inquiries</li>
            <li>Improve our service and develop new features</li>
            <li>Send important updates about our service</li>
            <li>Ensure the security and integrity of our platform</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Information Sharing</h2>
          <p className="mb-4">
            <strong>We will never sell your personal data.</strong> As a
            not-for-profit service, we do not sell, trade, rent, or monetize
            your personal information in any way. We may share your information
            only in the following limited circumstances:
          </p>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>With your explicit consent</li>
            <li>To comply with legal obligations or court orders</li>
            <li>To protect the safety and security of our users</li>
            <li>
              With essential service providers who help us operate our platform
              (email delivery, hosting) under strict confidentiality agreements
            </li>
          </ul>
          <p className="mb-4 text-sm text-muted-foreground">
            <strong>Note:</strong> Given our not-for-profit nature, we have no
            plans for business transfers or mergers that would involve sharing
            your data.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Data Security</h2>
          <p className="mb-4">
            We implement appropriate technical and organizational measures to
            protect your personal data against unauthorized access, alteration,
            disclosure, or destruction. However, no internet-based service can
            be 100% secure.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Your Rights</h2>
          <p className="mb-4">You have the right to:</p>
          <ul className="list-disc list-inside mb-4 space-y-2">
            <li>Access your personal data</li>
            <li>Correct inaccurate or incomplete data</li>
            <li>Delete your personal data</li>
            <li>Object to processing of your data</li>
            <li>Data portability</li>
            <li>Withdraw consent at any time</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Cookies</h2>
          <p className="mb-4">
            We use cookies and similar technologies to enhance your experience,
            remember your preferences, and analyze usage patterns. You can
            control cookie settings through your browser preferences.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Data Retention</h2>
          <p className="mb-4">
            We retain your personal data only as long as necessary to provide
            our services and fulfill the purposes outlined in this policy,
            unless a longer retention period is required by law.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Children's Privacy</h2>
          <p className="mb-4">
            Our service is not intended for children under 13 years of age. We
            do not knowingly collect personal information from children under
            13.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">
            Changes to This Policy
          </h2>
          <p className="mb-4">
            We may update this privacy policy from time to time. We will notify
            you of any material changes by posting the new policy on this page
            and updating the "Last updated" date.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Contact Us</h2>
          <p className="mb-4">
            If you have any questions about this privacy policy or our data
            practices, please contact us at:
          </p>
          <ul className="list-none mb-4 space-y-1">
            <li>
              Email:{" "}
              <a
                href="mailto:camply@juftin.com"
                className="text-primary hover:text-primary/80"
              >
                camply@juftin.com
              </a>
            </li>
            <li>
              GitHub:{" "}
              <a
                href="https://github.com/juftin/camply"
                className="text-primary hover:text-primary/80"
              >
                github.com/juftin/camply-web
              </a>
            </li>
          </ul>
          <p className="mb-4 text-sm text-muted-foreground">
            As an open-source, not-for-profit project, we welcome transparency
            and community feedback on our privacy practices.
          </p>
        </section>
      </div>
    </div>
  );
}
