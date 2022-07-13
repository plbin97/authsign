import { APIRequest } from './api'
import {FetchMock} from "jest-fetch-mock";
const fetchMock = fetch as FetchMock;

describe('testing api', () => {
  beforeEach(() => {
    fetchMock.resetMocks()
    fetchMock.mockResponse(async (request) => {
      return JSON.stringify({ data: '12345' })
    })
  })

  it('calls google and returns data to me', async () => {
    //assert on the response
    const res = await APIRequest('google')
    console.log(res)
    expect(res.data).toEqual('12345')

    //assert on the times called and arguments given to fetch
    expect(fetchMock.mock.calls.length).toEqual(1)
    expect(fetchMock.mock.calls[0][0]).toEqual('https://google.com')
  })
})