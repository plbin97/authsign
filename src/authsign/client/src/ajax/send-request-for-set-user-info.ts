import { userAddr } from './api-addr'
import { User } from '../models'

export const sendRequestForSetUserInfo = async (token: string, userInfo: Omit<User, any>): Promise<boolean> => {
  const response = await fetch(userAddr, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-Api-Key': token
    },
    body: JSON.stringify(userInfo)
  })
  return response.status === 200
}
