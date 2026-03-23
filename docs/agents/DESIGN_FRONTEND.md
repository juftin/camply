# DESIGN_FRONTEND: User Journey & Design System

This document defines the user experience and visual architecture for the `camply` frontend.

## 🎯 Design Goals
1. **Frictionless Search**: Find a campground and start a scan in < 30 seconds.
2. **Real-time Feedback**: Users should know exactly when their scans were last checked.
3. **Mobile-First**: Most users will check alerts on their phones; the dashboard must be responsive.
4. **Professional & Clean**: High-impact "Utility SaaS" aesthetic (inspired by clean, modern tools).

---

## 🏗️ Design System: Shadcn/UI + Tailwind

We will use **Shadcn/UI** as the foundation, allowing us to build accessible, themeable components quickly.

- **Primary Colors**: Nature-inspired (Forest Green, Slate, Earthy Orange).
- **Typography**: Clean sans-serif (Inter or Geist).
- **Components**:
    - `Command`: For global campground search.
    - `Dialog`: For creating and editing scans.
    - `Card`: For active scan items.
    - `Toast`: For notification success/failure feedback.
    - `Skeleton`: For loading states while fetching scan data.

---

## 🛤️ User Journey Map

### 1. Landing & Authentication
- **Hero**: Existing `Home.tsx` landing page.
- **Authentication**: Refactor `Auth.tsx` from a custom form to an Auth0 redirect.
- **Early Access Check**: Backend verifies email whitelist; unauthorized users see a dedicated "Request Access" page.

### 2. Main Dashboard (`/dashboard`)
- **Active Scans**: A grid of cards showing current monitoring tasks.
- **Navigation**: The existing `Header.tsx` should be updated to show "Dashboard" and "Profile" links for authenticated users.

### 3. Scan Creation Flow
1. **Find Park**: Use the existing `SearchBar.tsx` component.
2. **Action**: Clicking a campground result opens the `ScanForm` (Dialog or dedicated page).
3. **Configure**: Select dates, min stay, and campsite types.
4. **Save**: Scan is sent to the backend.

### 4. Alert & History Feed
- **Success Notifications**: View details of found campsites (Site #, Loop, Dates).
- **Direct Link**: A prominent button to book directly on the provider's site.

---

## 🔄 Frontend Architecture

- **Framework**: React 18 + TypeScript + Vite.
- **State Management**: **TanStack Query** (React Query) for server-state synchronization.
- **Form Handling**: **React Hook Form** + **Zod** for strict validation.
- **API Client**: Automated TypeScript SDK generated from backend OpenAPI schema.
- **Routing**: **TanStack Router** or **React Router** for clean, nested navigation.

---

## 📱 Responsiveness Requirements
- **Mobile (< 640px)**: Single-column scan cards, simplified search, bottom navigation for Dashboard/Profile.
- **Desktop (> 1024px)**: Multi-column grid, detailed sidebars for scan filters.
