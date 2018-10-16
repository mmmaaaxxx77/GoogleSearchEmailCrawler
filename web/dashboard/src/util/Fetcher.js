import axios from 'axios';
import _ from 'lodash';
import { persistStore } from 'redux-persist';
import store from '../store';
import { setToken } from '../actions'
import { URL, EMAILJOBIN, EMAILJOBALL } from '../config/Api';

export function getEmailIn() {
    const token = store.getState().token;

    if (!token)
        return null;

    return axios.get(URL + EMAILJOBIN);
}

export function getEmailAll() {
    const token = store.getState().token;

    if (!token)
        return null;

    return axios.get(URL + EMAILJOBALL);
}