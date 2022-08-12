export interface AppState {
  signIn: boolean,
  location: 'signup' | 'signin'
  status: 'loading' | 'idle'
}
