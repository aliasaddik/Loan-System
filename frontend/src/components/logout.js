import  {  useEffect } from 'react';
const Logout=() => {
   
    useEffect(() => {
        localStorage.clear();
        window.location.href = '/login';
    
      }, []);
}
export default Logout;