import { FetchMock, MockResponseInitFunction } from 'jest-fetch-mock'
const fetchMock = fetch as FetchMock

export const apiMockSetup = (mockResponse: MockResponseInitFunction) => {
  fetchMock.resetMocks()
  fetchMock.mockResponse(mockResponse)
  return fetchMock
}
