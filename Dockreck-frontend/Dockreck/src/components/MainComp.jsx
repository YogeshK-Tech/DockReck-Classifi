import React, { useState } from "react";
import styles from "../styles/MainComp.module.css";
import { useNavigate } from "react-router-dom";

const MainComp = () => {
  const [dragging, setDragging] = useState(false); // State to handle drag UI
  const [uploadStatus, setUploadStatus] = useState(""); // State for upload status
  const navigate = useNavigate();

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setDragging(false); // Hide the drag message

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const formData = new FormData();
      formData.append("file", files[0]); // Assuming only one file is uploaded

      setUploadStatus("Uploading...");

      try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        console.log("Server response:", result); // Log the backend response
        if (response.ok) {
          setUploadStatus(result.message);
          setTimeout(() => {
            navigate("/classification");
          }, 2000);
        } else {
          setUploadStatus(result.message || "Error uploading file.");
        }
      } catch (error) {
        setUploadStatus("Error uploading file. Please check your connection.");
        console.error(error);
      }
    }
  };

  return (
    <div
      className={styles.container}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div>
        <img
          className={styles.uploadImage}
          src="../src/assets/upload-img.png"
          alt="This is an image"
        />
        <h1 className={styles.heading}>Upload Documents</h1>
        <p className={styles.description}>
          You can easily upload your documents here by clicking on this button
          or just drag and drop.
        </p>
        <div className={styles.buttonContainer}>
          <button type="button" className={styles.primaryButton}>
            Upload Documents
          </button>
        </div>
      </div>

      {/* Drag and drop overlay */}
      {dragging && (
        <div className={styles.dragMessage}>Drop to classify the Documents</div>
      )}

      {/* Upload status message */}
      {uploadStatus && (
        <div className={styles.uploadStatus}>{uploadStatus}</div>
      )}
    </div>
  );
};

export default MainComp;
