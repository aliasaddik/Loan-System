import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { API_URL, headers } from '../constants';
import axios from 'axios';

const RegisterCustomer = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    mobile_number: '',
    date_of_birth: '',
    id_front: null,
    id_back: null,
    current_debt_outside: null,
    credit_limit_outside: null,
    credit_history_length: null,
    pursuit_of_new_credit: null,
    months_since_last_late_payment: null,
    credit_mix: null
  });
  const [errors, setErrors] = useState({});
  const[usercode, setUsercode] = useState('')
  const [registered, setRegistered] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateForm = () => {
    let isValid = true;
    const newErrors = {};

    // Validate required fields
    const requiredFields = [
      'first_name',
      'last_name',
      'email',
      'mobile_number',
      'date_of_birth',
      'id_front',
      'id_back',
      'current_debt_outside',
      'credit_limit_outside',
      'credit_history_length',
      'pursuit_of_new_credit',
      'months_since_last_late_payment',
      'credit_mix',
    ];
    requiredFields.forEach((field) => {
      if (!formData[field]) {
        isValid = false;
        newErrors[field] = 'This field is required';
      }
    });

    // Additional validations for specific fields
    if (formData.mobile_number && !/^\+?1?\d{9,15}$/.test(formData.mobile_number)) {
      isValid = false;
      newErrors.mobile_number = 'Enter a valid mobile number';
    }
    if (!formData.email) {
      isValid = false;
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      isValid = false;
      newErrors.email = 'Invalid email address';
    }
    if ((formData.current_debt_outside !== null && isNaN(formData.current_debt_outside) )||formData.current_debt_outside<0) {
      isValid = false;
      newErrors.current_debt_outside = 'Enter a valid number';
    }
    if ((formData.credit_limit_outside !== null && isNaN(formData.credit_limit_outside)) ||formData.current_limit_outside<0) {
      isValid = false;
      newErrors.credit_limit_outside = 'Enter a valid number';
    }
    if ((formData.credit_history_length !== null && isNaN(formData.credit_history_length))|| formData.credit_history_length<0) {
      isValid = false;
      newErrors.credit_history_length = 'Enter a valid number';
    }
    if ((formData.pursuit_of_new_credit !== null && isNaN(formData.pursuit_of_new_credit))|| formData.pursuit_of_new_credit<0) {
      isValid = false;
      newErrors.pursuit_of_new_credit = 'Enter a valid number';
    }
    if ((formData.months_since_last_late_payment !== null && isNaN(formData.months_since_last_late_payment))|| formData.months_since_last_late_payment<-1) {
      isValid = false;
      newErrors.months_since_last_late_payment = 'Enter a valid number';
    }
    if ((formData.credit_mix !== null && isNaN(formData.credit_mix))|| formData.credit_mix<0) {
      isValid = false;
      newErrors.credit_mix = 'Enter a valid number';
    } 

    // Set errors state
    setErrors(newErrors);

    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
     
    if (validateForm()) {
      setIsLoading(true);
      const formDataObj = new FormData();
      formDataObj.append('first_name', formData.first_name);
      formDataObj.append('last_name', formData.last_name);
      formDataObj.append('email', formData.email);
      formDataObj.append('mobile_number', formData.mobile_number);
      formDataObj.append('date_of_birth', formData.date_of_birth);
      formDataObj.append('id_front', formData.id_front);
      formDataObj.append('id_back', formData.id_back);
      formDataObj.append('current_debt_outside', formData.current_debt_outside);
      formDataObj.append('credit_limit_outside', formData.credit_limit_outside);
      formDataObj.append('credit_history_length', formData.credit_history_length);
      formDataObj.append('pursuit_of_new_credit', formData.pursuit_of_new_credit);
      formDataObj.append('months_since_last_late_payment', formData.months_since_last_late_payment);
      formDataObj.append('credit_mix', formData.credit_mix);

      try {
        const response  = await axios.post(
          API_URL + '/auth/onboard/',
          formDataObj,
          {  'Content-Type': 'multipart/form-data', headers: {"Authorization" : `Bearer ${localStorage.getItem('access_token')}`}}) 
          console.log(response.data.results.usercode+"response")
          console.log(response.data.results.results+"response")
          setRegistered (true);
          setUsercode(response.data.results.usercode);  
          setIsLoading(false);
         
      
          

        // // Reset form fields
        // setFormData({
        //   first_name: '',
        //   last_name: '',
        //   email: '',
        //   mobile_number: '',
        //   date_of_birth: '',
        //   id_front: null,
        //   id_back: null,
        //   current_debt_outside: null,
        //   credit_limit_outside: null,
        //   credit_history_length: null,
        //   pursuit_of_new_credit: null,
        //   months_since_last_late_payment: null,
        //   credit_mix: null,
        // });
        // setErrors({});
       
       
       
        
      } catch (error) {

        const newErrors = {};
        newErrors.error = error.response.data.message;
        console.log(formData)
        console.log(error.response.data.error)
        setErrors(newErrors);
      } finally {
        
        setIsLoading(false);
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };
  const handleClick =()=>{
  window.location.href = '/loans/create';
}
  return (
  <div>
      <h2>Register Customer</h2>
      {!registered ? ( <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formFirstName">
          <Form.Label>First Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter first name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            isInvalid={!!errors.first_name}
          />
          {errors.first_name && <Form.Control.Feedback type="invalid">{errors.first_name}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formLasttName">
          <Form.Label>Last Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter last name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            isInvalid={!!errors.last_name}
          />
          {errors.last_name && <Form.Control.Feedback type="invalid">{errors.last_name}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formEmail">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter user email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            isInvalid={!!errors.email}
          />
          {errors.email && <Form.Control.Feedback type="invalid">{errors.email}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formMobileNumber">
          <Form.Label>Mobile Number</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter mobile number"
            name="mobile_number"
            value={formData.mobile_number}
            onChange={handleChange}
            isInvalid={!!errors.mobile_number}
          />
          {errors.mobile_number && <Form.Control.Feedback type="invalid">{errors.mobile_number}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formDateOfBirth">
          <Form.Label>Date of Birth</Form.Label>
          <Form.Control
            type="date"
            placeholder="Enter date of birth"
            name="date_of_birth"
            value={formData.date_of_birth}
            onChange={handleChange}
            isInvalid={!!errors.date_of_birth}
          />
          {errors.date_of_birth && <Form.Control.Feedback type="invalid">{errors.date_of_birth}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formIdFront">
          <Form.Label>ID Front</Form.Label>
          <Form.Control
            type="file"
            name="id_front"
            onChange={handleChange}
            isInvalid={!!errors.id_front}
          />
          {errors.id_front && <Form.Control.Feedback type="invalid">{errors.id_front}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formIdBack">
          <Form.Label>ID Back</Form.Label>
          <Form.Control
            type="file"
            name="id_back"
            onChange={handleChange}
            isInvalid={!!errors.id_back}
          />
          {errors.id_back && <Form.Control.Feedback type="invalid">{errors.id_back}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formCurrentDebtOutside">
          <Form.Label>Current Debt Outside</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter current debt outside"
            name="current_debt_outside"
            value={formData.current_debt_outside}
            onChange={handleChange}
            isInvalid={!!errors.current_debt_outside}
          />
          {errors.current_debt_outside && <Form.Control.Feedback type="invalid">{errors.current_debt_outside}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formCreditLimitOutside">
          <Form.Label>Credit Limit Outside</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter credit limit outside"
            name="credit_limit_outside"
            value={formData.credit_limit_outside}
            onChange={handleChange}
            isInvalid={!!errors.credit_limit_outside}
          />
          {errors.credit_limit_outside && <Form.Control.Feedback type="invalid">{errors.credit_limit_outside}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formCreditHistoryLength">
          <Form.Label>Credit History Length</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter credit history length"
            name="credit_history_length"
            value={formData.credit_history_length}
            onChange={handleChange}
            isInvalid={!!errors.credit_history_length}
          />
          {errors.credit_history_length && <Form.Control.Feedback type="invalid">{errors.credit_history_length}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formPursuitOfNewCredit">
          <Form.Label>Pursuit of New Credit</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter pursuit of new credit"
            name="pursuit_of_new_credit"
            value={formData.pursuit_of_new_credit}
            onChange={handleChange}
            isInvalid={!!errors.pursuit_of_new_credit}
          />
          {errors.pursuit_of_new_credit && <Form.Control.Feedback type="invalid">{errors.pursuit_of_new_credit}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formMonthsSinceLastLatePayment">
          <Form.Label>Months Since Last Late Payment</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter months since last late payment"
            name="months_since_last_late_payment"
            value={formData.months_since_last_late_payment}
            onChange={handleChange}
            isInvalid={!!errors.months_since_last_late_payment}
          />
          {errors.months_since_last_late_payment && <Form.Control.Feedback type="invalid">{errors.months_since_last_late_payment}</Form.Control.Feedback>}
        </Form.Group>
        <Form.Group controlId="formCreditMix">
          <Form.Label>Credit Mix</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter credit mix"
            name="credit_mix"
            value={formData.credit_mix}
            onChange={handleChange}
            isInvalid={!!errors.credit_mix}
          />
          {errors.credit_mix && <Form.Control.Feedback type="invalid">{errors.credit_mix}</Form.Control.Feedback>}
        </Form.Group>
         <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Submit'}
          </Button>
      </Form>):
      ( <div><p>The usercode is {usercode} now you can create a loan for this customer </p>
       <Button  variant="primary" type="submit"  onClick={() => handleClick()}>Create Loan </Button></div>) }
     
      {errors.error && <p>{errors.error}</p>}
    </div>
  );
};

export default RegisterCustomer;
