import React from "react";
import styles from "../styles/NavBar.module.css"; // Import the CSS Module

const NavBar = () => {
  return (
    <div>
      <header
        className={`d-flex flex-wrap py-3 mb-4 border-bottom ${styles.header}`}
      >
        <a
          href="/"
          className={`d-flex align-items-center mb-3 mb-md-0 me-md-auto text-decoration-none ${styles.logo}`}
        >
          <span className="fs-4">DocReck</span>
        </a>

        <ul className={`nav nav-pills ${styles.nav}`}>
          <li className="nav-item">
            <a
              href="#"
              className={`nav-link active ${styles.navLinkActive}`}
              aria-current="page"
            >
              Home
            </a>
          </li>
          <li className="nav-item">
            <a href="#" className={`nav-link ${styles.navLink}`}>
              Uploads
            </a>
          </li>
          <li className="nav-item">
            <a href="#" className={`nav-link ${styles.navLink}`}>
              History
            </a>
          </li>
          <li className="nav-item">
            <a href="#" className={`nav-link ${styles.navLink}`}>
              About
            </a>
          </li>
        </ul>
      </header>
    </div>
  );
};

export default NavBar;
