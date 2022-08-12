import { apiMockSetup } from '../utils/api-mock-setup'
import { userAddr } from '../../ajax/api-addr'
import { sendRequestForSignup } from '../../ajax'
import { testUser } from '../utils/test-user'

describe('AJAX unit test on sign up', () => {
  beforeEach(() => {
    apiMockSetup(async (request: Request) => {
      if (request.method !== 'POST') {
        return ''
      }
      if (request.url !== userAddr) {
        return ''
      }
      const data = await request.json()
      if (data.username !== testUser.username) return ''
      if (data.password !== testUser.password) return ''
      return 'theToken'
    })
  })

  it('should get the token', async function () {
    const result = await sendRequestForSignup({
      username: 'testUserName',
      password: 'testPassword'
    })
    expect(result).toEqual('theToken')
  })
})
