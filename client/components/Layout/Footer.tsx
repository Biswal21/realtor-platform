import React from "react";

const Footer = () => {
  return (
    <footer className="flex w-full  justify-center bg-gray-200 p-4 dark:bg-slate-900 md:items-center md:justify-between md:p-6">
      <span className="flex flex-wrap text-sm text-neutral-500 dark:text-neutral-400 sm:text-center">
        <a href="#" className="hover:underline">
          Shelterkart
        </a>
        &nbsp;© 2022. All rights reserved.
      </span>
    </footer>
  );
};

export default Footer;
