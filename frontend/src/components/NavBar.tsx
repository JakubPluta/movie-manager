import React from 'react'
import {Link} from "react-router-dom"
const NavBar = () => {
  return (
      <nav className='flex justify-center my-4 mx-6'>
          <Link className='inline-block p-2 mx-2 bg-stone-500 hover:bg-blue-500 text-white text-center font-semibold w-32 rounded-2xl' to="/">Home</Link>
          <Link className='inline-block p-2 mx-2 bg-stone-500 hover:bg-blue-500 text-white text-center font-semibold w-32 rounded-2xl' to="/admin">Admin</Link>
    </nav>
  )
}

export default NavBar
