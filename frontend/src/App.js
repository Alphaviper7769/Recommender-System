import './App.css';
import { 
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate
 } from 'react-router-dom';

import Home from './Home';
import Login from './Login';
import Head from './Head';

const App = () => {
  return (
    <div className='App'>
      <Head />
      <Router>
        <Routes>
          <Route path='/' exact element={<Login />} />
          <Route path='/home' exact element={<Home />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;