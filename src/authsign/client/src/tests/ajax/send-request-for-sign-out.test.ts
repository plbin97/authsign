import { apiMockSetup } from '../utils/api-mock-setup'
import { signOutAddr } from '../../ajax/api-addr'
import { sendRequestForSignOut } from '../../ajax'

describe('AJAX unit test on sign out', () => {
  beforeEach(() => {
    apiMockSetup(async (request: Request) => {
      if (request.method !== 'GET') {
        return {
          status: 400
        }
      }
      if (request.url !== signOutAddr) {
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
  it('should sign out', async function () {
    const result = await sendRequestForSignOut('theToken')
    expect(result).toEqual(true)
  })
})
