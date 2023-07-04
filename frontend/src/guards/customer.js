import React from 'react';
import { Route, Redirect, Navigate } from 'react-router-dom';
 
export const Customer= ({children}) => {
 
   function isCustomer() {
       let flag = false;
 
       //check user has JWT token
       localStorage.getItem('access_token') &&   localStorage.getItem('user_type')==="Customer" ? flag=true : flag=false
      
       return flag
   }
 
   if(! isCustomer()) {return <Navigate to='/not-allowed' replace />; }
   return children ;
 
};
 