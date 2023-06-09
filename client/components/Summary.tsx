import React from 'react';
import { ListingData } from '../types/interfaces';

const Summary = (listing: ListingData) => {
  
  return <div>
    <h1>Summary</h1>
    <h2>Amount Payable : </h2>
    {listing.dealer_approved === true ? <h2>ShelterKart Approved</h2> : null}
    <h2>{listing.premium_amount}</h2>
  </div>;
};

export default Summary;

