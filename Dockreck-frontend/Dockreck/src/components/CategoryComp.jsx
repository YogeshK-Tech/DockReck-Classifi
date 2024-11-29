import React, { useState, useEffect } from "react";
import styles from "../styles/CategoryComp.module.css";

const CategoryComp = () => {
  const [classifiedDocs, setClassifiedDocs] = useState([]); // State for documents
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [saving, setSaving] = useState(null); // Tracks which document is being saved

  useEffect(() => {
    // Fetch classified documents from the backend
    const fetchClassifiedDocs = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/get_classified_docs"
        );
        if (!response.ok) {
          throw new Error("Failed to fetch classified documents.");
        }
        const data = await response.json();
        setClassifiedDocs(data.docs);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchClassifiedDocs();
  }, []);

  const handleLabelEdit = (index, field, value) => {
    // Ensure value is not empty or invalid
    if (!value.trim()) {
      alert("Category/Subcategory cannot be empty.");
      return;
    }
    // Update the label locally
    const updatedDocs = [...classifiedDocs];
    updatedDocs[index][field] = value.trim();
    setClassifiedDocs(updatedDocs);
  };

  const handleSave = async (doc, index) => {
    setSaving(index); // Set saving state for the current document
    try {
      const response = await fetch("http://127.0.0.1:5000/update_label", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(doc),
      });
      if (!response.ok) {
        throw new Error("Failed to update label.");
      }
      alert("Labels updated successfully!");
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      setSaving(null); // Reset saving state
    }
  };

  const handleSaveToLibrary = async () => {
    fetch("http://127.0.0.1:5000/save_todrive", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        /* relevant data */
      }),
    })
      .then((response) => response.json())
      .then((data) => console.log("Success:", data))
      .catch((error) => console.error("Error:", error));
  };

  if (loading) {
    return <div className={styles.listContainer}>Loading documents...</div>;
  }

  if (error) {
    return <div className={styles.listContainer}>Error: {error}</div>;
  }

  return (
    <div className={styles.listContainer}>
      <div>
        <h1>Classification Complete</h1>
        <h2>
          Here are your documents with their categories and subcategories.
        </h2>
        <h3>Click to open a document or edit labels by clicking on them.</h3>
      </div>
      <ol className="list-group list-group-numbered">
        {classifiedDocs.map((doc, index) => (
          <li
            key={index}
            className={`list-group-item d-flex justify-content-between align-items-start ${styles.listItem}`}
          >
            <div className="ms-2 me-auto">
              <div
                className={`fw-bold ${styles.documentName}`}
                tabIndex={0} // Makes the document name keyboard navigable
                role="button"
                onClick={() => window.open(doc.url, "_blank")} // Assuming `doc.url` contains the document's link
                aria-label={`Open ${doc.name}`}
              >
                {doc.name}
              </div>
              This is a {doc.type} document.
            </div>
            <span
              className={`${styles.badgeCustom1} badge`}
              contentEditable
              suppressContentEditableWarning
              onBlur={(e) =>
                handleLabelEdit(index, "category", e.target.innerText)
              }
              aria-label="Edit category"
            >
              {doc.category}
            </span>
            <span
              className={`${styles.badgeCustom2} badge`}
              contentEditable
              suppressContentEditableWarning
              onBlur={(e) =>
                handleLabelEdit(index, "subcategory", e.target.innerText)
              }
              aria-label="Edit subcategory"
            >
              {doc.subcategory}
            </span>
            <button
              onClick={() => handleSave(doc, index)}
              className={`btn btn-sm ${
                saving === index ? "btn-secondary" : "btn-primary"
              } ${styles.saveButton}`}
              disabled={saving === index} // Disable the button while saving
            >
              {saving === index ? "Saving..." : "Save"}
            </button>
          </li>
        ))}
      </ol>
      <div className={styles.buttonContainer}>
        <button
          type="button"
          className={styles.primaryButton}
          onClick={handleSaveToLibrary}
        >
          Save to Library
        </button>
      </div>
    </div>
  );
};

export default CategoryComp;
