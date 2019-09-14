import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';

import Chart from './Graph/Chart'

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  firstpaper: {
    padding: theme.spacing(2),
    minHeight: '10vh',
    textAlign: 'center',
    color: 'white', //theme.palette.text.secondary,
    fontSize: '18pt',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#3371c5',
  },
  paper: {
    padding: theme.spacing(2),
    height: 'auto',
    textAlign: 'center',
    color: theme.palette.text.secondary,
    overflowWrap: 'break-word',
    overflowy: 'scroll',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
}));

const grabRepos = () => {
  fetch('https://api.github.com/users/fcr3/repos')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    console.log(JSON.stringify(myJson));
  });
}

export default function CenteredGrid() {
  const classes = useStyles();

  var data = [[0, 3],[5, 13],[10, 22],[15, 36],[20, 48],[25, 59],
    [30, 77],[35, 85],[40, 95],[45, 105],[50, 120],[55, 150],
    [60, 147],[65, 168],[70, 176],[75, 188],[80, 199],[85, 213],
    [90, 222],[95, 236],[100, 249]]

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper className={classes.firstpaper}>
            Welcome to the ncappzoo analysis webapp!
          </Paper>
        </Grid>
        <Grid item xs={12} m={6}>
          <Paper className={classes.paper}>
            Go to the Menu. Check out the views and the clones!
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            Tutorial: Hover over the data points to see the data <br/>
            <Chart data={data}/>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
