import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { API_URL } from '../constants';

const ViewLoans = () => {
  const [loans, setLoans] = useState([]);

  useEffect(() => {
    getLoans();
  }, []);

  const getLoans = async () => {
    try {
      const response = await axios.get(API_URL + 'loans/get_all/', {
        headers: { "Authorization": `Bearer ${localStorage.getItem('access_token')}` }
      });
      setLoans(response.data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const handleViewPDF = (pdfUrl) => {
    window.open(API_URL + pdfUrl);
  };

  const handleAcceptLoan = async (loanId) => {
    try {
      await axios.post(
        API_URL + 'installments/accept_loan/' + loanId + '/',
        null,
        { headers: { "Authorization": `Bearer ${localStorage.getItem('access_token')}` } }
      );
      // Refresh loans after accepting
      getLoans();
    } catch (error) {
      console.log('Error:', error);
    }
  };

  const handleRejectLoan = async (loanId) => {
    try {
      await axios.delete(
        API_URL + 'loans/reject/' + loanId + '/',
        { headers: { "Authorization": `Bearer ${localStorage.getItem('access_token')}` } }
      );
      // Refresh loans after rejecting
      getLoans();
    } catch (error) {
      console.log('Error:', error);
    }
  };

  return (
    <div>
      {loans.length > 0 ? (
        <div>
          {loans.map((loan) => (
            <div key={loan.id}>
              <p>Requested Amount: {loan.requested_amount}</p>
              <p>Customer Email: {loan.customer.email}</p>
              <p>Customer Full Name: {loan.customer.full_name}</p>
              <p>No of Months: {loan.no_of_months}</p>
              <p>Accepted Amount: {loan.accepted_amount}</p>
              <p>Total Amount to be paid: {loan.total_amount}</p>
              <p>Business: {loan.business}</p>
              <p>
                Offer PDF: <button onClick={() => handleViewPDF(loan.offer_pdf)}>View PDF</button>
              </p>
              {loan.accepted === false && (
                <div>
                  <button onClick={() => handleAcceptLoan(loan.id)}>Accept</button>
                  <button onClick={() => handleRejectLoan(loan.id)}>Reject</button>
                </div>
              )}
              <hr />
            </div>
          ))}
        </div>
      ) : (
        <p>No offers are made.</p>
      )}
    </div>
  );
};

export default ViewLoans;
