import React, { useState, useRef } from "react";
import styles from "../styles/MainComp.module.css";
import { useNavigate } from "react-router-dom";

const MainComp = () => {
  const [dragging, setDragging] = useState(false); // State to handle drag UI
  const [uploadStatus, setUploadStatus] = useState(""); // State for upload status
  const navigate = useNavigate();
  const fileInputRef = useRef(null); // Ref to the file input element

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
      await uploadFile(files[0]);
    }
  };

  const handleFileSelect = async (e) => {
    const file = e.target.files[0]; // Get the selected file
    if (file) {
      await uploadFile(file);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current.click(); // Trigger file input click
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file); // Assuming only one file is uploaded

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
          <button
            type="button"
            className={styles.primaryButton}
            onClick={handleButtonClick}
          >
            Upload Documents
          </button>
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: "none" }} // Hidden input element
            onChange={handleFileSelect}
          />
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
