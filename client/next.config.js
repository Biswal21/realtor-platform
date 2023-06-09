/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ["shelterkart1.s3.amazonaws.com"],
  },
  // env: {
  //   API_HOST: process.env.NEXT_PUBLIC_API_HOST,
  // },
};
// TODO: CHANGE THIS TO THE REAL DOMAIN

module.exports = nextConfig;
