import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API_URL } from '../constants';

const ViewInstallments = () => {
  const [installments, setInstallments] = useState([]);

  useEffect(() => {
    fetchInstallments();
  }, []);

  const fetchInstallments = async () => {
    try {
      const response = await axios.get(API_URL + 'installments/my_installments/',{ headers: {"Authorization" : `Bearer ${localStorage.getItem('access_token')}`} 
    });
      setInstallments(response.data);
    } catch (error) {
      console.error('Error fetching installments:', error);
    }
  };

  const handlePay = async (installmentId) => {
    try {
      await axios.put(API_URL + 'installments/accept_loan/' + installmentId+'/', null,
       { headers: {"Authorization" : `Bearer ${localStorage.getItem('access_token')}`} 
    });
      fetchInstallments(); // Refresh the list of installments after successful payment
    } catch (error) {
      console.error('Error paying installment:', error);
    }
  };

  return (
    <div>
      {installments.map((installment) => (
        <div key={installment.id}>
          <p>Due Date: {installment.due_date}</p>
          <p>Amount without Interest: {installment.amount_without_interest}</p>
          <p>Original Amount Due: {installment.original_amount_due}</p>
          <p>Amount To Pay:{installment.amount_to_pay}</p>
          <p>Loan from:{installment.loan}</p>
          <p>Paid: {installment.paid ? 'Yes' : 'No'}</p>
          {!installment.paid && (
            <button onClick={() => handlePay(installment.id)}>Pay</button>
          )}
          <hr />
        </div>
      ))}
    </div>
  );
};

export default ViewInstallments;
