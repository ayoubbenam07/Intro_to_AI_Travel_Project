import { Typography, Box } from "@mui/material";
import PropTypes from "prop-types";
import styles from "./FooterSection.module.css";
import backgroundImage from "./image.png";
import { Link } from "react-router-dom";

const FooterSection = ({ className = "" }) => {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

  const handleSignOut = (e) => {
    e.preventDefault();
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("userEmail");
    window.location.href = "/";
  };

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
            sx={{ 
              fontWeight: "500", 
              lineHeight: { xs: "2.5rem", sm: "3.5rem" },
              fontSize: { xs: "2.5rem", sm: "3.5rem" } 
            }}
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
            <Link to="/" className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>Home</Link>
          </Box>
          <Box className={styles.item}>
            <Link to="/itinerary" className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>Itinerary</Link>
          </Box>
          <Box className={styles.item}>
            <Link to="/plan" className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>Plan Journey</Link>
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
            Explorer
          </Typography>
        </Box>
        <Box className={styles.list}>
          {isLoggedIn ? (
            <>
              <Box className={styles.item}>
                <Link to="/profile" className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>My Profile</Link>
              </Box>
              <Box className={styles.item}>
                <a href="#" onClick={handleSignOut} className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>Sign Out</a>
              </Box>
            </>
          ) : (
            <>
              <Box className={styles.item}>
                <Link to="/login" className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>Sign In</Link>
              </Box>
              <Box className={styles.item}>
                <Link to="/register" className={styles.theSpiritOf} style={{ textDecoration: 'none', color: 'inherit' }}>Create Account</Link>
              </Box>
            </>
          )}
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
