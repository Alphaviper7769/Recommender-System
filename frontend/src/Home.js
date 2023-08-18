import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
  const purchaseHandler = async () => {
    // await axios.post(process.env.REACT_APP_BACKEND + '/purchase', props);
  };

  const { img, name, price, tag } = props.props;

  return (
    <div className='prods'>
      <img src={props.img} className='prods-img' alt='img' />
      <div className='prod-body'>
        <h2>{name}</h2>
        <p>{price}</p>
        <p>{tag}</p>
      </div>
      <div className='buttons'>
        <button onClick={purchaseHandler}>Purchase</button>
      </div>
    </div>
  );
};


function Home() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([
    {
      img: '',
      name: 'laptop',
      price: 'Rs 20000',
      tag: 'Electronics'
    },
    {
      img: '',
      name: 'laptop',
      price: 'Rs 20000',
      tag: 'Electronics'
    },
    {
      img: '',
      name: 'laptop',
      price: 'Rs 20000',
      tag: 'Electronics'
    }
  ]);
    // useEffect(() => {
    //     const get_products = async () => {
    //       let response;
    //       response = await axios.get(process.env.REACT_APP_BACKEND + '/home');
    //       setProducts(response);
    //     };

    //     get_products();
    // }, []);
    const [search, setSearch] = useState('');
    const submitChange = (e) => {
      setSearch(...search, e.target.value);
    };
    const searchSubmit = async (e) => {
      e.preventDefault();
      // submit tags
      // axios.post(process.env.REACT_APP_BACKEND + '/search', {
      //   'tag': search
      // });
      navigate('/home');
    };
    return (
      <>
        <form onSubmit={searchSubmit} className='search'>
          <input type='text' name='search' value={search} onChange={submitChange} />
          <button type='submit'>Search</button>
        </form>
        {products.length > 0 && <div className="home">
        {products.length > 0 && products.map((product) => {
            return <Prods props={product} />;
        })}
        </div>}
      </>
    );
}

export default Home;
