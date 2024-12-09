# **Dockreck**

Dockreck is a powerful document classification and management tool that leverages AI to categorize documents and organize them into structured folders. With an easy-to-use interface and seamless Google Drive integration, Dockreck simplifies document workflows for users by automating the categorization and organization process. Users can also retrain the model using their input for improved accuracy over time.

---

## **Features**
- **Document Upload and Preview**:
  - Upload documents via drag-and-drop or a file upload button.
  - Preview uploaded files directly within the app.
  
- **Automated Categorization**:
  - Classifies documents into categories and subcategories using AI.
  - Editable categories and subcategories for user-defined organization.

- **Google Drive Integration**:
  - Save documents directly to Google Drive.
  - Automatically organizes files into folders based on categories and subcategories.

- **Model Retraining**:
  - User edits are saved to retrain the AI model for improved classification accuracy.

- **User-Friendly Interface**:
  - Intuitive navigation with the NavBar.
  - Simple routes for seamless user experience.

---

## **Project Structure**

### **Backend**
- **Framework**: Flask
- **Key Files**:
  - `app.py`: Main Flask server file that handles API requests.
  - `classify.py`: Contains logic for categorizing documents.
  - `training.py` and `train_transformer.py`: Scripts for retraining the AI model using updated user data.
  - `extract_text.py`: Extracts text content from uploaded documents for classification.
  - `global_config.py`: Configuration settings for the project.
  - `category_classifier.pkl` and `subcategory_classifier.pkl`: Pre-trained model files for categorization.
  - `credentials.json`: Used for authenticating Google Drive API.
  - `librarymodule.py`: Handles file operations for saving documents to Google Drive.

- **Folders**:
  - **processed**: Stores initial training data for model bootstrapping.
  - **uploads**: Temporarily stores user-uploaded files.
  - **tokens**: Stores session or authentication tokens.

---

### **Frontend**
- **Framework**: ReactJS (with Vite for development and build).
- **Key Files**:
  - `main.jsx`: Defines application routes.
  - `App.jsx`: Main application file rendering components.
  - **Components**:
    - `NavBar.jsx`: Handles navigation between routes.
    - `MainComp.jsx`: Allows users to upload documents.
    - `CategoryComp.jsx`: Displays categorized documents with options to edit and save them.
    - `LibraryComp.jsx`: Manages saved files in Google Drive.
  - **Styling**:
    - Scoped CSS modules for individual components (e.g., `CategoryComp.module.css`).

---

## **Workflow**

1. **Upload Files**:
   - Drag-and-drop or click the upload button in the `MainComp`.
   - Files are stored temporarily in the `uploads` folder.

2. **Categorization**:
   - Files are classified into categories and subcategories using pre-trained models.
   - Users can edit these classifications in `CategoryComp`.

3. **Save to Library**:
   - Edited files are saved to Google Drive in structured folders.

4. **Retraining**:
   - When users save edited categories, the changes are logged and used for retraining the AI models via `training.py`.

---

## **Technologies Used**

### **Frontend**:
- ReactJS
- Vite
- CSS Modules

### **Backend**:
- Flask
- Python Libraries:
  - `sklearn`, `transformers`, and other AI/ML libraries
  - `google-api-python-client` for Google Drive integration

### **Datastores**:
- Pre-trained models stored as `.pkl` files
- Session management via Flask

---

## **Setup and Installation**

### Prerequisites
- Python 3.8 or above
- Node.js (for React frontend)
- pip (Python package manager)

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Dockreck

2. **Backend Setup**:
   ```bash
   cd Dockreck-backend
   pip install -r requirements.txt

3. **Frontend Setup**:
   ```bash
   cd Dockreck-frontend/Dockreck
   npm install

3. **Run the Backend**:
   ```bash
   python app.py

4. **Run the Frontend**:
   ```bash
   npm run dev


## **Usage**

### **Uploading Files**
1. Navigate to the upload section.
2. Drag-and-drop files or use the upload button to upload your documents.
3. Wait for the categorization process to complete automatically.

### **Editing Categories**
1. Navigate to the category view where your categorized documents are displayed.
2. Click on the category or subcategory name to edit them.
3. Save the changes to retrain the AI model for better classification in the future.

### **Saving to Library**
1. After editing categories, click the "Save to Library" button.
2. Your files will be organized and saved into Google Drive, with folders structured by categories and subcategories.

---

## **Contributing**

We welcome contributions! To contribute, follow these steps:

1. **Fork** the repository to your own GitHub account.
2. **Create a new branch** for your feature or bugfix.
3. **Submit a pull request** with a detailed description of the changes you’ve made.

---





