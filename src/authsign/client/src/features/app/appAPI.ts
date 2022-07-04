import {signInAPIAddr, signUpAPIAddr} from "../../app/apiAddr";

export const sendRequestForSignin = async (username: string, password: string): Promise<[boolean, string]> => {
    let response = await fetch(signInAPIAddr, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password
        })
    });
    let resultText = await response.text();
    if (response.status !== 200) {
        return [false, resultText];
    }
    return [true, resultText]
}

export const sendRequestForSignup = async (username: string, password: string): Promise<[boolean, string]> => {
    let response = await fetch(signUpAPIAddr, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password
        })
    });
    let resultText = await response.text();
    if (response.status !== 200) {
        return [false, resultText];
    }
    return [true, resultText];

}