import React from 'react';
import { Route, Redirect, Navigate } from 'react-router-dom';
 
export const LoggedIn= ({children}) => {
 
   function hasJWT() {
       let flag = false;
 
       //check user has JWT token
       localStorage.getItem('access_token') ? flag=true : flag=false
      
       return flag
   }
 
   if(! hasJWT()) {return <Navigate to='/login' replace />; }
   return children ;
 
};
 
 