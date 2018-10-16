import React from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch } from "react-router-dom";

import indexRoutes from "routes/index.jsx";

import { getUser, setPersistStore } from "util/Auth";

import "assets/scss/material-dashboard-pro-react.css?v=1.2.0";

import { LOGINURL } from "config/Api";

const hist = createBrowserHistory();

// if(!window.location.href.includes(LOGINURL)){
// 	setPersistStore(function(){
// 		getUser();
// 	})
// }

ReactDOM.render(

  <Router history={hist}>
    <Switch>
      {indexRoutes.map((prop, key) => {
        return <Route path={prop.path} component={prop.component} key={key} />;
      })}
    </Switch>
  </Router>,
  document.getElementById("root")
);
