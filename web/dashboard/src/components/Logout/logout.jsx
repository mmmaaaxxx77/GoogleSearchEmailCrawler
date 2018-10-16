import React from "react";
import PropTypes from "prop-types";
import { Switch, Route, Redirect } from "react-router-dom";

// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
import pagesStyle from "assets/jss/material-dashboard-pro-react/layouts/pagesStyle.jsx";


import { getUser, setPersistStore, logOut } from "../../util/Auth";

// var ps;

class Logout extends React.Component {
  componentDidUnmount() {
  	console.log("logout");
  	logOut();
  }
  render() {
    const { classes, ...rest } = this.props;
    return (
      <div>       
      </div>
    );
  }
}

Logout.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(pagesStyle)(Logout);
