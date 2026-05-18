import { useState, useEffect } from "react";
import casbahRegister from "./casbahRegister.png";

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

export default function Register() {
  const isDesktop = useIsDesktop();

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: isDesktop ? "row" : "column",
        background: "var(--color-neutral-100)",
        fontFamily: "var(--font-body)",
      }}
    >
      <div
        style={{
          position: "relative",
          width: isDesktop ? "50%" : "100%",
          minHeight: isDesktop ? "100vh" : "50vh",
          overflow: "hidden",
          flexShrink: 0,
        }}
      >
        <img
          src={casbahRegister}
          alt="The Casbah"
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: 0.9,
          }}
        />

        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to right, rgba(0,119,190,0.10), transparent)",
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to top, rgba(0,119,190,0.55), transparent 60%)",
          }}
        />

        <div
          style={{
            position: "absolute",
            top: isDesktop ? 32 : 24,
            left: isDesktop ? 44 : 24,
            zIndex: 10,
          }}
        >
          <span
            style={{
              fontFamily: "var(--font-headline)",
              fontSize: isDesktop ? "2.5rem" : "1.75rem",
              fontWeight: 500,
              letterSpacing: "-0.025em",
              color: "var(--color-neutral-1000)",
              lineHeight: 1,
            }}
          >
            Algiers AI
          </span>
        </div>

        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            padding: isDesktop ? "0 64px 56px" : "0 24px 32px",
            zIndex: 10,
          }}
        >
          <p
            style={{
              color: "var(--color-secondary)",
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "2.4px",
              textTransform: "uppercase",
              marginBottom: 12,
              fontFamily: "var(--font-body)",
            }}
          >
            THE CASBAH EXPERIENCE
          </p>
          <blockquote
            style={{
              fontFamily: "var(--font-headline)",
              color: "var(--color-neutral)",
              fontSize: isDesktop ? "2.75rem" : "1.5rem",
              fontStyle: "italic",
              fontWeight: 400,
              lineHeight: 1.2,
              margin: 0,
              maxWidth: 480,
              textShadow: "0 2px 12px rgba(0,0,0,0.3)",
            }}
          >
            "To travel through the Casbah is to walk within the architecture of
            memory itself, a labyrinth of light and sea-salt."
          </blockquote>
        </div>
      </div>

      <div
        style={{
          position: "relative",
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "var(--color-neutral-100)",
          overflow: "hidden",
          padding: isDesktop ? "80px" : "40px 24px 56px",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: 320,
            height: 320,
            borderRadius: "50%",
            background: "var(--color-primary-light)",
            filter: "blur(60px)",
            transform: "translate(30%, -30%)",
            pointerEvents: "none",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            width: 320,
            height: 320,
            borderRadius: "50%",
            background: "var(--color-primary-light)",
            filter: "blur(60px)",
            transform: "translate(-30%, 30%)",
            pointerEvents: "none",
          }}
        />

        <div
          style={{
            position: "relative",
            width: "100%",
            maxWidth: 512,
            display: "flex",
            flexDirection: "column",
            gap: isDesktop ? 48 : 36,
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <h1
              style={{
                fontFamily: "var(--font-headline)",
                color: "var(--color-neutral-1000)",
                fontSize: isDesktop ? "3rem" : "2.25rem",
                fontWeight: 500,
                lineHeight: 1.1,
                margin: 0,
              }}
            >
              Create Your Profile
            </h1>
            <p
              style={{
                fontFamily: "var(--font-body)",
                color: "var(--color-neutral-700)",
                fontSize: 16,
                lineHeight: "24px",
                margin: 0,
              }}
            >
              Step into the future of Algerian exploration.
            </p>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
            <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
              <Field label="Full Name">
                <UnderlineInput type="text" placeholder="Meghabber Mohammed Al Ghazali" />
              </Field>
              <Field label="Email Address">
                <UnderlineInput type="email" placeholder="contact@algiersai.dz" />
              </Field>
              <Field label="Secure Password">
                <UnderlineInput type="password" placeholder="••••••••" />
              </Field>
            </div>

            <button
              type="submit"
              onClick={() => {
                localStorage.setItem("isLoggedIn", "true");
                localStorage.setItem("userEmail", "meghabber@algiers.ai");
                window.location.href = "/profile";
              }}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 12,
                borderRadius: 9999,
                background: "var(--color-primary)",
                color: "var(--color-neutral)",
                padding: "18px 0",
                fontSize: isDesktop ? 20 : 17,
                fontWeight: 600,
                letterSpacing: "1px",
                fontFamily: "var(--font-body)",
                border: "none",
                cursor: "pointer",
                boxShadow:
                  "0 20px 25px -5px rgba(0,0,0,0.10), 0 8px 10px -6px rgba(0,0,0,0.10)",
                transition: "background 0.2s",
                WebkitTapHighlightColor: "transparent",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.background = "var(--color-primary-hover)")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.background = "var(--color-primary)")
              }
            >
              Begin My Journey
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path
                  d="M12.175 9H0V7H12.175L6.575 1.4L8 0L16 8L8 16L6.575 14.6L12.175 9Z"
                  fill="white"
                />
              </svg>
            </button>

            <p
              style={{
                textAlign: "center",
                fontSize: 13,
                lineHeight: "22px",
                color: "var(--color-neutral-800)",
                margin: 0,
                fontFamily: "var(--font-body)",
              }}
            >
              By continuing, you agree to our{" "}
              <a
                href="#"
                style={{ color: "var(--color-primary)", textDecoration: "none" }}
              >
                Terms of Intelligence
              </a>
              .
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

const labelStyle = {
  color: "var(--color-neutral-500)",
  fontSize: 11,
  fontWeight: 700,
  letterSpacing: "1.2px",
  textTransform: "uppercase",
  fontFamily: "var(--font-body)",
};

function Field({ label, children }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <label style={labelStyle}>{label}</label>
      {children}
    </div>
  );
}

function UnderlineInput({ type, placeholder }) {
  const [focused, setFocused] = useState(false);
  return (
    <input
      type={type}
      placeholder={placeholder}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      style={{
        width: "100%",
        boxSizing: "border-box",
        background: "transparent",
        border: "none",
        borderBottom: `1px solid ${
          focused ? "var(--color-primary)" : "var(--color-neutral-300)"
        }`,
        paddingBottom: 14,
        paddingTop: 12,
        fontSize: 16,
        color: "var(--color-neutral-1000)",
        fontFamily: "var(--font-body)",
        outline: "none",
        transition: "border-color 0.18s",
        borderRadius: 0,
      }}
    />
  );
}