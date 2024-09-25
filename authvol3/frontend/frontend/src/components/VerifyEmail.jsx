import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

function VerifyEmail() {
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (otp) {
      setLoading(true);
      try {
        const response = await axios.post("/api/verifyemail", { otp });
        if (response.status === 200) {
          navigate("/login");
          console.log(response.data.message); 
          toast.success(response.data.message)
        } else {
          console.log('Unexpected response status:', response.status);
        }
      } catch (error) {
        if (error.response) {
       
          console.log('Error:', error.response.data.message || 'An unexpected error occurred.');
        } else if (error.request) {

          console.log('No response from server.');
        } else {

          console.log('Request setup error.');
        }
      } finally {
        setLoading(false);
      }
    } else {
      console.log('Please enter the OTP code.');
    }
  }

  return (
    <div className='flex justify-center items-center h-screen bg-indigo-600'>
      {loading ? (
        <div className="flex justify-center items-center">
          <div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-32 w-32"></div>
        </div>
      ) : (
        <div className='w-[600px] p-6 shadow bg-white rounded'>
          <h1>Verify Email</h1>
          <hr className='mt-3' />
          <form onSubmit={handleSubmit}>
            <div className='mt-3'>
              <label htmlFor="otp" className='block text-base mb-2'>Enter your OTP code</label>
              <input
                type="text"
                name="otp"
                className='border w-full outline-none py-2 rounded px-2'
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
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

export default VerifyEmail;
