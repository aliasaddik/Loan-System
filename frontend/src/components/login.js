// Import the react JS packages 
import axios from "axios";
import { API_URL } from "../constants";
import {useState} from "react";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';

// Define the Login function.
export const Login = () => {
      
     const [error, setError] = useState(null);
     const [email, setEmail] = useState('');
     const [password, setPassword] = useState('');
    
     const submit = async e => {
          e.preventDefault();
        try {
            const user = {
              email: email,
              password: password,
            };
      
            const { data } = await axios.post(API_URL + '/auth/login/', user);
      
            localStorage.clear();
            localStorage.setItem('access_token', data.results.access_token);
            localStorage.setItem('refresh_token', data.results.refresh_token);
            localStorage.setItem('user_type', data.results.user_type)
            axios.defaults.headers.common['Authorization'] = `Bearer ${data['access_token']}`;
            window.location.href = '/';
          } catch (error) {
            setError(error.message);
            }
        };
 
    return(
        <div className="Auth-form-container">
        <Form  onSubmit={submit}>
        <Form.Group className="mb-3" controlId="formGroupEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email"  onChange={e => setEmail(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGroupPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password"  onChange={e => setPassword(e.target.value)}/>
        </Form.Group>
        <Button variant="primary" type="submit">
        Login
      </Button>
      </Form>
     
{error && (
         <Toast  bg={'danger'}>
         <Toast.Header>
           <img src="holder.js/20x20?text=%20" className="rounded me-2" alt="" />
           <strong className="me-auto">Cannot Login</strong>
        </Toast.Header>
         <Toast.Body> Make sure the credentials you entered are correct.</Toast.Body>
       </Toast>
      )}
     </div>
     )}