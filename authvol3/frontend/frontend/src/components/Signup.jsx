import React, { useState } from 'react'
import axios from "axios"
import { useNavigate } from 'react-router-dom'
import { toast } from "react-toastify";

function Signup() {
  const navigate = useNavigate()
  const [formdata, setFormdata] = useState({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    password2: ""
  })
  const [loading, setLoading] = useState(false); 

  const handleOnChange = (e) => {
    setFormdata({ ...formdata, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { email, first_name, last_name, password, password2 } = formdata;

    if (!email || !first_name || !last_name || !password || !password2) {
      console.log('Please fill in all fields');
    } else {
      setLoading(true);
      try {
        console.log('Submitting form:', formdata);
        const resq = await axios.post("/api/register", formdata);
        const response = resq.data;
        console.log('Response status:', resq.status);

        if (resq.status === 201) {
          console.log('Navigating to /otp/verify');
          navigate("/otp/verify");
          toast.success(response.message);
        } else {
          console.log('Unexpected status code:', resq.status);
        }
      } catch (error) {
        if (error.response && error.response.status === 400) {
          console.log('Error:', error.response.data);
          if (error.response.data.email) {
            console.log('Email error:', error.response.data.email[0]);
          }
        } else {
          console.log('An unexpected error occurred:', error.message);
        }
      } finally {
        setLoading(false);
      }
    }
  };

  const { email, first_name, last_name, password, password2 } = formdata

  return (
    <div className='flex justify-center items-center h-screen bg-indigo-600'>
      {loading ? (
        <div className="flex justify-center items-center">
          <div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-32 w-32"></div>
        </div>
      ) : (
        <div className='w-[500px] p-6 shadow bg-white rounded'>
          <h1>Signup</h1>
          <hr className='mt-3' />
          <form onSubmit={handleSubmit}>
            <div className='mt-3'>
              <label htmlFor="email" className='block text-base mb-2'>Email Address</label>
              <input
                type="text"
                name="email"
                className='border w-full outline-none py-2 rounded'
                value={email}
                onChange={handleOnChange}
              />
            </div>

            <div className='mt-3'>
              <label htmlFor="first_name" className='block text-base mb-2'>First Name</label>
              <input
                type="text"
                name="first_name"
                className='border w-full outline-none py-2 rounded'
                value={first_name}
                onChange={handleOnChange}
              />
            </div>

            <div className='mt-3'>
              <label htmlFor="last_name" className='block text-base mb-2'>Last name</label>
              <input
                type="text"
                name="last_name"
                className='border w-full outline-none py-2 rounded'
                value={last_name}
                onChange={handleOnChange}
              />
            </div>

            <div className='mt-3'>
              <label htmlFor="password" className='block text-base mb-2'>Password</label>
              <input
                type="password"
                name="password"
                className='border w-full outline-none py-2 rounded'
                value={password}
                onChange={handleOnChange}
              />
            </div>

            <div className='mt-3'>
              <label htmlFor="password2" className='block text-base mb-2'>Confirm Password</label>
              <input
                type="password"
                name="password2"
                className='border w-full outline-none py-2 rounded'
                value={password2}
                onChange={handleOnChange}
              />
            </div>

            <div className='mt-3'>
              <button type="submit" className='bg-red-100 w-full py-2 rounded font-semibold'>Submit</button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

export default Signup
