import logo from './logo.svg';
import React, { useState, useEffect } from 'react';

var products = []

/*
products ; {
  id: {
    name: ,
    price: ,
    img:
  }
}
*/

const Prods = (props) => {
  const [purchase, setPurchase] = useState(true);
  const purchaseHandler = () => {
    setPurchase(false);
  }
  return (
    <div className='prods'>
      <img src={props.img} className='prods-img' alt='img' />
      <h2>{props.name}</h2>
      <p>{props.price}</p>
      <div className='buttons'>
          {purchase ?
            <button onClick={purchaseHandler}>Purchase</button>
            : <p>Purchased</p>
          }
      </div>
    </div>
  );
};


function Home() {
    useEffect(() => {
        // http request
    }, []);
    return (
        <div className="home">
        {products.map((product) => {
            <Prods props={product} />
        })}
        </div>
    );
}

export default Home;
