import PropTypes from "prop-types";
import { SOCIAL_LINKS } from "../config/socialLinks";
import styles from "./SocialLinks.module.css";

const ICONS_SPRITE = "/icons.svg";

/**
 * SocialLinks — footer / profile row of social platform links.
 */
export default function SocialLinks({ className = "", centered = false, links = SOCIAL_LINKS }) {
  const navClass = [styles.root, centered && styles.centered, className].filter(Boolean).join(" ");

  return (
    <nav className={navClass} aria-label="Social media">
      <ul className={styles.list}>
        {links.map(({ id, label, href, icon }) => (
          <li key={id}>
            <a
              href={href}
              className={styles.link}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={label}
              title={label}
            >
              <svg className={styles.icon} aria-hidden="true">
                <use href={`${ICONS_SPRITE}#${icon}`} />
              </svg>
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

SocialLinks.propTypes = {
  className: PropTypes.string,
  centered: PropTypes.bool,
  links: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      href: PropTypes.string.isRequired,
      icon: PropTypes.string.isRequired,
    })
  ),
};
