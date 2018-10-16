import React from 'react';
// react component used to create sweet alerts
import SweetAlert from "react-bootstrap-sweetalert";
// material-ui components
import withStyles from "@material-ui/core/styles/withStyles";
// core components
import Button from "components/CustomButtons/Button.jsx";
// styles for buttons on sweetalert
import sweetAlertStyle from "assets/jss/material-dashboard-pro-react/views/sweetAlertStyle.jsx";
// react component for creating dynamic tables
import ReactTable from "react-table";
// @material-ui/icons
import Assignment from "@material-ui/icons/Assignment";
import ViewList from "@material-ui/icons/ViewList";
import Dvr from "@material-ui/icons/Dvr";
import Favorite from "@material-ui/icons/Favorite";
import Edit from "@material-ui/icons/Edit";
import Close from "@material-ui/icons/Close";
// @material-ui/icons
import MailOutline from "@material-ui/icons/MailOutline";
import Check from "@material-ui/icons/Check";
import Contacts from "@material-ui/icons/Contacts";
import FiberManualRecord from "@material-ui/icons/FiberManualRecord";
import CustomInput from "components/CustomInput/CustomInput.jsx";
import FormLabel from "@material-ui/core/FormLabel";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Radio from "@material-ui/core/Radio";
import Checkbox from "@material-ui/core/Checkbox";
// core components
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import Card from "components/Card/Card.jsx";
import CardBody from "components/Card/CardBody.jsx";
import CardIcon from "components/Card/CardIcon.jsx";
import CardHeader from "components/Card/CardHeader.jsx";
import moment from 'moment';

import { dataTable } from "variables/general.jsx";

import { getEmailIn, getEmailAll } from "../../util/Fetcher";
import { setPersistStore } from "../../util/Auth";

import axios from 'axios';
import { URL, EMAILJOBIN, EMAILJOBALL } from '../../config/Api';
import store from '../../store';

class ReactTables extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      alert: null,
      editId: null,
      editTitle: null,
      editQuery: null,
      isEditQuery: null
    };
    this.hideAlert = this.hideAlert.bind(this);
  }

  hideAlert() {
    this.setState({
      alert: null
    });
  }

  inputAlert() {
    this.setState({
      alert: (
        <SweetAlert
          input
          showCancel
          style={{ display: "block", marginTop: "-100px" }}
          title="Input something"
          onConfirm={e => this.inputConfirmAlert(e)}
          onCancel={() => this.hideAlert()}
          confirmBtnCssClass={
            this.props.classes.button + " " + this.props.classes.info
          }
          cancelBtnCssClass={
            this.props.classes.button + " " + this.props.classes.danger
          }
        />
      )
    });
  }

  showAlert(id, title, query, isQuery) {

    let alertTitle = "修改『" + title + "』的Title";
    if(isQuery){
      alertTitle = "修改『" + title +"』的Query ";
    }

    this.setState({
      editId: id,
      editTitle: title,
      editQuery: query,
      isEditQuery: isQuery
    });

    this.setState({
      alert: (
        <SweetAlert
          input
          showCancel
          style={{ display: "block", marginTop: "-100px" }}
          title={alertTitle}
          onConfirm={e => this.postHotPostEdit(e)}
          onCancel={() => this.hideAlert()}
          confirmBtnCssClass={
            this.props.classes.button + " " + this.props.classes.info
          }
          cancelBtnCssClass={
            this.props.classes.button + " " + this.props.classes.danger
          }
        />
      )
    });
  }

 postHotPostEdit(e){

    console.log(e);
    console.log(this.state.editId, this.state.editTitle,this.state.editQuery,this.state.isEditQuery);

    const self = this;

    axios.post(URL + EMAILJOBALL, {
        id: this.state.editId,
        title: this.state.isEditQuery?this.state.editTitle:e,
        query: this.state.isEditQuery?e:this.state.editQuery
    })
    .then(function(response) {
        console.log(response);
        self.hideAlert();
        self.componentDidMount();
    })
    .catch(function(error) {
        console.log(error);
    });
  }

  componentDidMount() {
    const self = this;
    setPersistStore(
      function(){
        getEmailAll().then(function(d){
          console.log(d);
          self.setState({data:d.data.map((prop, key) => {

            let id = prop['id'];
            let created_at = prop['created_at'];
            let title = prop['title'];
            let query_url = prop['query_url'];
            let skip_url = prop['skip_url'];
            let total_count = prop['total_count'];
            let skip_count = prop['skip_count'];
            let status = prop['status'];
            let filename = prop['filename'];
            let actions = (
                <div className="actions-right">
                  <Button
                    justIcon
                    round
                    simple
                    onClick={self.inputAlert.bind(self)}
                    color="info"
                    className="like"
                    size="sm"
                  >
                    <Edit />
                  </Button>{" "}
                </div>
              );
            
            const fd = moment(created_at, 'YYYY-MM-DD h:mm:ss a').toDate();
            created_at = moment(fd).format('YYYY-MM-DD');

            if(status == "DONE"){
              let d_link = "http://gcrawlerapi.johnnyplanet.com/api/downloadexcel" + filename;
              status = (<a href={d_link} target="_blank">完成 (下載EXCEL)</a>);
            }

            return {
              created_at: created_at,
              title: title,
              total_count: total_count,
              skip_count: skip_count,
              status: status,
              actions: actions
            }
          })});
      });
    });
    self.loopTable();
  }

  loopTable(){
    const self = this;
    window.setTimeout(function(){
      self.componentDidMount();
    },5000); 
  }  

  render() {
    const self = this;
    const { classes } = this.props;
    return (      
      <GridContainer>      
        {this.state.alert}
       <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="rose" icon>
              <CardIcon color="rose">
                <MailOutline />
              </CardIcon>
              <h4 className={classes.cardIconTitle}>Stacked Form</h4>
            </CardHeader>
            <CardBody>
              <form action="http://gcrawlerapi.johnnyplanet.com/api/alljob" method="post">
                <CustomInput
                  labelText="Google 查詢 URL"
                  id="query_url"                  
                  formControlProps={{
                    fullWidth: true
                  }}
                  inputProps={{
                    type: "text",
                    name: "query_url"
                  }}
                />
                <CustomInput
                  labelText="略過URL (半型逗點分隔)"
                  id="skip_url"                  
                  formControlProps={{
                    fullWidth: true
                  }}
                  inputProps={{
                    type: "text",
                    "name": "skip_url"
                  }}
                />
                <Button type="submit" color="rose">新增任務</Button>
              </form>
            </CardBody>
          </Card>
        </GridItem>        
        <GridItem xs={12}>
          <Card>            
            <CardHeader color="primary" icon>
              <CardIcon color="primary">
                <ViewList />
              </CardIcon>
              <h4 className={classes.cardIconTitle}>時事話題設定</h4>
            </CardHeader>
            <CardBody>
              <ReactTable
                data={this.state.data}
                filterable
                columns={[
                 {
                    Header: "送出時間",
                    accessor: "created_at",
                    width: 150
                  },
                  {
                    Header: "搜尋主題",
                    accessor: "title"
                  },
                  {
                    Header: "Google總數",
                    accessor: "total_count",
                    width: 120
                  },
                  {
                    Header: "略過網頁總數",
                    accessor: "skip_count",
                    width: 120
                  },
                  {
                    Header: "狀態",
                    accessor: "status",
                    filterable: false,
                    width: 150
                  }
                ]}
                defaultPageSize={10}
                showPaginationTop
                showPaginationBottom={false}
                className="-striped -highlight"
                previousText='上一頁'
                nextText='下一頁'
                loadingText='資料讀取中...'
                noDataText='無資料...'
                pageText='頁數'
                ofText='/'
                rowsText='筆'
              />
            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
    );
  }
}

export default withStyles(sweetAlertStyle)(ReactTables);