import React, { useMemo , useCallback} from "react";
import { useNavigate } from "react-router-dom";
import { useAuth, useUser } from "@clerk/clerk-react";
import NavBar from "./navBar";
import '../App.css'


const History = () => {
  const { isSignedIn,user,isLoaded} = useUser()
  if(!isLoaded){
    return <>Loading...</>
  }

  const navigate = useNavigate()
    const CheckAuth = useCallback(function () {
        if (!isSignedIn) {
            navigate("/")
        }
    })
  CheckAuth()

  const data = useMemo(function(){
    let files = localStorage.getItem(user.primaryEmailAddress.emailAddress)
    if(!files)
      return []
    return JSON.parse(files)
  },[])

  if(!data){
    return <div></div>
  }
  
  return (
    <div className="w-screen h-screen overflow-auto bg-gray-950">
        <NavBar></NavBar>
        <div className="flex flex-col gap-5 items-start">
        {
          data.map(function(el){
            return (
              <DocumentInfoCard date={el.date} doc={el.doc} ></DocumentInfoCard>
            )
          })
        }
        </div>
      </div>
  );
};


const DocumentInfoCard = ({date,doc}) => {

  return (
      <div className="w-screen border-b border-slate-600   bg-transparent shadow-xl overflow-hidden">
        
        <div className="p-6 flex gap-5 justify-start items-center ">
          
          <div className="flex justify-between items-center gap-2">
            <span className="text-gray-400 font-medium">Date:</span>
            <span className="text-gray-100">{date}</span>
          </div>
          <div className="flex justify-between items-center  gap-2">
            <span className="text-gray-400 font-medium">Category:</span>
            <span className="text-gray-100">{doc.category}</span>
          </div>
          <div className="flex justify-between items-center gap-2">
            <span className="text-gray-400 font-medium">Name:</span>
            <span className="text-gray-100">{doc.name}</span>
          </div>
          <div className="flex justify-between items-center gap-2">
            <span className="text-gray-400 font-medium">Subcategory:</span>
            <span className="text-gray-100">{doc.subcategory}</span>
          </div>
          <div className="flex justify-between items-center gap-2">
            <span className="text-gray-400 font-medium">Type:</span>
            <span className="text-gray-100">{doc.type}</span>
          </div>
          
        </div>
      </div>
  );
};


export default History;
