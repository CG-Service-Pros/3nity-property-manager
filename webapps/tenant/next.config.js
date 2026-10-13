/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    externalDir: true,
    cpus: 1
  },
  basePath: process.env.BASE_PATH || '',
  productionBrowserSourceMaps: false
};

module.exports = nextConfig;
