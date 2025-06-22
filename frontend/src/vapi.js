import Vapi from '@vapi-ai/web'

// Initialize Vapi with your API key from environment variable
const vapi = new Vapi(import.meta.env.VITE_VAPI_API_KEY)

export default vapi