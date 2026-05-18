import { Typography, Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import heropic from "./herosectionpic.png";
import casbahpic from "./casbah.png";
import notreDamePic from "./notreDame.png";





const sx = {


  heroSection: {
    display: "flex",
    flex: 1,
    alignItems: "flex-start",
    position: "relative",
    width: "100%",
    lineHeight: "normal",
    letterSpacing: "normal",
  },

  mainContainer: {
    flex: 1,
    background: "linear-gradient(0deg, #f9f9f9, rgba(249,249,249,0.1) 38.4%, rgba(249,249,249,0))",
    padding: "11.593rem 5rem",
    boxSizing: "border-box",
    isolation: "isolate",
    maxWidth: "100%",
    zIndex: 1,
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "space-between",
    position: "relative",
    gap: "2rem",
    "@media (max-width:900px)": {
      paddingTop: "7.563rem",
      paddingBottom: "7.563rem",
      flexDirection: "column",
      alignItems: "center",
      gap: "3rem",
    },
    "@media (max-width:700px)": {
      paddingLeft: "1.5rem",
      paddingRight: "1.5rem",
      flexDirection: "column",
    },
  },

  bgImage: {
    height: "100%",
    width: "100%",
    position: "absolute",
    margin: 0,
    top: 0,
    left: 0,
    objectFit: "cover",
    flexShrink: 0,
    zIndex: 0,
  },

  gradient: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    height: "12rem",
    background: "linear-gradient(to bottom, transparent, #f3f3f4)",
    zIndex: 1,
    pointerEvents: "none",
  },


  container: {
    alignSelf: "stretch",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    padding: "5rem 0 0",
    boxSizing: "border-box",
    gap: "1.5rem",
    maxWidth: "56rem",
    zIndex: 2,
    flexShrink: 0,
    textAlign: "left",
    fontSize: "5rem",
    color: "var(--color-neutral-1000)",
    fontFamily: "var(--font-body)",
    "@media (max-width:900px)": { maxWidth: "100%" },
    "@media (max-width:700px)": { paddingTop: "3.25rem" },
  },

  heading1: {
    alignSelf: "stretch",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    fontFamily: "var(--font-headline)",
  },

  titleText: {
    margin: 0,
    position: "relative",
    filter: "drop-shadow(0px 3px 5px rgba(26,28,28,0.5))",
    fontWeight: "700",
    lineHeight: "5.625rem",
    letterSpacing: "-1.6px",
    "@media (max-width:900px)": { fontSize: "3.5rem", lineHeight: "4rem" },
    "@media (max-width:450px)": { fontSize: "2.5rem", lineHeight: "3rem" },
  },

  infiniteAlgiers: { color: "var(--color-primary)" },

  descriptionBox: {
    width: "100%",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    maxWidth: "36rem",
    fontSize: "1.375rem",
    color: "var(--color-neutral-700)",
    "@media (max-width:700px)": { maxWidth: "100%" },
  },

  descriptionText: {
    alignSelf: "stretch",
    position: "relative",
    lineHeight: "2rem",
    fontWeight: 600,
    "@media (max-width:450px)": { fontSize: "1.125rem", lineHeight: "1.625rem" },
  },

  buttonRow: {
    alignSelf: "stretch",
    display: "flex",
    alignItems: "flex-start",
    padding: "1rem 0 0",
    gap: "1.5rem",
    textAlign: "center",
    fontSize: "1rem",
    color: "#fff",
    "@media (max-width:700px)": { flexDirection: "column", alignItems: "stretch" },
  },

  primaryButton: {
    borderRadius: "9999px",
    backgroundColor: "var(--color-primary)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "1.281rem 2.5rem 1.343rem",
    position: "relative",
    isolation: "isolate",
    cursor: "pointer",
  },

  buttonShadow: {
    width: "100%",
    height: "100%",
    position: "absolute",
    top: 0,
    right: "0.019rem",
    bottom: 0,
    left: 0,
    boxShadow: "0 25px 50px -12px rgba(0, 94, 151, 0.3)",
    borderRadius: "9999px",
    backgroundColor: "transparent",
    zIndex: 0,
    flexShrink: 0,
  },

  primaryButtonLabel: {
    position: "relative",
    zIndex: 1,
    flexShrink: 0,
    lineHeight: "1.5rem",
    fontWeight: "700",
  },

  secondaryButton: {
    textTransform: "none",
    color: "var(--color-neutral-1000)",
    fontSize: "16px",
    background: "rgba(255, 255, 255, 0.4)",
    border: "rgba(255, 255, 255, 0.3) solid 1px",
    borderRadius: "9999px",
    backdropFilter: "blur(30px)",
    padding: "1.25rem 2.5rem",
    "&:hover": { background: "rgba(255, 255, 255, 0.4)" },
    "@media (max-width:700px)": { padding: "1rem 2.5rem" },
  },


  floatingCards: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    gap: "2.5rem",
    zIndex: 2,
    flexShrink: 0,
    paddingTop: "2rem",
    lineHeight: "normal",
    letterSpacing: "normal",
    "@media (max-width:700px)": { width: "100%" },
  },


  card: {
    width: "20rem",
    backdropFilter: "blur(30px)",
    backgroundColor: "rgba(255, 255, 255, 0.4)",
    border: "1px solid rgba(255, 255, 255, 0.3)",
    borderRadius: "40px",
    boxSizing: "border-box",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    padding: "1.5rem",
    position: "relative",
    isolation: "isolate",
    gap: "0.5rem",
    textAlign: "left",
    fontSize: "0.75rem",
    color: "var(--color-neutral)",
    fontFamily: "var(--font-body)",
    "@media (max-width:700px)": { width: "100%" },
  },

  cardShadow: {
    width: "100%",
    height: "100%",
    position: "absolute",
    top: 0,
    bottom: 0,
    left: 0,
    boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
    borderRadius: "40px",
    backgroundColor: "transparent",
    zIndex: 0,
    flexShrink: 0,
  },

  cardImageWrapper: {
    alignSelf: "stretch",
    height: "12rem",
    borderRadius: "24px",
    flexShrink: 0,
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    justifyContent: "center",
    position: "relative",
    overflow: "hidden",
    isolation: "isolate",
    zIndex: 1,
  },

  cardImage: {
    flex: 1,
    alignSelf: "stretch",
    position: "relative",
    maxWidth: "100%",
    maxHeight: "100%",
    objectFit: "cover",
    overflow: "hidden",
    zIndex: 0,
  },

  cardImageGradient: {
    position: "absolute",
    width: "100%",
    height: "100%",
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    background: "linear-gradient(0deg, rgba(0,0,0,0.6), transparent)",
    zIndex: 1,
  },

  cardLabel: {
    position: "absolute",
    bottom: "1rem",
    left: "1rem",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    zIndex: 2,
  },

  cardLabelText: {
    position: "relative",
    textTransform: "uppercase",
    lineHeight: "1rem",
    letterSpacing: "1.2px",
    fontWeight: "700",
  },

  cardHeading: {
    alignSelf: "stretch",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    padding: "0.5rem 0 0",
    zIndex: 2,
    flexShrink: 0,
    fontSize: "1.25rem",
    color: "var(--color-neutral-1000)",
  },

  cardTitle: {
    margin: 0,
    alignSelf: "stretch",
    position: "relative",
    fontWeight: "600",
    lineHeight: "1.75rem",
    letterSpacing: "1px",
  },

  cardBody: {
    alignSelf: "stretch",
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    zIndex: 3,
    flexShrink: 0,
    fontSize: "0.875rem",
    color: "var(--color-neutral-700)",
  },

  cardBodyText: {
    alignSelf: "stretch",
    position: "relative",
    lineHeight: "1.5rem",
  },
};


const GlassCard = ({ imageSrc, label, title, description }) => (
  <Box component="section" sx={sx.card}>
    <Box sx={sx.cardShadow} />

    <Box sx={sx.cardImageWrapper}>
      <Box component="img" sx={sx.cardImage} loading="lazy" alt="" src={imageSrc} />
      <Box sx={sx.cardImageGradient} />
      <Box sx={sx.cardLabel}>
        <Typography
          variant="inherit"
          variantMapping={{ inherit: "b" }}
          sx={sx.cardLabelText}
        >
          {label}
        </Typography>
      </Box>
    </Box>

    <Box sx={sx.cardHeading}>
      <Typography
        variant="inherit"
        variantMapping={{ inherit: "h3" }}
        sx={sx.cardTitle}
      >
        {title}
      </Typography>
    </Box>

    <Box sx={sx.cardBody}>
      <div style={{ alignSelf: "stretch", position: "relative", lineHeight: "1.5rem" }}>
        {description}
      </div>
    </Box>
  </Box>
);

GlassCard.propTypes = {
  imageSrc: PropTypes.string,
  label: PropTypes.string,
  title: PropTypes.string,
  description: PropTypes.string,
};


const FloatingCards = () => (
  <Box sx={sx.floatingCards}>
    <GlassCard
      imageSrc={casbahpic}
      label="MORNING: 09:00"
      title="The Casbah"
      description={`Wander through the heartbeat of Algiers, a\nUNESCO world heritage site.`}
    />
    <GlassCard
      imageSrc={notreDamePic}
      label="AFTERNOON: 15:00"
      title="Notre Dame d'Afrique"
      description={`A spiritual beacon offering the most\nbreathtaking views of the bay.`}
    />
  </Box>
);


const HeroContent = () => {
  const navigate = useNavigate();
  return (
    <Box component="section" sx={sx.container}>
      <Box sx={sx.heading1}>
        <Typography
          variant="inherit"
          variantMapping={{ inherit: "h1" }}
          sx={sx.titleText}
        >
          <Typography variant="inherit" variantMapping={{ inherit: "span" }}>
            One Day.
            <br />
          </Typography>
          <Typography
            variant="inherit"
            variantMapping={{ inherit: "span" }}
            sx={sx.infiniteAlgiers}
          >
            Infinite Algiers.
          </Typography>
        </Typography>
      </Box>

      <Box sx={sx.descriptionBox}>
        <Box sx={sx.descriptionText}>
          Your AI-powered guide to discovering the perfect 24 hours in Algeria's
          capital. Experience the blend of long lasting history and Mediterranean
          elegance through a refractive lens.
        </Box>
      </Box>

      <Box sx={sx.buttonRow}>
        <Box 
          sx={sx.primaryButton} 
          onClick={() => navigate("/plan")}
          style={{ cursor: "pointer" }}
        >
          <Box sx={sx.buttonShadow} />
          <Typography
            variant="inherit"
            variantMapping={{ inherit: "b" }}
            sx={sx.primaryButtonLabel}
          >
            Start Your Journey
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};


const HeroSection = () => {
  return (
    <>
      <Box sx={sx.heroSection}>
        <Box component="main" sx={sx.mainContainer}>
          <Box component="img" sx={sx.bgImage} alt="" src={heropic} />
          <Box sx={sx.gradient} />
          <HeroContent />
          <FloatingCards />
        </Box>
      </Box>
    </>
  );
};

export default HeroSection;