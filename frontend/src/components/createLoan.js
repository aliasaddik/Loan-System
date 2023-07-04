import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import axios from 'axios';
import { API_URL} from '../constants';

const CreateLoan = () => {
  const [formData, setFormData] = useState({
    requested_amount: '',
    customer: '',
    no_of_months: ''
  });
  const [errors, setErrors] = useState({});
  const [loanCreated, setLoanCreated] = useState(false);

  const validateForm = () => {
    let isValid = true;
    const newErrors = {};

    // Validate requested_amount field
    if (!formData.requested_amount || formData.requested_amount <= 0) {
      newErrors.requested_amount = 'Requested amount must be a positive number';
      isValid = false;
    }

    // Validate customer field
    if (!formData.customer) {
      newErrors.customer = 'Customer email is required';
      isValid = false;
    } else if (!validateEmail(formData.customer)) {
      newErrors.customer = 'Invalid customer email';
      isValid = false;
    }

    // Validate no_of_months field
    if (!formData.no_of_months || formData.no_of_months <= 0) {
      newErrors.no_of_months = 'Number of months must be a positive number';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      try {
        // Send POST request
        await axios.post(API_URL+"/loans/create/" , formData,
        { headers: {"Authorization" : `Bearer ${localStorage.getItem('access_token')}`} 
    });

        // Reset form fields
        setFormData({
          requested_amount: '',
          customer: '',
          no_of_months: ''
        });

        // Set loanCreated flag to show success message
        setLoanCreated(true);
      } catch (error) {
        const newErrors = {};
        newErrors.error =  error.response.data.message
        console.log(error.response)
        setErrors(newErrors);
        // Handle error case here
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value
    }));
  };

  return (
    <div>
      <h2>Create Loan</h2>
      {loanCreated ? (
        <div>
          <p>Loan created successfully!</p>
        </div>
      ) : (
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formRequestedAmount">
            <Form.Label>Requested Amount</Form.Label>
            <Form.Control
              type="number"
              placeholder="Enter requested amount"
              name="requested_amount"
              value={formData.requested_amount}
              onChange={handleChange}
              isInvalid={!!errors.requested_amount}
            />
            <Form.Control.Feedback type="invalid">{errors.requested_amount}</Form.Control.Feedback>
          </Form.Group>

          <Form.Group controlId="formCustomer">
            <Form.Label>Customer Email</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter customer email"
              name="customer"
              value={formData.customer}
              onChange={handleChange}
              isInvalid={!!errors.customer}
            />
            <Form.Control.Feedback type="invalid">{errors.customer}</Form.Control.Feedback>
          </Form.Group>

          <Form.Group controlId="formNoOfMonths">
            <Form.Label>Number of Months</Form.Label>
            <Form.Control
              type="number"
              placeholder="Enter number of months"
              name="no_of_months"
              value={formData.no_of_months}
              onChange={handleChange}
              isInvalid={!!errors.no_of_months}
            />
            <Form.Control.Feedback type="invalid">{errors.no_of_months}</Form.Control.Feedback>
          </Form.Group>

          <Button variant="primary" type="submit">
            Create Loan
          </Button>
        </Form>
      )}
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

    </div>
  );
};

export default CreateLoan;
