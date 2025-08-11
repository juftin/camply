import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { Home } from "@/pages/Home";
import { Providers } from "@/pages/Providers";
import { Auth } from "@/pages/Auth";
import { PrivacyPolicy } from "@/pages/PrivacyPolicy";
import { TermsOfService } from "@/pages/TermsOfService";
import { Contact } from "@/pages/Contact";
import { Contribute } from "@/pages/Contribute";
import { FAQ } from "@/pages/FAQ";
import { Ethos } from "@/pages/Ethos";
import { HowItWorks } from "@/pages/HowItWorks";
import { Campground } from "@/pages/Campground";
import { RecreationArea } from "@/pages/RecreationArea";

// Get base path from Vite's import.meta.env.BASE_URL
const basename = import.meta.env.BASE_URL.replace(/\/$/, "");

function App() {
  return (
    <Router basename={basename}>
      <Routes>
        {/* Auth page without layout */}
        <Route path="/auth" element={<Auth />} />

        {/* Pages with layout */}
        <Route
          path="/*"
          element={
            <Layout>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/providers" element={<Providers />} />
                <Route path="/ethos" element={<Ethos />} />
                <Route path="/how-it-works" element={<HowItWorks />} />
                <Route path="/contribute" element={<Contribute />} />
                <Route path="/faq" element={<FAQ />} />
                <Route path="/privacy" element={<PrivacyPolicy />} />
                <Route path="/terms" element={<TermsOfService />} />
                <Route path="/contact" element={<Contact />} />
                <Route
                  path="/campground/:providerId/:campgroundId"
                  element={<Campground />}
                />
                <Route
                  path="/rec-area/:providerId/:recreationAreaId"
                  element={<RecreationArea />}
                />
              </Routes>
            </Layout>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
