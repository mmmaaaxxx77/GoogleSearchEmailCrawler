import axios from 'axios';
import _ from 'lodash';
import { persistStore } from 'redux-persist';
import store from '../store';
import { setToken } from '../actions'
import { URL, STOCK_LIST, STOCK_SHAREHOLDER, STOCK_DETAIL } from '../config/Api';

export function getDetail() {
    const token = store.getState().token;

    if (!token)
        return null;

    return axios.get(URL + STOCK_DETAIL, { headers: { Authorization: 'Token ' + token } });    
}

export function getStockList() {
    const token = store.getState().token;

    if (!token)
        return null;

    return axios.get(URL + STOCK_LIST, { headers: { Authorization: 'Token ' + token } });    
}

export function getStockShareHolder(stock_id) {
    const token = store.getState().token;

    if (!token)
        return null;

    let url = URL + STOCK_SHAREHOLDER;

    if(stock_id)
    	url += "/" + stock_id + "/";

    return axios.get(url , { headers: { Authorization: 'Token ' + token } });
}