let host;

if (process.env.NODE_ENV === 'production') {
    host = 'https://your-backend-url.com';
}
else if (process.env.NODE_ENV === 'development') {
    host = 'http://127.0.0.1:5000'
}

export { host };