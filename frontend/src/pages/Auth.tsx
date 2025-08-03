import * as React from "react";
import { TentTree, Mail, Lock, User, Eye, EyeOff, Tent } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Link, useSearchParams } from "react-router-dom";
import { Header } from "@/components/Header";
import { DismissibleBanner } from "@/components/DismissibleBanner";

export function Auth() {
  const [searchParams] = useSearchParams();
  const [isSignUp, setIsSignUp] = React.useState(
    searchParams.get("mode") === "signup",
  );
  const [showPassword, setShowPassword] = React.useState(false);
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const passwordsMatch = formData.password === formData.confirmPassword;
  const showPasswordMismatch =
    isSignUp && formData.confirmPassword && !passwordsMatch;

  // Password complexity validation
  const passwordRequirements = {
    minLength: formData.password.length >= 8,
    hasUppercase: /[A-Z]/.test(formData.password),
    hasLowercase: /[a-z]/.test(formData.password),
    hasNumber: /\d/.test(formData.password),
    hasSpecialChar: /[!@#$%^&*(),.?":{}|<>]/.test(formData.password),
  };

  const isPasswordValid = Object.values(passwordRequirements).every(Boolean);
  const showPasswordValidation =
    isSignUp && formData.password && !isPasswordValid;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (isSignUp && (!passwordsMatch || !isPasswordValid)) {
      return; // Prevent form submission if passwords don't match or aren't valid
    }

    // TODO: Add authentication logic
    console.log("Form submitted:", formData);
  };

  const toggleMode = () => {
    setIsSignUp(!isSignUp);
    setFormData({
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    });
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header showLogo={false} />

      {/* Development Banner - only show on signup */}
      <DismissibleBanner
        id="auth-signup"
        icon={Tent}
        showCondition={isSignUp}
        storageType="session"
        className="bg-orange-100 border-b border-orange-200 py-3 px-4 text-orange-800"
        closeButtonClassName="hover:bg-orange-200 text-orange-800"
      >
        <p className="text-sm font-medium text-center">
          Uh oh! camply isn't accepting new users yet. Beta version coming soon,
          can't wait for you to try it out!
        </p>
      </DismissibleBanner>

      <div className="flex-1 flex items-center justify-center px-4 py-6">
        <div className="w-full max-w-md">
          {/* Logo Section */}
          <div className="text-center mb-6">
            <Link to="/" className="inline-flex items-center space-x-2">
              <TentTree className="h-8 w-8 text-primary" />
              <span className="text-2xl font-bold">camply</span>
            </Link>
            <p className="text-muted-foreground mt-1 text-sm">
              Never miss your perfect campsite
            </p>
          </div>

          <Card>
            <CardHeader className="text-center pb-4">
              <CardTitle className="text-xl">
                {isSignUp ? "Create Account" : "Let's Go Camping"}
              </CardTitle>
              <CardDescription className="text-sm">
                {isSignUp
                  ? "Sign up to start monitoring campsite availability"
                  : "Sign in to your camply account"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-3">
                {/* Name field - only for sign up */}
                {isSignUp && (
                  <div className="space-y-1">
                    <label htmlFor="name" className="text-sm font-medium">
                      Full Name
                    </label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                      <Input
                        id="name"
                        name="name"
                        type="text"
                        placeholder="Enter your full name"
                        value={formData.name}
                        onChange={handleInputChange}
                        className="pl-10"
                        required={isSignUp}
                      />
                    </div>
                  </div>
                )}

                {/* Email field */}
                <div className="space-y-1">
                  <label htmlFor="email" className="text-sm font-medium">
                    Email Address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="Enter your email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="pl-10"
                      required
                    />
                  </div>
                </div>

                {/* Password field */}
                <div className="space-y-1">
                  <label htmlFor="password" className="text-sm font-medium">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                    <Input
                      id="password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className="pl-10 pr-10"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                  {showPasswordValidation && (
                    <div className="mt-2 space-y-1">
                      <p className="text-xs text-muted-foreground">
                        Password must contain:
                      </p>
                      <div className="grid grid-cols-1 gap-1 text-xs">
                        <div
                          className={`flex items-center gap-1 ${passwordRequirements.minLength ? "text-green-600" : "text-red-500"}`}
                        >
                          <span className="text-xs">
                            {passwordRequirements.minLength ? "✓" : "✗"}
                          </span>
                          At least 8 characters
                        </div>
                        <div
                          className={`flex items-center gap-1 ${passwordRequirements.hasUppercase ? "text-green-600" : "text-red-500"}`}
                        >
                          <span className="text-xs">
                            {passwordRequirements.hasUppercase ? "✓" : "✗"}
                          </span>
                          One uppercase letter
                        </div>
                        <div
                          className={`flex items-center gap-1 ${passwordRequirements.hasLowercase ? "text-green-600" : "text-red-500"}`}
                        >
                          <span className="text-xs">
                            {passwordRequirements.hasLowercase ? "✓" : "✗"}
                          </span>
                          One lowercase letter
                        </div>
                        <div
                          className={`flex items-center gap-1 ${passwordRequirements.hasNumber ? "text-green-600" : "text-red-500"}`}
                        >
                          <span className="text-xs">
                            {passwordRequirements.hasNumber ? "✓" : "✗"}
                          </span>
                          One number
                        </div>
                        <div
                          className={`flex items-center gap-1 ${passwordRequirements.hasSpecialChar ? "text-green-600" : "text-red-500"}`}
                        >
                          <span className="text-xs">
                            {passwordRequirements.hasSpecialChar ? "✓" : "✗"}
                          </span>
                          One special character
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Confirm Password field - only for sign up */}
                {isSignUp && (
                  <div className="space-y-1">
                    <label
                      htmlFor="confirmPassword"
                      className="text-sm font-medium"
                    >
                      Confirm Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                      <Input
                        id="confirmPassword"
                        name="confirmPassword"
                        type="password"
                        placeholder="Confirm your password"
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        className={`pl-10 ${showPasswordMismatch ? "border-red-500 focus:border-red-500 focus:ring-red-500" : ""}`}
                        required={isSignUp}
                      />
                    </div>
                    {showPasswordMismatch && (
                      <p className="text-xs text-red-500 mt-1">
                        Passwords do not match
                      </p>
                    )}
                  </div>
                )}

                {/* Forgot Password link - only for sign in */}
                {!isSignUp && (
                  <div className="text-right">
                    <a
                      href="#"
                      className="text-sm text-primary hover:text-primary/80"
                    >
                      Forgot password?
                    </a>
                  </div>
                )}

                {/* Submit Button */}
                <Button
                  type="submit"
                  className="w-full mt-2"
                  disabled={isSignUp}
                >
                  {isSignUp ? "Create Account" : "Sign In"}
                </Button>

                {/* Divider */}
                <div className="relative my-3">
                  <div className="absolute inset-0 flex items-center">
                    <span className="w-full border-t" />
                  </div>
                  <div className="relative flex justify-center text-xs uppercase">
                    <span className="bg-background px-2 text-muted-foreground">
                      Or continue with
                    </span>
                  </div>
                </div>

                {/* Social Login Buttons */}
                <div className="grid grid-cols-2 gap-2">
                  <Button
                    variant="outline"
                    type="button"
                    className="w-full"
                    disabled={isSignUp}
                  >
                    <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
                      <path
                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                        fill="#4285F4"
                      />
                      <path
                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                        fill="#34A853"
                      />
                      <path
                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                        fill="#FBBC05"
                      />
                      <path
                        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                        fill="#EA4335"
                      />
                    </svg>
                    Google
                  </Button>
                  <Button
                    variant="outline"
                    type="button"
                    className="w-full"
                    disabled={isSignUp}
                  >
                    <svg
                      className="mr-2 h-4 w-4"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
                    </svg>
                    GitHub
                  </Button>
                </div>
              </form>

              {/* Toggle between Sign In / Sign Up */}
              <div className="mt-6 text-center">
                <span className="text-muted-foreground">
                  {isSignUp
                    ? "Already have an account?"
                    : "Don't have an account?"}
                </span>{" "}
                <button
                  onClick={toggleMode}
                  className="text-primary hover:text-primary/80 font-medium"
                >
                  {isSignUp ? "Sign in" : "Sign up"}
                </button>
              </div>
            </CardContent>
          </Card>

          {/* Terms and Privacy */}
          <div className="mt-4 text-center text-xs text-muted-foreground">
            By continuing, you agree to our{" "}
            <Link to="/terms" className="text-primary hover:text-primary/80">
              Terms of Service
            </Link>{" "}
            and{" "}
            <Link to="/privacy" className="text-primary hover:text-primary/80">
              Privacy Policy
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
