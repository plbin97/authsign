import { signOutAddr } from './api-addr'

export const sendRequestForSignOut = async (token: string): Promise<boolean> => {
  const response = await fetch(signOutAddr, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Api-Key': token
    }
  })
  return response.status === 200
}
