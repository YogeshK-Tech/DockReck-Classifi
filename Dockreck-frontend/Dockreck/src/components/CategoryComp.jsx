import React, { useState, useEffect, useCallback } from "react";
import styles from "../styles/CategoryComp.module.css";
import NavBar from "./navBar";
import { useUser,useAuth } from "@clerk/clerk-react";
import { useNavigate } from "react-router-dom";


const CategoryComp = () => {
  const {isSignedIn, user,isLoaded} = useUser()
  if(!isLoaded){
    return <>Loading....</>
  }
  const navigate = useNavigate()
    const CheckAuth = useCallback(function () {
        if (!isSignedIn) {
            navigate("/")
        }
    })
  CheckAuth()
  


  const [classifiedDocs, setClassifiedDocs] = useState([]); // State for documents
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [saving, setSaving] = useState(null); // Tracks which document is being saved
  
  
  function getCurrentDate() {
    const options = { year: 'numeric', month: 'long', day: '2-digit' };
    const currentDate = new Date().toLocaleDateString('en-GB', options); // Format as dd MMMM yyyy
    return currentDate;
  }

  function savetolocal(){
    let obj = [
      {
        doc:classifiedDocs[0],
        date:getCurrentDate()
      }
    ]
    let email = user?.primaryEmailAddress?.emailAddress
    let arr = JSON.parse(localStorage.getItem(email))
    if(arr){
      let value = [...arr,...obj]
      localStorage.setItem(email,JSON.stringify(value))
      }
    else
      localStorage.setItem(email,JSON.stringify(obj))

  }

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

  function addtohistory(){
    savetolocal()
  }
  

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
    try {
      const response = await fetch("http://127.0.0.1:5000/save_todrive", {
        method: "POST",
        credentials: "include",
      });

      if (response.status === 401) {
        const data = await response.json();
        if (data.redirect_url) {
          // Redirect user to OAuth flow
          window.location.href = data.redirect_url;
        }
      } else if (response.ok) {
        const result = await response.json();
        console.log("Files uploaded successfully:", result);
        alert("Files uploaded to Google Drive!");
      } else {
        console.error("Error during save to Drive:", await response.json());
      }
    } catch (error) {
      console.error("Unexpected error:", error);
      alert("An unexpected error occurred.");
    }
  };

  if (loading) {
    return <div className={styles.listContainer}>Loading documents...</div>;
  }

  if (error) {
    return <div className={styles.listContainer}>Error: {error}</div>;
  }

  return (
    <>
      <NavBar>
      </NavBar>

      <div className='bg-slate-950 text-white w-full h-screen flex flex-col items-center text-center'>
        <div className="mt-10">
          <h1 className="text-green-700">Classification Complete</h1>
          <h2 className="mt-5 text-slate-600 text-[1.5rem]">
            Here are your documents with their categories and subcategories.
          </h2>
          <h3  className=" text-slate-600 ">Click to open a document or edit labels by clicking on them.</h3>
        </div>
        <ol className="list-group list-group-numbered mt-5">
          {classifiedDocs.map((doc, index) => (
            <li
              key={index}
              className={` text-center flex justify-between align-items-start gap-5 ${styles.listItem}`}
            >
              <div className="ms-2 me-auto">
                <div
                  className={`fw-bold ${styles.documentName}`}
                  tabIndex={0} // Makes the document name keyboard navigable
                  role="button"
                  onClick={() =>
                    window.open(
                      `http://127.0.0.1:5000/files/${encodeURIComponent(
                        doc.url
                      )}`,
                      "_blank"
                    )
                  }
                  // Assuming `doc.url` contains the document's link
                  aria-label={`Open ${doc.name}`}
                >
                  {doc.name}
                </div>
                This is a {doc.type} document.
              </div>
              <span
                className={`${styles.badgeCustom1} text-center badge`}
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
                className={`btn btn-sm ${saving === index ? "btn-secondary" : "btn-primary"
                  } ${styles.saveButton} bg-violet-700`}
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
            onClick={addtohistory}
          >
            Save to History
          </button>
        </div>
      </div>
    </>
  );
};

export default CategoryComp;
