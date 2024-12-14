import React, { useState, useRef, useEffect } from "react";
import styles from "../styles/MainComp.module.css";
import { useNavigate } from "react-router-dom";
import '../App.css'

const MainComp = () => {
  const [dragging, setDragging] = useState(false); // State to handle drag UI
  const [uploadStatus, setUploadStatus] = useState(""); // State for upload status
  const navigate = useNavigate();
  const fileInputRef = useRef(null); // Ref to the file input element

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/initial_run", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Backend Response:", data);
        } else {
          const error = await response.json();
          console.error("Error:", error);
        }
      } catch (error) {
        console.error("Fetch Error:", error);
      }
    };

    fetchData();
  }, []); // Runs only once when the component mounts

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
    console.log(e.dataTransfer.files)
    const files = Array.from(e.dataTransfer.files); // Convert FileList to an array
    if (files.length > 0) {
      await uploadFiles(files); // Call bulk upload handler
    }
  };

  const handleFileSelect = async (e) => {
    const files = Array.from(e.target.files); // Convert FileList to an array
    if (files.length > 0) {
      await uploadFiles(files); // Call bulk upload handler
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current.click(); // Trigger file input click
  };

  const uploadFiles = async (files) => {
    setUploadStatus(`Uploading ${files.length} file(s)...`);

    try {
      const uploadPromises = files.map(async (file) => {
        const formData = new FormData();
        formData.append("file", file); // Add the file to the FormData object

        const response = await fetch("http://127.0.0.1:5000/upload", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.message || "Error uploading a file.");
        }
        return result.message; // Return success message for this file
      });

      const results = await Promise.all(uploadPromises); // Wait for all uploads
      setUploadStatus(`All files uploaded successfully: ${results.join(", ")}`);
      setTimeout(() => {
        navigate("/classification");
      }, 2000);
    } catch (error) {
      setUploadStatus("Error uploading one or more files. Please try again.");
      console.error(error);
    }
  };

  return (
    <div
      className={`bg-slate-950 text-center h-screen`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="pl-5 pr-5 pt-10 flex flex-col items-center gap-3">

        <img src="../src/assets/upload-img.png" className="w-[100px] h-[100px]" alt="" />
        
        <h1 className='text-white text-[3rem] font-bold'>Upload Documents</h1>
        <p className={styles.description}>
          You can easily upload your documents here by clicking on this button
          or just drag and drop.
        </p>
        <div className={styles.buttonContainer}>
          <button
            type="button"
            className="text-white bg-violet-950 p-3 pl-5 pr-5 rounded-full"
            onClick={handleButtonClick}
          >
            Browse
          </button>
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: "none" }} // Hidden input element
            onChange={handleFileSelect}
            multiple // Allow multiple files selection
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
