import './App.css';
import {BrowserRouter,Routes, Route,useMatch} from 'react-router-dom'
import {NotAllowed} from "./components/notAllowed";
import {Login} from "./components/login";
import { MyNavbar } from './components/navbar';
import RegisterCustomer from './components/register';
import VerifyUser from './components/verifyEmail';
import CreateLoan from './components/createLoan';
import ViewLoans from './components/viewLoans';
import ViewInstallments from './components/viewInstallments';
import ViewCustomer from './components/viewCustomer';
import AdminView from './components/adminView';
import { Admin } from './guards/admin';
import { Customer } from './guards/customer';
import { Merchant } from './guards/merchant';
import Logout from './components/logout';
 
 
 
 function App() {
    
      
    return <BrowserRouter>
      <MyNavbar/>
     <Routes>
     <Route path="/login" element={<Login/>}/>
     </Routes>
    
   
     <Routes>
     <Route path="/not-allowed" element = {<NotAllowed/>}/>
     <Route path="/onboard" element = {<Merchant><RegisterCustomer/></Merchant>} /> 
     <Route path = "/verify" element = {<VerifyUser/>}/>
     <Route path = "/loans/create" element = {<Merchant><CreateLoan/></Merchant>}/>
     <Route path = "/loans/view_all" element = {<Customer><ViewLoans/></Customer>}/>
     <Route path = "/installments/view_all" element = {<Customer><ViewInstallments/></Customer>}/>
     <Route path= "/viewcustomer/:customerId" element = {<Admin><ViewCustomer/></Admin>}/>
     <Route path = "/viewAll" element = {<Admin><AdminView/></Admin>}/>
     <Route path = "/logout" element = {<Logout/> } />
    
</Routes> 

      </BrowserRouter>;
}
export default App;