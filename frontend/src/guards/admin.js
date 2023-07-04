import React from 'react';
import { Route, Redirect, Navigate } from 'react-router-dom';
 
export const Admin= ({children}) => {
 
   function isAdmin() {
       let flag = false;
 
       //check user has JWT token
       localStorage.getItem('access_token') &&   localStorage.getItem('user_type')==="Admin" ? flag=true : flag=false
      
       return flag
   }
 
   if(! isAdmin()) {return <Navigate to='/not-allowed' replace />; }
   return children ;
 
};
 