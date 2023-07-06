import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useEffect, useState } from 'react';
 

export const MyNavbar =() =>{
  const [isLoggedInCustomer, setIsLoggedInCustomer] = useState(false);
  const [isLoggedInAdmin, setIsLoggedInAdmin] = useState(false);
  const [isLoggedInMerchant, setIsLoggedInMerchant] = useState(false);

  useEffect(() => {
    const userType = localStorage.getItem('user_type');
    setIsLoggedInCustomer(userType === 'Customer');
    setIsLoggedInAdmin(userType === 'Admin');
    setIsLoggedInMerchant(userType === 'Merchant');
 
  }, []);
    
  return (
    <div>
      {   }
{isLoggedInAdmin && <Navbar bg="dark" data-bs-theme="dark">
  <Container>
  <Navbar.Brand>Admin Navbar</Navbar.Brand>
        <Nav className="me-auto">
            <Nav.Link href="/viewAll">View All</Nav.Link>
            <Nav.Link href="/logout">Logout</Nav.Link>
            
              
          </Nav>
        
      </Container>
      </Navbar>}
   
      {isLoggedInMerchant && <Navbar bg="dark" data-bs-theme="dark">
  <Container>
  <Navbar.Brand>Merchant Navbar</Navbar.Brand>
        <Nav className="me-auto">
            <Nav.Link href="/onboard">Onboard a new customer</Nav.Link>
            <Nav.Link href="/loans/create">Create an offer</Nav.Link>
            <Nav.Link href="/logout">Logout</Nav.Link>
              
          </Nav>
        
      </Container>
      </Navbar>}
      {isLoggedInCustomer && <Navbar bg="dark" data-bs-theme="dark">
  <Container>
  <Navbar.Brand>Customer Navbar</Navbar.Brand>
        <Nav className="me-auto">
            <Nav.Link href="/loans/view_all">view loans and offers</Nav.Link>
            <Nav.Link href="/installments/view_all">installmnets</Nav.Link>
            <Nav.Link href="/logout">Logout</Nav.Link>
              
          </Nav>
        
      </Container>
      </Navbar>}
      </div> );
}

 