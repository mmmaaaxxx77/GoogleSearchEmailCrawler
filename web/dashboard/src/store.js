import { compose, createStore, applyMiddleware } from 'redux';
import { createLogger } from 'redux-logger';
import { persistStore, autoRehydrate } from 'redux-persist';
import reduxReset from 'redux-reset'
import rootReducer from './reducers';
import { getUser } from './util/Auth'

const store = createStore(
    rootReducer,
    compose(
        applyMiddleware(
            createLogger(),
        ),
        reduxReset(),
        autoRehydrate()
    )
);
persistStore(store, {}, function() {
	// const user = getUser().then(function(d){
	// 	console.log(d.data);
	// });     
});
export default store;