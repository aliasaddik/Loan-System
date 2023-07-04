import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import axios from 'axios';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { API_URL } from '../constants';

const VerifyUser = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    usercode: '',
    password: '',
    new_password1: '',
    new_password2: ''
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if all required fields are filled
    if (!formData.usercode|| !formData.password|| !formData.new_password1 || !formData.new_password2) {
      setErrors({ error: 'All fields are required' });
      return;
    }

    // Check if new_password1 and new_password2 match
    if (formData.new_password1 !== formData.new_password2) {
      setErrors({ error: 'Passwords do not match' });
      return;
    }

    try {
      // Send POST request
      await axios.post(API_URL+"/auth/verify/", formData);

      // Reset form fields
      setFormData({
        usercode: '',
        password: '',
        new_password1: '',
        new_password2: ''
      });

      // Navigate to the login page
      navigate('/login');
    } catch (error) {
      // Handle errors
     
      const newErrors = {};
      newErrors.error=  error.response.data.message
      console.log(error.response)
      setErrors(newErrors);
      
    }
  };

  return (
    <div>
      <h2>Register User</h2>
      {errors.error && <div className="error">{errors.error}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formUserCode">
          <Form.Label>User Code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter user code"
            name="usercode"
            value={formData.usercode}
            onChange={handleChange}
            required
          />
        </Form.Group>
        <Form.Group controlId="formPassword">
          <Form.Label>Emailed Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="formnew_password1">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter password"
            name="new_password1"
            value={formData.new_password1}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="formnew_password2">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm password"
            name="new_password2"
            value={formData.new_password2}
            onChange={handleChange}
            required
          />
        </Form.Group>

        {Object.keys(errors).map((key) => (
          <div key={key} className="error">
          {errors &&
  Object.keys(errors).map((key) => (
    <div key={key} className="error">
      {Array.isArray(errors[key]) ? (
        errors[key].map((errorMsg) => <div key={errorMsg}>{errorMsg}</div>)
      ) : (
        <div>{errors[key]}</div>
      )}
    </div>
  ))}
          </div>
        ))}


        <Button variant="primary" type="submit">
          Verify
        </Button>
      </Form>
    </div>
  );
};

export default VerifyUser;
