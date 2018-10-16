import React from "react";
// react component for creating dynamic tables
import ReactTable from "react-table";

// @material-ui/core components
import withStyles from "@material-ui/core/styles/withStyles";
// @material-ui/icons
import Assignment from "@material-ui/icons/Assignment";
import ViewList from "@material-ui/icons/ViewList";
import Dvr from "@material-ui/icons/Dvr";
import Favorite from "@material-ui/icons/Favorite";
import Close from "@material-ui/icons/Close";
// core components
import GridContainer from "components/Grid/GridContainer.jsx";
import GridItem from "components/Grid/GridItem.jsx";
import Button from "components/CustomButtons/Button.jsx";
import Card from "components/Card/Card.jsx";
import CardBody from "components/Card/CardBody.jsx";
import CardIcon from "components/Card/CardIcon.jsx";
import CardHeader from "components/Card/CardHeader.jsx";

import { dataTable } from "variables/general.jsx";

import { cardTitle } from "assets/jss/material-dashboard-pro-react.jsx";

import { getStockShareHolder } from "../../util/Stock";
import { setPersistStore } from "../../util/Auth";

import store from '../../store';
import axios from 'axios';
import { URL, STOCK_LIST, STOCK_SHAREHOLDER, STOCK_DETAIL } from '../../config/Api';

const styles = {
  cardIconTitle: {
    ...cardTitle,
    marginTop: "15px",
    marginBottom: "0px"
  }
};

class ReactTables extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loading: true,
      pages: 1,
      stock_id: null
    };
  }

  /*
  componentDidMount() {
    const self = this;
    setPersistStore(
      function(){
        getStockShareHolder().then(function(d){
          console.log(d);
          self.setState({data:d.data.data.map((prop, key) => {
            return {
              id: key,
              stock_id: prop['stock_id'],
              stock_name: prop['stock_name'],
              position: prop['position'],
              name: prop['name'],
              stock_count: prop['stock_count'],
              stock_percentage: prop['stock_percentage'],
              stock_update_date: prop['stock_update_date']              
            }
          })});
      });
    });
  }
  */

  render() {
    const self = this;
    const { classes } = this.props;
    return (
      <GridContainer>
        <GridItem xs={12}>
          <Card>
            <CardHeader color="primary" icon>
              <CardIcon color="primary">
                <ViewList />
              </CardIcon>
              <h4 className={classes.cardIconTitle}>大股東列表</h4>
            </CardHeader>
            <CardBody>
              <ReactTable
                data={this.state.data}
                filterable
                columns={[
                  {
                    Header: "類別",
                    accessor: "stock_type",
                    sortable: false,
                    width: 60
                  },                  
                  {
                    Header: "股票代號",
                    accessor: "stock_id",
                    sortable: false,
                    width: 80
                  },
                  {
                    Header: "股票名稱",
                    accessor: "stock_name",
                    sortable: false,
                    width: 100
                  },                  
                  {
                    Header: "職稱",
                    accessor: "position",
                    sortable: false
                  },
                  {
                    Header: "姓名/法人名稱",
                    accessor: "name",
                    sortable: false
                  },
                  {
                    Header: "持股張數",
                    accessor: "stock_count",
                    width: 90
                  },
                  {
                    Header: "持股比例",
                    accessor: "stock_percentage",
                    sortable: false,
                    filterable: false,
                    width: 80
                  },
                  {
                    Header: "更新時間",
                    accessor: "stock_update_date",
                    sortable: false,
                    width: 80
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

                loading={self.state.loading}
                pages={self.state.pages}
                manual
                onFetchData={(state, instance) => {

                    let url = URL + STOCK_SHAREHOLDER;

                    const page = state.page;
                    const pageSize = state.pageSize;
                    const sorted = state.sorted;
                    const filtered = state.filtered;

                    console.log(state);

                    if(self.state.stock_id)
                      url += "/" + self.state.stock_id + "/";

                    url += "?pageSize=" + pageSize;
                    url += "&page=" + page;

                    console.log(filtered);
                    for(let i=0;i<filtered.length;i++){
                      let ff = filtered[i];
                      url += "&" + ff['id'] + "=" + ff['value'];
                    }

                    for(let i=0;i<sorted.length;i++){
                      let ff = sorted[i];

                      let _sort = 'asc';
                      if(ff['desc']){
                        _sort = 'desc';
                      }
                      url += "&" + ff['id'] + "_sort=" + _sort;
                    }

                    // show the loading overlay
                    self.setState({loading: true})
                    // fetch your data
                    setPersistStore(function(){
                      const token = store.getState().token;
                      axios.get(url,
                      { headers: { Authorization: 'Token ' + token } })
                      .then((res) => {
                        // Update react-table
                        self.setState({
                          data: res.data.data.map((prop, key) => {
                            return {
                              id: key,
                              stock_type: prop['stock_type'],
                              stock_id: prop['stock_id'],
                              stock_name: prop['stock_name'],
                              position: prop['position'],
                              name: prop['name'],
                              stock_count: prop['stock_count'],
                              stock_percentage: prop['stock_percentage'],
                              stock_update_date: prop['stock_update_date']
                            }
                          }),
                          pages: res.data.count,
                          loading: false
                        })
                      })
                    });
                  }}
              />
            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
    );
  }
}

export default withStyles(styles)(ReactTables);
