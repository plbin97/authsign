import {sendRequestForSignin, sendRequestForSignup} from "./appAPI";
import {FetchMock} from "jest-fetch-mock";

const fetchMock = fetch as FetchMock;
import {signInAPIAddr, signUpAPIAddr} from "../../app/apiAddr";

// Means the user existed in the database
const testUser = {
    username: 'testUserName',
    password: 'testPassword',
    token: 'asdfasdfsadfasdfafsdf'
}

const newUser = {
    username: 'anotherOne',
    password: 'hihihi',
    token: 'sdfadfdsfdsf'
}


describe('MockApi Testing', () => {
    beforeEach(() => {
        fetchMock.resetMocks()
        fetchMock.mockResponse(async (request: Request) => {
            switch (request.url) {
                case signInAPIAddr:
                    const signInResult = await request.json()
                    if (signInResult['username'] !== testUser.username || signInResult['password'] !== testUser.password) {
                        return {
                            status: 400,
                            body: 'Username or password incorrect'
                        }
                    }
                    return {
                        status: 200,
                        body: testUser.token
                    }
                case signUpAPIAddr:
                    const signUpResult = await request.json()
                    if (signUpResult['username'] === testUser.username) {
                        return {
                            status: 400,
                            body: 'Username is unavailable'
                        }
                    }
                    if (signUpResult['password'] === undefined) {
                        return {
                            status: 400,
                            body: 'Lack of parameters'
                        }
                    }
                    return {
                        status: 200,
                        body: newUser.token
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
        let [isSuccess, resultText] = await sendRequestForSignin(testUser.username, testUser.password);
        expect(isSuccess).toBe(true);
        expect(resultText).toBe(testUser.token);
    })
    test('Sign in negative test', async () => {
        let [isSuccess, resultText] = await sendRequestForSignin(testUser.username + '123', testUser.password);
        expect(isSuccess).toBe(false);
    })

    test('Sign up positive test', async () => {
        let [isSuccess, resultText] = await sendRequestForSignup(newUser.username, newUser.password);
        expect(isSuccess).toBe(true);
        expect(resultText).toBe(newUser.token)
    })

    test('Sign up negative test', async () => {
        let [isSuccess, resultText] = await sendRequestForSignup(testUser.username, newUser.password);
        expect(isSuccess).toBe(false)
    })

})