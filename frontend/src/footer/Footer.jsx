import { Typography, Box } from "@mui/material";
import PropTypes from "prop-types";
import styles from "./FooterSection.module.css";
import backgroundImage from "./image.png";

const FooterSection = ({ className = "" }) => {
  return (
    <div className={[styles.footerSection, className].join(" ")}>
      <img
        className={styles.ab6axuama6a4ohdfkgkjnw513zoc9yIcon}
        alt=""
        src={backgroundImage}
      />
      <Box className={styles.container}>
        <Box className={styles.item}>
          <Typography
            className={styles.algiersAi}
            variant="inherit"
            variantMapping={{ inherit: "h1" }}
            sx={{ fontWeight: "500", lineHeight: "3.5rem" }}
          >
            Algiers AI
          </Typography>
        </Box>
        <Box className={styles.container3}>
          <div className={styles.theSpiritOf}>
            The spirit of Algiers, digitally refined.
            <br />
            Experience the Mediterranean through
            <br />
            the lens of pure intelligence.
          </div>
        </Box>
      </Box>
      <Box className={styles.container4}>
        <Box className={styles.item}>
          <Typography
            className={styles.discover}
            variant="inherit"
            variantMapping={{ inherit: "h3" }}
            sx={{
              fontWeight: "600",
              lineHeight: "1.75rem",
              letterSpacing: "1px",
            }}
          >
            Discover
          </Typography>
        </Box>
        <Box className={styles.list}>
          <Box className={styles.item}>
            <a href="#" className={styles.theSpiritOf}>The Casbah</a>
          </Box>
          <Box className={styles.item}>
            <a href="#" className={styles.theSpiritOf}>Notre Dame d'Afrique</a>
          </Box>
          <Box className={styles.item}>
            <a href="#" className={styles.theSpiritOf}>Martyrs' Memorial</a>
          </Box>
        </Box>
      </Box>
      <Box className={styles.container5}>
        <Box className={styles.item}>
          <Typography
            className={styles.discover}
            variant="inherit"
            variantMapping={{ inherit: "h3" }}
            sx={{
              fontWeight: "600",
              lineHeight: "1.75rem",
              letterSpacing: "1px",
            }}
          >
            Legal
          </Typography>
        </Box>
        <Box className={styles.list}>
          <Box className={styles.item}>
            <a href="#" className={styles.theSpiritOf}>Privacy</a>
          </Box>
          <Box className={styles.item}>
            <a href="#" className={styles.theSpiritOf}>Terms</a>
          </Box>
        </Box>
      </Box>
      <Box className={styles.margin}>
        <Box className={styles.horizontalborder}>
          <Box className={styles.container6}>
            <div className={styles.ensiaIntroTo}>
              © 2026 ENSIA Intro to AI project - Team 06.
            </div>
          </Box>
        </Box>
      </Box>
    </div>
  );
};

FooterSection.propTypes = {
  className: PropTypes.string,
};

export default FooterSection;
