import { useState } from 'react'
import './index.css'
import { ToastContainer } from 'react-toastify'
import "react-toastify/dist/ReactToastify.css"
import { BrowserRouter as Router,Routes,Route } from 'react-router-dom'
import Signup from './components/Signup'
import Login from './components/Login'
import Profile from './components/Profile'
import VerifyEmail from './components/VerifyEmail'
import ForgetPassword from './components/ForgetPassword'
import Index from './components/Index'


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
     <Router>
      <ToastContainer/>
        <Routes>
          <Route path='/' element={<Signup/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/dashboard' element={<Profile/>}/>
          <Route path='/otp/verify' element={<VerifyEmail/>}/>
          <Route path='/forget_password' element={<ForgetPassword/>}/>
        </Routes>
     </Router>
    </>
  )
}

export default App
