import { userAddr } from './api-addr'
import { UserSignInOut } from '../models'

export const sendRequestForSignup = async (userSignInOut: UserSignInOut): Promise<string | null> => {
  const response = await fetch(userAddr, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userSignInOut)
  })
  const resultText = await response.text()
  if (response.status !== 200) {
    return null
  }
  return resultText
}
