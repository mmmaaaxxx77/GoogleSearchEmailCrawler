import axios from 'axios';
import _ from 'lodash';
import { persistStore } from 'redux-persist';
import store from '../store';
import { setToken } from '../actions'
import { URL, LOGIN, USER, LOGOUT } from '../config/Api';

export function InvalidCredentialsException(message) {
    this.message = message;
    this.name = 'InvalidCredentialsException';
}

export function login(username, password) {

    axios.post(URL + LOGIN, {
            username,
            password
        })
        .then(function(response) {
            store.dispatch(setToken(response.data.token));
            window.location.href = "/";
        })
        .catch(function(error) {
            // raise different exception if due to invalid credentials
            // if (_.get(error, 'response.status') === 400) {
            //     throw new InvalidCredentialsException(error);
            // }
            // throw error;
            //window.location.href = "/pages/login-page";
        });
}

export function loggedIn() {
    return store.getState().token != null;
}

export function setPersistStore(init) {
    return persistStore(store, {}, init);
}

export function getUser() {
    const token = store.getState().token;

    if (!token)
        return null;

    return axios.get(URL + USER, { headers: { Authorization: 'Token ' + token } }).catch(error => {
        store.dispatch({
            type: 'RESET'
        });
    });
}

export function logOut() {
    let init = function() {
        const token = store.getState().token;
        axios.get(URL + LOGOUT, { headers: { Authorization: 'Token ' + token } }).then(function() {
            store.dispatch({
                type: 'RESET'
            });
            window.location.href = "/";
        }).catch(error => {
            store.dispatch({
                type: 'RESET'
            });
            window.location.href = "/pages/login-page";
        });
    };
    setPersistStore(init);
}