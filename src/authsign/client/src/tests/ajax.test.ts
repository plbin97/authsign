import {sendRequestForSignin, sendRequestForSignup} from "../ajax";
import {FetchMock} from "jest-fetch-mock";
import {userAddr, signInAddr} from "../ajax/apiAddr";
import UserSignInOut from "../models/UserSignInOut";

const fetchMock = fetch as FetchMock;

// Means the user existed in the database
const testUser: UserSignInOut = {
    username: 'testUserName',
    password: 'testPassword'
}
const testUserToken = 'asdfasdfs'

const newUser: UserSignInOut = {
    username: 'anotherOne',
    password: 'hihihi'
}
const newUserToken = 'asdfgerger'


describe('MockApi Testing', () => {
    beforeEach(() => {
        fetchMock.resetMocks()
        fetchMock.mockResponse(async (request: Request) => {
            switch (request.url) {
                case signInAddr:
                    if (request.method !== 'POST') {
                        return {
                            status: 404,
                            body: ''
                        }
                    }
                    const signInResult: UserSignInOut = await request.json()
                    if (signInResult.username !== testUser.username || signInResult.password !== testUser.password) {
                        return {
                            status: 400,
                            body: 'Username or password incorrect'
                        }
                    }
                    return {
                        status: 200,
                        body: testUserToken
                    }
                case userAddr:
                    switch (request.method) {
                        case 'POST':
                            const signUpResult: UserSignInOut = await request.json()
                            if (signUpResult.username === testUser.username) {
                                return {
                                    status: 400,
                                    body: 'Username is unavailable'
                                }
                            }
                            return {
                                status: 200,
                                body: newUserToken
                            }
                        default:
                            return {
                                status: 404,
                                body: ''
                            }
                    }
                default:
                    return {
                        status: 404,
                        body: 'Invalid URL'
                    }
            }
        })
    })
    test('Sign in positive test', async () => {
        let resultText = await sendRequestForSignin(testUser);
        expect(resultText).toBe(testUserToken);
    })
    test('Sign in negative test', async () => {
        const wrongTestUser: UserSignInOut = {
            username: testUser.username + '123',
            password: testUser.password
        }
        let resultText = await sendRequestForSignin(wrongTestUser);
        expect(resultText).toBeNull();
    })

    test('Sign up positive test', async () => {
        let resultText = await sendRequestForSignup(newUser);
        expect(resultText).toBe(newUserToken)
    })

    test('Sign up negative test', async () => {
        const wrongNewUser: UserSignInOut = {
            username: testUser.username,
            password: newUser.password
        }
        let resultText = await sendRequestForSignup(wrongNewUser);
        expect(resultText).toBeNull()
    })

})