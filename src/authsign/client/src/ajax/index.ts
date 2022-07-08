import {userAddr, signInAddr} from "./apiAddr";
import UserSignInOut from "../models/UserSignInOut";

export const sendRequestForSignin = async (userSignInOut: UserSignInOut): Promise<string | null> => {
    let response = await fetch(signInAddr, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userSignInOut)
    });
    let resultText = await response.text();
    if (response.status !== 200) {
        return null;
    }
    return resultText;
}

export const sendRequestForSignup = async (userSignInOut: UserSignInOut): Promise<string | null> => {
    let response = await fetch(userAddr, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userSignInOut)
    });
    let resultText = await response.text();
    if (response.status !== 200) {
        return null;
    }
    return resultText;

}

