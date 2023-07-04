import React from 'react';
import { Route, Redirect, Navigate } from 'react-router-dom';
 
export const Merchant= ({children}) => {
 
   function isMerchant() {
       let flag = false;
 
       //check user has JWT token
       localStorage.getItem('access_token') &&   localStorage.getItem('user_type')==="Merchant" ? flag=true : flag=false
      
       return flag
   }
 
   if(! isMerchant()) {return <Navigate to='/not-allowed' replace />; }
   return children ;
 
};
 
 