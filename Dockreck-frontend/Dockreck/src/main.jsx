import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import App from "./App.jsx";
// Importing bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import MainComp from "./components/MainComp.jsx";
import CategoryComp from "./components/CategoryComp.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/",
        element: <MainComp />,
      },
      {
        path: "/home",
        element: <MainComp />,
      },
      {
        path: "/classification",
        element: <CategoryComp />,
      },
    ],
  },
]);
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
