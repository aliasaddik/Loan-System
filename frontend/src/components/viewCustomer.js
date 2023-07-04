import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../constants';
import { useParams } from 'react-router-dom';
import Card from 'react-bootstrap/Card';

const ViewCustomer = ( ) => {
  const [customerData, setCustomerData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { customerId } = useParams();
  useEffect(() => {
    const fetchCustomerData = async () => {
      try {
        const response = await axios.get(API_URL + 'customers/' + customerId + '/',
        { headers: {"Authorization" : `Bearer ${localStorage.getItem('access_token')}`}});
        setCustomerData(response.data.results);
        setLoading(false);
      } catch (error) {
        setError('Error fetching customer data.');
        setLoading(false);
      }
    };

    fetchCustomerData();
  }, [customerId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      {customerData && (
        <Card>
          <Card.Body>
            <Card.Title>Customer Details</Card.Title>
            <Card.Text>
              <p>First Name: {customerData.first_name}</p>
              <p>Last Name: {customerData.last_name}</p>
              <p>Email: {customerData.email}</p>
              <p>Mobile Number: {customerData.mobile_number}</p>
              <p>Date of Birth: {customerData.date_of_birth}</p>
              <p>Current Debt Outside: {customerData.current_debt_outside}</p>
              <p>Credit Limit Outside: {customerData.credit_limit_outside}</p>
              {/* Add more customer fields as needed */}
            </Card.Text>
          </Card.Body>
        </Card>
      )}

      <div>
        <Card>
          <Card.Body>
            <Card.Title>ID Front</Card.Title>
            {customerData && customerData.id_front && (
              <img src={API_URL + customerData.id_front} alt="ID Front" style={{ maxWidth: '200px' }} />
            )}
          </Card.Body>
        </Card>
      </div>

      <div>
        <Card>
          <Card.Body>
            <Card.Title>ID Back</Card.Title>
            {customerData && customerData.id_back && (
              <img src={API_URL + customerData.id_back} alt="ID Back" style={{ maxWidth: '200px' }} />
            )}
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

export default ViewCustomer;