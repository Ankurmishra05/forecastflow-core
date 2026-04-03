# ForecastFlow UI

React frontend for the ForecastFlow prediction API.

## Local development

1. Copy `.env.example` to `.env`.
2. Set `REACT_APP_API_BASE_URL` to your backend URL.
3. Run `npm install`.
4. Run `npm start`.

If you are running the FastAPI app locally, use:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Deployment

For a hosted frontend, add this environment variable in your frontend hosting dashboard:

```env
REACT_APP_API_BASE_URL=https://your-render-backend.onrender.com
```

Without that variable, the app falls back to `http://localhost:8000`, which only works for local development.
