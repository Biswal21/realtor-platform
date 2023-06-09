import React, { useEffect, useState } from "react";
import { useTheme } from "next-themes";

const ThemeToggler: React.FC = () => {
  const { systemTheme, theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState<Boolean>(false);

  const currentTheme = () => {
    const presentTheme = theme === "system" ? systemTheme : theme;
    return presentTheme;
  };

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <>
      {!mounted ? null : (
        <div>
          {currentTheme() === "dark" ? (
            <div
              className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-400 text-gray-100"
              onClick={() => setTheme("light")}
            >
              <svg
                className="h-6 w-6"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                  clipRule="evenodd"
                ></path>
              </svg>
            </div>
          ) : (
            <div
              className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-lg border-2 border-gray-400 text-gray-900"
              onClick={() => setTheme("dark")}
            >
              <svg
                className="h-6 w-6 "
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                ></path>
              </svg>
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default ThemeToggler;
