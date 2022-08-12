import { userAddr } from './api-addr'
import { User } from '../models'

export const sendRequestForGetUserInfo = async (token: string): Promise<User | null> => {
  const response = await fetch(userAddr, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Api-Key': token
    }
  })
  const result = await response.json()
  if (response.status !== 200) {
    return null
  }
  return result as User
}
