import { Typography, Box } from "@mui/material";
import PropTypes from "prop-types";


import beachDinnerPic from "./beach_dinner.png";
import marketTourPic from "./market_tour.png";
import yachtMarinasPic from "./yacht_marinas.png";
import ancientRuinsPic from "./ancient_ruins.png";


const globalStyles = `
  @import url("https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;0,700&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Hanken+Grotesk:ital,wght@0,400;0,600;0,700&display=swap");
  @import url("https://fonts.googleapis.com/icon?family=Material+Icons");

  body {
    margin: 0;
    line-height: normal;
  }

  :root {
    --Second-Colour: #005e97;
    --Second-Colour1: #005e97;
    --Gradient: linear-gradient(0deg, #f9f9f9, rgba(249,249,249,0.1) 38.4%, rgba(249,249,249,0));
    --Gradient1: linear-gradient(0deg, #f9f9f9, rgba(249,249,249,0.1) 38.4%, rgba(249,249,249,0));
    --Title-shadow: drop-shadow(0px 3px 5px rgba(26,28,28,0.5));
    --Title-shadow1: drop-shadow(0px 3px 5px rgba(26,28,28,0.5));
  }
`;



const cardImageSx = {
  alignSelf: "stretch",
  flex: 1,
  position: "relative",
  maxWidth: "100%",
  overflow: "hidden",
  maxHeight: "100%",
  objectFit: "cover",
};

const gradientFullSx = (variant = "large") => ({
  margin: "0 !important",
  position: "absolute",
  width: "100%",
  height: "100%",
  top: 0,
  right: 0,
  bottom: 0,
  left: 0,
  background:
    variant === "large"
      ? "linear-gradient(0deg, var(--Second-Colour), rgba(0,94,151,0) 50%, rgba(0,79,82,0))"
      : "linear-gradient(0deg, var(--Second-Colour), rgba(0,94,151,0) 50%, rgba(0,94,151,0))",
  opacity: 0.8,
});

const tagBadgeSx = {
  backdropFilter: "blur(12px)",
  borderRadius: "9999px",
  backgroundColor: "rgba(121,245,251,0.2)",
  border: "1px solid rgba(255,255,255,0.2)",
  display: "flex",
  alignItems: "flex-start",
  padding: "4px 16px",
};

const cardBaseSx = {
  height: "500px",
  borderRadius: "48px",
  overflow: "hidden",
  display: "flex",
  flexDirection: "column",
  alignItems: "flex-start",
  justifyContent: "center",
  position: "relative",
  isolation: "isolate",
  textAlign: "left",
  fontSize: "12px",
  color: "#fff",
  fontFamily: "Hanken Grotesk",
};



const TagBadge = ({ label }) => (
  <Box sx={tagBadgeSx}>
    <Typography
      variant="inherit"
      variantMapping={{ inherit: "b" }}
      sx={{ lineHeight: "16px", letterSpacing: "1.2px", fontWeight: "700", position: "relative" }}
    >
      {label}
    </Typography>
  </Box>
);



const LargeCard = ({ src }) => (
  <Box
    component="section"
    sx={{ ...cardBaseSx, gridColumn: "1 / span 8", gridRow: 1 }}
  >
    <Box component="img" sx={cardImageSx} loading="lazy" alt="" src={src} />
    <Box sx={gradientFullSx("large")} />
    <Box
      sx={{
        margin: "0 !important",
        position: "absolute",
        width: "calc(100% - 96px)",
        right: "48px",
        bottom: "48px",
        left: "48px",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: "8px",
      }}
    >
      <Box sx={{ ...tagBadgeSx, padding: "4px 15px" }}>
        <Typography
          variant="inherit"
          variantMapping={{ inherit: "b" }}
          sx={{ lineHeight: "16px", letterSpacing: "1.2px", fontWeight: "700", position: "relative" }}
        >
          FINE DINING
        </Typography>
      </Box>
      <Box
        sx={{
          alignSelf: "stretch",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          padding: "3px 0 0",
          fontSize: "48px",
          fontFamily: "EB Garamond",
          "@media (max-width:1050px)": { fontSize: "38px" },
          "@media (max-width:450px)": { fontSize: "29px" },
        }}
      >
        <Box
          component="div"
          sx={{
            alignSelf: "stretch",
            position: "relative",
            lineHeight: "56px",
            fontWeight: "500",
            "@media (max-width:1050px)": { lineHeight: "45px" },
            "@media (max-width:450px)": { lineHeight: "34px" },
          }}
        >
          Gastronomy of the Bay
        </Box>
      </Box>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          maxWidth: "449px",
          fontSize: "16px",
          color: "rgba(255,255,255,0.8)",
          "@media (max-width:450px)": { maxWidth: "100%" },
        }}
      >
        <div style={{ position: "relative", lineHeight: "24px" }}>
          Experience a fusion of French technique and Algerian spices at
          <br />
          sunset.
        </div>
      </Box>
    </Box>
  </Box>
);



const SmallCard1 = ({ src }) => (
  <Box
    component="section"
    sx={{ ...cardBaseSx, gridColumn: "9 / span 4", gridRow: 1 }}
  >
    <Box component="img" sx={cardImageSx} loading="lazy" alt="" src={src} />
    <Box sx={gradientFullSx("small")} />
    <Box
      sx={{
        margin: "0 !important",
        position: "absolute",
        bottom: "48px",
        left: "40px",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: "11px",
      }}
    >
      <TagBadge label="EXCLUSIVE" />
      <Typography
        variant="inherit"
        variantMapping={{ inherit: "h3" }}
        sx={{
          margin: 0,
          position: "relative",
          fontWeight: "600",
          fontSize: "20px",
          lineHeight: "28px",
          letterSpacing: "1px",
          "@media (max-width:450px)": { fontSize: "16px", lineHeight: "22px" },
        }}
      >
        Coastal Yacht Tour
      </Typography>
    </Box>
  </Box>
);



const SmallCard2 = ({ src }) => (
  <Box
    component="section"
    sx={{ ...cardBaseSx, gridColumn: "1 / span 4", gridRow: 2 }}
  >
    <Box component="img" sx={cardImageSx} loading="lazy" alt="" src={src} />
    <Box sx={gradientFullSx("small")} />
    <Box
      sx={{
        margin: "0 !important",
        position: "absolute",
        bottom: "48px",
        left: "40px",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: "11px",
      }}
    >
      <TagBadge label="HISTORY" />
      <div
        style={{
          position: "relative",
          fontSize: "20px",
          letterSpacing: "1px",
          lineHeight: "28px",
          fontWeight: "600",
        }}
      >
        Martyrs' Legacy
      </div>
    </Box>
  </Box>
);



const MediumCard = ({ src }) => (
  <Box
    component="section"
    sx={{ ...cardBaseSx, gridColumn: "5 / span 8", gridRow: 2 }}
  >
    <Box component="img" sx={cardImageSx} loading="lazy" alt="" src={src} />
    <Box sx={gradientFullSx("large")} />
    <Box
      sx={{
        margin: "0 !important",
        position: "absolute",
        bottom: "48px",
        left: "48px",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: "11px",
      }}
    >
      <TagBadge label="CULTURE" />
      <div
        style={{
          position: "relative",
          fontSize: "48px",
          lineHeight: "56px",
          fontWeight: "500",
          fontFamily: "EB Garamond",
        }}
      >
        The Artisans of the Old City
      </div>
    </Box>
  </Box>
);



const ExperienceSection = ({ className = "" }) => (
  <>
    <style>{globalStyles}</style>

    <Box
      className={className}
      sx={{
        width: "100%",
        position: "relative",
        backgroundColor: "#f3f3f4",
        padding: "128px 80px",
        boxSizing: "border-box",
        lineHeight: "normal",
        letterSpacing: "normal",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        "@media (max-width:1050px)": { padding: "96px 40px" },
        "@media (max-width:700px)": { padding: "64px 24px" },
        "@media (max-width:480px)": { padding: "48px 16px" },
      }}
    >

      <Box
        component="main"
        sx={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          gap: "64px",
          maxWidth: "1280px",
          margin: "0 auto",
          "@media (max-width:1200px)": { gap: "32px" },
          "@media (max-width:750px)": { gap: "16px" },
          "@media (max-width:700px)": { gap: "16px" },
        }}
      >

        <Box
          component="section"
          sx={{
            alignSelf: "stretch",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-between",
            gap: "20px",
            maxWidth: "100%",
            textAlign: "left",
            fontSize: "12px",
            color: "var(--Second-Colour1)",
            fontFamily: "Hanken Grotesk",
            "@media (max-width:1200px)": { flexWrap: "wrap" },
          }}
        >

          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-start",
              gap: "16px",
              maxWidth: "672px",
              "@media (max-width:750px)": { maxWidth: "100%" },
            }}
          >
            <Typography
              variant="inherit"
              variantMapping={{ inherit: "b" }}
              sx={{
                position: "relative",
                textTransform: "uppercase",
                lineHeight: "16px",
                letterSpacing: "1.2px",
                fontWeight: "700",
              }}
            >
              SELECTED CURATIONS
            </Typography>
            <Box
              sx={{
                position: "relative",
                fontSize: "48px",
                lineHeight: "60px",
                fontWeight: "500",
                fontFamily: "EB Garamond",
                color: "#1a1c1c",
                "@media (max-width: 900px)": { fontSize: "40px", lineHeight: "50px" },
                "@media (max-width: 480px)": { fontSize: "26px", lineHeight: "34px", wordBreak: "keep-all" },
              }}
            >
              Craft Your Mediterranean Legacy
            </Box>
          </Box>


          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-start",
              padding: "0 24px 0 0",
              boxSizing: "border-box",
              maxWidth: "384px",
              fontSize: "18px",
              color: "#404751",
              "@media (max-width:450px)": { maxWidth: "100%" },
            }}
          >
            <Box sx={{ position: "relative", lineHeight: "32px", "@media (max-width:480px)": { fontSize: "16px", lineHeight: "26px" } }}>
              From the bustling markets to the silent yacht
              <br />
              marinas, our AI designs a day that flows with
              <br />
              your rhythm.
            </Box>
          </Box>
        </Box>


        <Box
          component="main"
          sx={{
            alignSelf: "stretch",
            display: "grid",
            gridTemplateColumns: "repeat(12, 1fr)",
            gridTemplateRows: "repeat(2, 500px)",
            gap: "32px",
            "@media (max-width: 1050px)": {
              display: "flex",
              flexDirection: "column"
            }
          }}
        >
          <LargeCard src={beachDinnerPic} />
          <SmallCard1 src={marketTourPic} />
          <SmallCard2 src={yachtMarinasPic} />
          <MediumCard src={ancientRuinsPic} />
        </Box>
      </Box>
    </Box>
  </>
);

ExperienceSection.propTypes = {
  className: PropTypes.string,
};

export default ExperienceSection;