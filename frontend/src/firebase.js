import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

// Your Firebase configuration
// Replace these with your actual Firebase project config
const firebaseConfig = {
  apiKey: "AIzaSyBJT8YJDfNz-QwzR_trpIxEQaB-S6aMa9U",
  authDomain: "contextllm-42080.firebaseapp.com",
  projectId: "contextllm-42080",
  storageBucket: "contextllm-42080.firebasestorage.app",
  messagingSenderId: "390264275141",
  appId: "1:390264275141:web:8af9e60c342d2b5b66b0ac",
  measurementId: "G-9F5RZJHHNR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app)

export default app