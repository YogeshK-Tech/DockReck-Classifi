import { useState } from "react";
import styles from "../styles/NavBar.module.css"; // Import the CSS Module

const NavBar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div>
      <header
        className={`d-flex flex-wrap py-3 mb-4 border-bottom ${styles.header}`}
      >
        <a
          href="/"
          className={`d-flex align-items-center mb-3 mb-md-0 me-md-auto text-decoration-none ${styles.logo}`}
        >
          <span className={styles.logoText}>DocReck</span>
        </a>

        <button
          className={styles.toggleButton}
          onClick={toggleMobileMenu}
          aria-label="Toggle navigation"
        >
          ☰
        </button>

        <ul
          className={`${styles.nav} ${
            isMobileMenuOpen ? styles.navOpen : ""
          }`}
        >
          <li className={`nav-item ${styles.navItem}`}>
            <a href="#" className={styles.navLink}>
              Home
            </a>
          </li>
          <li className={`nav-item ${styles.navItem}`}>
            <a href="#" className={styles.navLink}>
              Uploads
            </a>
          </li>
          <li className={`nav-item ${styles.navItem}`}>
            <a href="#" className={styles.navLink}>
              History
            </a>
          </li>
          <li className={`nav-item ${styles.navItem}`}>
            <a href="#" className={styles.navLink}>
              About
            </a>
          </li>
        </ul>
      </header>
    </div>
  );
};

export default NavBar;
