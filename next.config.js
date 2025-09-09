/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['books.google.com'], // For Google Books API cover images
  },
}

module.exports = nextConfig