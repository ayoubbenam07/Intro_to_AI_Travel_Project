import { Typography, Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";

const AIHeadIcon = () => (
  <svg
    width="52"
    height="60"
    viewBox="0 0 52 60"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <path
      d="M26 2C15.507 2 7 10.507 7 21c0 6.574 3.27 12.381 8.286 15.93V46a3 3 0 0 0 3 3h15.428a3 3 0 0 0 3-3v-9.07C41.73 33.381 45 27.574 45 21 45 10.507 36.493 2 26 2z"
      fill="var(--primary)"
    />
    <rect x="19" y="47" width="14" height="7" rx="3.5" fill="var(--primary)" />
    <circle cx="26" cy="20" r="3" fill="white" />
    <path
      d="M26 11a1 1 0 0 1 1 1v1.22a7.1 7.1 0 0 1 2.607 1.08l.863-.863a1 1 0 1 1 1.414 1.414l-.863.863A7.1 7.1 0 0 1 32.1 18.5H33a1 1 0 0 1 0 2h-.9a7.1 7.1 0 0 1-1.08 2.607l.863.863a1 1 0 0 1-1.414 1.414l-.863-.863A7.1 7.1 0 0 1 27 25.1V26a1 1 0 0 1-2 0v-.9a7.1 7.1 0 0 1-2.607-1.08l-.863.863a1 1 0 0 1-1.414-1.414l.863-.863A7.1 7.1 0 0 1 19.9 20.5H19a1 1 0 0 1 0-2h.9a7.1 7.1 0 0 1 1.08-2.607l-.863-.863a1 1 0 1 1 1.414-1.414l.863.863A7.1 7.1 0 0 1 25 12.22V12a1 1 0 0 1 1-1z"
      fill="white"
      fillOpacity="0.9"
    />
  </svg>
);

const AIJourneySection = ({ className = "" }) => {
  const navigate = useNavigate();
  return (
    <>
      <Box
        component="section"
        className={className}
        sx={{
          width: "100%",
          minHeight: "100vh",
          backgroundColor: "var(--color-neutral-100)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: {
            xs: "32px 16px 96px 16px",
            sm: "80px 40px 128px 40px",
            md: "128px 80px 160px 80px",
          },
          boxSizing: "border-box",
          fontFamily: "var(--font-body)",
        }}
      >
        <Box
          sx={{
            backgroundColor: "var(--color-neutral)",
            borderRadius: "36px",
            boxShadow:
              "0 4px 6px rgba(0,0,0,0.04), 0 20px 60px rgba(0,0,0,0.07)",
            maxWidth: "820px",
            width: "100%",
            padding: {
              xs: "40px 16px 48px",
              sm: "72px 64px 80px",
              md: "88px 112px 96px",
            },
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            textAlign: "center",
            boxSizing: "border-box",
          }}
        >
          <Box sx={{ mb: "28px" }}>
            <AIHeadIcon />
          </Box>

          <Typography
            variantMapping={{ inherit: "h2" }}
            variant="inherit"
            sx={{
              fontFamily: "var(--font-headline)",
              fontWeight: 700,
              fontSize: { xs: "1.75rem", sm: "2.75rem", md: "3.25rem" },
              lineHeight: 1.18,
              color: "var(--color-neutral-1000)",
              letterSpacing: "-0.3px",
              mb: "20px",
            }}
          >
            Let the Intelligence Guide You
          </Typography>

          <Typography
            variant="body1"
            sx={{
              fontFamily: "var(--font-body)",
              fontWeight: 400,
              fontSize: { xs: "1rem", md: "1.0625rem" },
              lineHeight: "1.8rem",
              color: "var(--color-neutral-700)",
              maxWidth: "500px",
              mb: "52px",
            }}
          >
            Tell our Mediterranean Intelligence about your interests, and we will
            weave a seamless path through the city, handling reservations, weather
            alerts, and cultural context in real-time.
          </Typography>

          <Box
            sx={{
              position: "relative",
              width: "100%",
              maxWidth: "540px",
            }}
          >
            <Box
              sx={{
                position: "absolute",
                bottom: "-14px",
                left: "5%",
                right: "5%",
                height: "32px",
                borderRadius: "50%",
                background: "rgba(0, 119, 190, 0.22)",
                filter: "blur(14px)",
                zIndex: 0,
              }}
            />
            <Button
              variant="contained"
              fullWidth
              onClick={() => navigate("/plan")}
              sx={{
                position: "relative",
                zIndex: 1,
                borderRadius: "9999px",
                backgroundColor: "var(--color-primary)",
                color: "var(--color-neutral)",
                fontFamily: "var(--font-body)",
                fontWeight: 700,
                fontSize: { xs: "1rem", md: "1.0625rem" },
                letterSpacing: "0.2px",
                textTransform: "none",
                padding: { xs: "16px 32px", md: "20px 40px" },
                boxShadow: "none",
                "&:hover": {
                  backgroundColor: "var(--color-tertiary)",
                  boxShadow: "none",
                },
              }}
            >
              Start Your Journey
            </Button>
          </Box>
        </Box>
      </Box>
    </>
  );
};

AIJourneySection.propTypes = {
  className: PropTypes.string,
};

export default AIJourneySection;