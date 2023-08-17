import axios from 'axios';
import React, { useState, useEffect } from 'react';

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
  const purchaseHandler = async (product) => {
    await axios.post(process.env.REACT_APP_BACKEND + '/purchase', product);
  };

  return (
    <div className='prods'>
      <img src={props.img} className='prods-img' alt='img' />
      <h2>{props.name}</h2>
      <p>{props.price}</p>
      <div className='buttons'>
        <button onClick={purchaseHandler.call(props)}>Purchase</button>
      </div>
    </div>
  );
};


function Home() {
    const [products, setProducts] = useState([]);
    useEffect(() => {
        const get_products = async () => {
          let response;
          response = await axios.get(process.env.REACT_APP_BACKEND + '/home');
          setProducts(response);
        };

        get_products();
    }, []);
    return (
      <>
        {products.length > 0 && <div className="home">
        {products.map((product) => {
            <Prods props={product} />
        })}
        </div>}
      </>
    );
}

export default Home;
