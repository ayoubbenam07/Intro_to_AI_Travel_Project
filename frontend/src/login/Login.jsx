import { useState, useEffect } from "react";
import seaLogin from "./seaLogin.png";

const API = {
  async loginWithEmail(email, password) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (email && password) resolve({ token: "mock_token", user: { email } });
        else reject(new Error("Invalid credentials"));
      }, 800);
    });
  },
};

function useIsDesktop() {
  const [isDesktop, setIsDesktop] = useState(
    typeof window !== "undefined" ? window.innerWidth >= 1024 : true
  );
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 1024px)");
    const handler = (e) => setIsDesktop(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);
  return isDesktop;
}

export default function Login() {
  const isDesktop = useIsDesktop();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");
    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }
    setLoading(true);
    try {
      const { token, user } = await API.loginWithEmail(email, password);
      console.log("Logged in:", user, token);
      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("userEmail", email);
      window.location.href = "/profile";
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: isDesktop ? "row" : "column",
        background: "var(--color-neutral)",
        fontFamily: "var(--font-body)",
      }}
    >
      {!isDesktop && (
        <div style={{ position: "relative", height: 280, overflow: "hidden", flexShrink: 0 }}>
          <img
            src={seaLogin}
            alt="Algiers cityscape"
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(0deg, rgba(0,119,190,0.45) 0%, rgba(0,119,190,0.00) 60%)",
            }}
          />
          <div
            style={{
              position: "absolute",
              bottom: 0,
              left: 0,
              padding: "0 24px 28px",
            }}
          >
            <h1
              style={{
                fontFamily: "var(--font-headline)",
                color: "var(--color-neutral)",
                fontSize: 30,
                fontWeight: 500,
                lineHeight: 1.2,
                letterSpacing: "-0.5px",
                margin: 0,
              }}
            >
              Algiers AI
            </h1>
          </div>
        </div>
      )}

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: isDesktop ? "64px 96px" : "48px 24px 56px",
          background: "var(--color-neutral)",
        }}
      >
        <div
          style={{
            width: "100%",
            maxWidth: 448,
            display: "flex",
            flexDirection: "column",
            gap: 30,
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <h2
              style={{
                fontFamily: "var(--font-headline)",
                fontSize: "clamp(36px, 5vw, 48px)",
                fontWeight: 500,
                lineHeight: 1.167,
                color: "var(--color-neutral-1000)",
                margin: 0,
              }}
            >
              Welcome Back
            </h2>
            <p
              style={{
                color: "var(--color-neutral-700)",
                fontSize: 16,
                lineHeight: "24px",
                margin: 0,
                fontFamily: "var(--font-body)",
              }}
            >
              Continue your journey through the white city.
            </p>
          </div>

          <div
            style={{ display: "flex", flexDirection: "column", gap: 40, width: "100%" }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
              <UnderlineField
                label="Email Address"
                type="email"
                value={email}
                onChange={setEmail}
                placeholder="explorer@algiers.ai"
              />

              <UnderlineField
                label="Password"
                labelRight={
                  <a
                    href="#"
                    style={{
                      color: "var(--color-primary)",
                      fontSize: 12,
                      fontWeight: 700,
                      letterSpacing: "0.6px",
                      textTransform: "uppercase",
                      textDecoration: "none",
                      fontFamily: "var(--font-body)",
                    }}
                  >
                    Forgot?
                  </a>
                }
                type="password"
                value={password}
                onChange={setPassword}
                placeholder="••••••••"
              />
            </div>

            {error && (
              <p
                style={{
                  color: "#c0392b",
                  fontSize: 13,
                  margin: "-16px 0 0",
                  fontFamily: "var(--font-body)",
                }}
              >
                {error}
              </p>
            )}

            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 24,
                paddingTop: 16,
              }}
            >
              <PillButton
                onClick={handleLogin}
                disabled={loading}
                label={loading ? "Entering…" : "Begin Journey"}
                icon={<ArrowRightIcon />}
              />

              <div style={{ display: "flex", justifyContent: "center" }}>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    window.location.href = "/";
                  }}
                  style={{
                    color: "var(--color-primary)",
                    fontFamily: "var(--font-body)",
                    fontSize: 20,
                    fontWeight: 600,
                    letterSpacing: "1px",
                    textDecoration: "none",
                  }}
                >
                  Discover as Guest
                </a>
              </div>
            </div>
          </div>

          <div
            style={{
              borderTop: "1px solid var(--color-neutral-200)",
              paddingTop: 16,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <p
              style={{
                fontSize: 14,
                lineHeight: "24px",
                textAlign: "center",
                margin: 0,
                fontFamily: "var(--font-body)",
              }}
            >
              <span style={{ color: "var(--color-neutral-1000)" }}>
                Are you new here?{" "}
              </span>
              <a
                href="/register"
                style={{ color: "var(--color-primary)", textDecoration: "none" }}
              >
                Create Account
              </a>
            </p>
          </div>
        </div>
      </div>

      {isDesktop && (
        <div
          style={{
            flex: 1,
            position: "relative",
            overflow: "hidden",
            minHeight: "100vh",
          }}
        >
          <img
            src={seaLogin}
            alt="Algiers cityscape"
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(90deg, rgba(0,119,190,0.10) 0%, rgba(0,119,190,0.00) 100%)",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "linear-gradient(0deg, rgba(0,119,190,0.40) 0%, rgba(0,119,190,0.00) 50%)",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-end",
              padding: 80,
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 16,
                maxWidth: 448,
                paddingBottom: 32,
              }}
            >
              <h1
                style={{
                  fontFamily: "var(--font-headline)",
                  color: "var(--color-neutral)",
                  fontSize: 48,
                  fontWeight: 500,
                  lineHeight: "56px",
                  letterSpacing: "-1.2px",
                  margin: 0,
                }}
              >
                Algiers AI
              </h1>
              <p
                style={{
                  color: "var(--color-neutral)",
                  fontSize: 18,
                  fontStyle: "italic",
                  lineHeight: "32px",
                  opacity: 0.9,
                  margin: 0,
                  fontFamily: "var(--font-body)",
                }}
              >
                "Algiers is a city of white steps leading to a sky of infinite blue,
                where every corner whispers a century-old secret."
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


function UnderlineField({ label, labelRight, type, value, onChange, placeholder }) {
  const [focused, setFocused] = useState(false);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 4, width: "100%" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <label
          style={{
            color: "var(--color-neutral-500)",
            fontSize: 12,
            fontWeight: 700,
            letterSpacing: "0.6px",
            textTransform: "uppercase",
            fontFamily: "var(--font-body)",
          }}
        >
          {label}
        </label>
        {labelRight}
      </div>
      <div
        style={{
          borderBottom: `1px solid ${
            focused ? "var(--color-primary)" : "var(--color-neutral-300)"
          }`,
          paddingBottom: 17,
          paddingTop: 16,
          transition: "border-color 0.18s",
        }}
      >
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          style={{
            width: "100%",
            color: "var(--color-neutral-500)",
            fontFamily: "var(--font-body)",
            fontSize: 18,
            fontWeight: 400,
            background: "transparent",
            outline: "none",
            border: "none",
            boxSizing: "border-box",
          }}
        />
      </div>
    </div>
  );
}

function PillButton({ label, icon, onClick, disabled }) {
  const [hovered, setHovered] = useState(false);
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 12,
        padding: "20px 0",
        borderRadius: 9999,
        background: disabled
          ? "var(--color-neutral-400)"
          : hovered
          ? "var(--color-primary-hover)"
          : "var(--color-primary)",
        color: "var(--color-neutral)",
        fontFamily: "var(--font-body)",
        fontSize: 20,
        fontWeight: 600,
        letterSpacing: "1px",
        border: "none",
        cursor: disabled ? "not-allowed" : "pointer",
        boxShadow: "0 10px 25px -5px rgba(0,119,190,0.25)",
        transition: "background 0.2s",
        WebkitTapHighlightColor: "transparent",
      }}
    >
      {label}
      {icon}
    </button>
  );
}


function ArrowRightIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 20 20"
      fill="none"
      strokeWidth="1.5"
      stroke="white"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4 10h12M11 5l5 5-5 5" />
    </svg>
  );
}