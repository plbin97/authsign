import { apiMockSetup } from '../utils/api-mock-setup'
import { userAddr } from '../../ajax/api-addr'
import { sendRequestForGetUserInfo } from '../../ajax'
import { User } from '../../models'

const testUserResult: User = {
  id: 123,
  username: 'testUser',
  first_name: 'Linbin',
  last_name: 'Pang',
  email: 'i@teenet.me',
  email_verified: false,
  password: '',
  phone: '9737522776',
  role: 'admin'
}

describe('AJAX unit test on getting user information', () => {
  beforeEach(() => {
    apiMockSetup(async (request: Request) => {
      if (request.method !== 'GET') {
        return ''
      }
      if (request.url !== userAddr) {
        return ''
      }
      const token = request.headers.get('X-Api-Key')
      if (!token) {
        return ''
      }
      if (token !== 'theToken') {
        return ''
      }
      return {
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(testUserResult),
        status: 200
      }
    })
  })
  it('should get user info', async function () {
    const result = await sendRequestForGetUserInfo('theToken')
    expect(result).toEqual(testUserResult)
  })
})
