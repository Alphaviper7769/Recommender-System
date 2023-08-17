import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();
    const [data, setData] = useState({
        userID: '',
        password: ''
    });
    const { userID, password } = data;

    const onSubmitHandler = (e) => {
        e.preventDefault();
        navigate('/home');
    };

    const onChangeHandler = (e) => {
        setData({ ...data, [e.target.name]: e.target.value });
    };

    return (
        <div className='login'>
            <form onSubmit={onSubmitHandler}>
                <div className='field'>
                    <label>UserID</label>
                    <input type='text' onChange={onChangeHandler} name='userID' value={userID} />
                </div>
                <div className='field'>
                    <label>Password</label>
                    <input type='password' onChange={onChangeHandler} name='password' value={password} />
                </div>
                <button type='submit'>LOGIN</button>
            </form>
        </div>
    );
};

export default Login;