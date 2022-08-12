import { apiMockSetup } from '../utils/api-mock-setup'
import { signInAddr } from '../../ajax/api-addr'
import { sendRequestForSignin } from '../../ajax'
import { testUser } from '../utils/test-user'

describe('AJAX unit test on sign in', () => {
  beforeEach(() => {
    apiMockSetup(async (request: Request) => {
      if (request.method !== 'POST') {
        return ''
      }
      if (request.url !== signInAddr) {
        return ''
      }
      const data = await request.json()
      if (data.username !== testUser.username) return ''
      if (data.password !== testUser.password) return ''
      return 'theToken'
    })
  })
  it('should get the token', async function () {
    const result = await sendRequestForSignin({
      username: 'testUserName',
      password: 'testPassword'
    })
    expect(result).toEqual('theToken')
  })
})
