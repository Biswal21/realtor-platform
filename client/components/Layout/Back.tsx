import React from 'react'
import { NextRouter } from 'next/router'

const Back:React.FC<{router: NextRouter}> = ({router}) => {
  return (
    
    <div
          className=" z-50 p-2 mt-5 ml-4 bg-white rounded-md dark:bg-slate-700 md:hidden cursor-pointer"
          onClick={() => router.back()}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </div>
  )
}

export default Back