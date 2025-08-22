import { auth, db } from './firebase';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';

// Signup + save user to Firestore
export const signup = async (email: string, password: string) => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);

  // Save user data to Firestore
  await setDoc(doc(db, 'users', userCredential.user.uid), {
    uid: userCredential.user.uid,
    email: userCredential.user.email,
    createdAt: new Date()
  });

  return userCredential;
};

// Login
export const login = (email: string, password: string) =>
  signInWithEmailAndPassword(auth, email, password);

// Logout
export const logout = () => signOut(auth);

// Get current logged-in user
export const getCurrentUser = (): Promise<User | null> =>
  new Promise((resolve, reject) => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      unsubscribe();
      resolve(user);
    }, reject);
  });
