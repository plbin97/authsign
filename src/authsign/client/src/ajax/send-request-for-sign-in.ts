import { UserSignInOut } from '../models'
import { signInAddr } from './api-addr'

export const sendRequestForSignin = async (userSignInOut: UserSignInOut): Promise<string | null> => {
  const response = await fetch(signInAddr, {
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
