import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../constants';

const AdminView = () => {
  const [loans, setLoans] = useState([]);
  const [orderBy, setOrderBy] = useState('');
  const [filterBy, setFilterBy] = useState('');
  const [noOfLoans, setNoOfLoans] = useState("");
  const [totalMoney, setTotalMoney] = useState("");
  const [totalPaid, setTotalPaid] = useState("");
  const [filterValue, setFilterValue] = useState('');

  useEffect(() => {
    fetchData();
    fetchstatsData();

  }, []);
  const fetchstatsData = async () => {
    try {
      const response = await axios.get(API_URL + 'loans/loan_stats/get_stats/',
      { headers: {"Authorization" : `Bearer ${localStorage.getItem('access_token')}`}});
      setNoOfLoans(response.data.results.no_of_loans);
      setTotalMoney(response.data.results.total_money);
      setTotalPaid(response.data.results.total_paid);
     
    } catch (error) {
      console.log('Error:', error);
   
    }}


  const fetchData = async () => {
    try {
        const params = {};
      
      if(orderBy)
      params['ordering'] = orderBy;
      if (filterBy && filterValue) {
        
        params[filterBy] = filterValue;
      }
  
      const response = await axios.get(API_URL + '/loans/view_all_data/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
        params: params,
      });
  
      setLoans(response.data);
    } catch (error) {
      console.log('Error:', error);
        
    }
  };
  const handleDownloadCSV = async () => {
    // try {
    //   const response = await axios.get(API_URL + '/loans/view_all_data/csv/', {
    //     headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
    //   });
   
    //   window.open(URL.createObjectURL(new Blob([response.data])), '_blank');
    // } catch (error) {
    //   console.log('Error:', error);
    // }
  const csvURL = API_URL + '/loans/view_all_data/csv/';
  const headers = { Authorization: `Bearer ${localStorage.getItem('access_token')}` };

  // Open the CSV file URL in a new window with headers
  window.open(csvURL, '_blank', 'headers=' + JSON.stringify(headers));
  };
  
  
  
   const handleFilterByChange = (e) => {
      setFilterBy(e.target.value);
      setFilterValue('');
    };
  
    
  
    const handleFilterValueChange = (e) => {
      setFilterValue(e.target.value);
    };
  
    const handleOrderByChange = (event) => {
      setOrderBy(event.target.value);
      fetchData(); // Fetch data after selecting an order by value
    };
  
    return (
      <div>
        <h2>Admin View</h2>
        <div>
  <h2>No. of Loans: {noOfLoans}</h2>
  <h2>Total Money: {totalMoney}</h2>
  <h2>Total Paid: {totalPaid}</h2>
</div>

  
        {/* Filter and Order By */}
        <div>
          <label>Filter By:</label>
          <select value={filterBy} onChange={handleFilterByChange}>
            <option value="">-- Select --</option>
            {/* <option value="business">Business</option>
            <option value="customer">Customer</option> */}
            <option value="no_of_months">No of Months</option>
            <option value="accepted_amount">Accepted Amount</option>
            <option value="total_amount">Total Amount</option>
            <option value="interest_rate">Interest Rate</option>
            {/* <option value="created_at">Created At</option> */}
            </select>
{filterBy && (
  <>
    {filterBy === 'customer' ? (
      <input type="text" value={filterValue} onChange={handleFilterValueChange} />
    ) : filterBy === 'business' ? (
      <input type="text" value={filterValue}  onChange={handleFilterValueChange} />
    ) : filterBy === 'no_of_months' ? (
      <input type="number" value={filterValue}  onChange={handleFilterValueChange} />
    ) : filterBy === 'accepted_amount' ? (
      <input type="number" value={filterValue}  onChange={handleFilterValueChange} />
    ) : filterBy === 'total_amount' ? (
      <input type="number" value={filterValue}  onChange={handleFilterValueChange} />
    ) : filterBy === 'interest_rate' ? (
      <input type="number" value={filterValue}  onChange={handleFilterValueChange} />
    ) : null}
    <button onClick={fetchData}>Apply Filter</button>
  </>
)}

  
          <label>Order By:</label>
          <select value={orderBy} onChange={handleOrderByChange}>
            <option value="">-- Select --</option>
            <option value="business">Business</option>
            <option value="customer">Customer</option>
            <option value="no_of_months">No of Months</option>
            <option value="accepted_amount">Accepted Amount</option>
            <option value="total_amount">Total Amount</option>
            <option value="interest_rate">Interest Rate</option>
          </select>
           
        </div>
  <div>
        {loans.map((loan) => (
          
          <div key={loan.id}>
             <p>
              Customer:{' '}
              <a href={`/viewcustomer/:${loan.customer.id}`}>
                {loan.customer.full_name}
              </a>
            </p>
            <p>Requested Amount: {loan.requested_amount}</p>
            <p>No of Months: {loan.no_of_months}</p>
            <p>Accepted Amount: {loan.accepted_amount}</p>
            <p>Total Amount: {loan.total_amount}</p>
            <p>Business: {loan.business}</p>
            <p>Accepted: {loan.accepted? 'Yes' : 'No'}</p>
            <p>
              Offer PDF:{' '}
              <button onClick={() => window.open(API_URL + loan.offer_pdf)}>View PDF</button>
            </p>
            <hr />
          </div>
          
             
        ))}
      </div>

      {/* Download CSV */}
      <div>
        <button onClick={handleDownloadCSV}>Download CSV</button>
      </div>
    </div>
  );
};

export default AdminView;
