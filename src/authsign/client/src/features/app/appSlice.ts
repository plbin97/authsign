import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState, AppThunk } from '../../app/store';

export interface AppState {
    isUser: false,
    location: 'signup' | 'signin'
    status: 'loading' | 'idle'
}

const initialState: AppState = {
    isUser: false,
    location: 'signin',
    status: 'idle'
}



export const appSlice = createSlice({
    name: 'app',
    initialState,
    reducers: {
        toSignin: (state) => {
            state.location = 'signin'
        },
        toSignup: (state) => {
            state.location = 'signup'
        }
    }
})