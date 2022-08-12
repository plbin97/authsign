import { apiMockSetup } from '../utils/api-mock-setup'
import { userAddr } from '../../ajax/api-addr'
import { sendRequestForSetUserInfo } from '../../ajax'

describe('AJAX unit test on setting user information', () => {
  beforeEach(() => {
    apiMockSetup(async (request: Request) => {
      if (request.method !== 'PUT') {
        return {
          status: 400
        }
      }
      if (request.url !== userAddr) {
        return {
          status: 400
        }
      }
      const token = request.headers.get('X-Api-Key')
      if (!token) {
        return {
          status: 400
        }
      }
      if (token !== 'theToken') {
        return {
          status: 400
        }
      }
      return {
        status: 200
      }
    })
  })
  it('should set user info', async function () {
    const result = await sendRequestForSetUserInfo('theToken', {
      first_name: 'Linbin',
      last_name: 'Pang'
    })
    expect(result).toEqual(true)
  })
})
